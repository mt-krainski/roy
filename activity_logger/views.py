from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.utils import timezone
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
