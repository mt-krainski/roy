from datetime import timedelta
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
import plotly.offline as opy
import plotly.graph_objs as go
from django.utils.timezone import now
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from activity_logger.models import Establishment, ActivityType, Activity

ACTIVITY_START = 'start'
ACTIVITY_FINISH = 'finish'

VALID_REQUEST_TYPES = (
    ACTIVITY_FINISH,
    ACTIVITY_START,
)


@api_view(['POST'])
@authentication_classes((TokenAuthentication,))
@permission_required('activity_logger.add')
@login_required
def activity_manager_view(request):
    """Manage activities - add new or finish existing one.

    Request structure:
    {
        'type': ('start', 'finish'),
        'establishment': 'establishment-slug', (only for type=='start')
        'activity_type': 'activity-type-slug', (only for type=='start')
        'activity_uuid': 'activity-uuid' (only for type=='finish')

    }
    """

    request_type = request.data.get('type')
    if request_type not in VALID_REQUEST_TYPES:
        return HttpResponse(
            'Improper request type - "type" has to be '
            f'in {VALID_REQUEST_TYPES}.',
            status=422,
        )

    if request_type == ACTIVITY_START:
        return start_activity(
            request.data.get('establishment'),
            request.data.get('activity_type'),
            request.user
        )

    elif request_type == ACTIVITY_FINISH:
        return finish_activity(
            request.data.get(
                'activity_uuid'
            ).replace('"', '').replace('\'', ''),
            request.user)


def start_activity(
    establishment, activity_type, user,
        activity_name='From API'
):
    """Start a new activity based on passed parameters.

    Passed parameters are slugs.

    Return uuid of a newly started activity.
    Raises Establishment.DoesNotExist or ActivityType.DoesNotExist
        if selected establishment or activity_type do not exist
    """

    try:
        establishment = Establishment.objects.get(slug=establishment)
        activity_type = ActivityType.objects.get(slug=activity_type)
        new_item = Activity.objects.create(
            name=activity_name,
            activity_type=activity_type,
            establishment=establishment,
            user=user,
            start_time=timezone.now()
        )
    except Establishment.DoesNotExist:
        return HttpResponse(
            'Establishment not recognized.',
            status=422,
        )
    except ActivityType.DoesNotExist:
        return HttpResponse(
            'Activity type not recognized.',
            status=422,
        )

    return Response(new_item.uuid)


def finish_activity(
    activity_uuid, user
):
    """Finish activity given by uuid.

    Works only if user matches the activity uuid and the activity is not yet
    finished.
    """
    try:
        item = Activity.objects.get(
            uuid=activity_uuid,
            user=user,
            end_time__isnull=True,
        )
        item.end_time = timezone.now()
        item.save()
    except Activity.DoesNotExist or ValidationError:
        return HttpResponse(
            'Invalid UUID',
            status=422
        )

    return Response("Success")


@login_required
def summary_view(request):

    data = Activity.objects.filter(
        user=request.user,
        start_time__isnull=False,
        end_time__isnull=False,
        start_time__gt=now()-timedelta(days=30)
    )

    activity_types = ActivityType.objects.filter(user=request.user)

    results = []
    for day in [(now()-timedelta(days=n)).date() for n in range(0, 30)]:
        day_data = data.filter(
            Q(start_time__date=day) |
            Q(start_time__date=day-timedelta(days=1), end_time__date=day)
        )
        # if day_data.exists():
        activities = {}
        for activity in day_data:
            if activity.end_time.date() == activity.start_time.date():
                delta = activity.end_time - activity.start_time
            else:
                delta = (
                    activity.end_time -
                    activity.end_time.replace(hour=0, minute=0, second=0)
                )
            delta = delta - timedelta(microseconds=delta.microseconds)
            current_delta = activities.get(
                activity.activity_type.slug, timedelta())

            activities[activity.activity_type.slug] = current_delta + delta

        total_recorded = sum(activities.values(), timedelta())
        activities['other'] = timedelta(hours=24) - total_recorded

        results.append(
            (day, activities)
        )

    data_traces = [go.Bar(
        x=[
            day
            for day, data
            in results
        ],
        y=[
            data[activity_type.slug].total_seconds()/3600
            if activity_type.slug in data else 0
            for day, data
            in results
        ],
        text=[
            f'{activity_type.name}: {str(data[activity_type.slug])}'
            if activity_type.slug in data else ''
            for day, data
            in results
        ],
        name=activity_type.name,
        hoverinfo='text',
    ) for activity_type in activity_types] + [
        go.Bar(
            x=[
                day
                for day, data
                in results
                if 'other' in data
            ],
            y=[
                data['other'].total_seconds()/3600
                if 'other' in data else 0
                for day, data
                in results
            ],
            text=[
                f'Other: {str(data["other"])}'
                if 'other' in data else ''
                for day, data
                in results
            ],
            name='Other',
            hoverinfo='text',
            marker=dict(
                color='#ECEFF1',
            ),
        )
    ]

    layout = go.Layout(
        barmode='stack',
        title='Activities report',
        yaxis=dict(
            title='Duration [h]',
            range=[0, 24],
            tickvals=list(range(0, 25, 2)),
        ),
    )

    figure = go.Figure(data=data_traces, layout=layout)

    div = opy.plot(figure, output_type='div')

    return render(
        request, 'activity_logger/summary.html',
        {'graph': div}
    )
