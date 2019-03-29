from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import SuspiciousOperation
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


@api_view(['POST', 'GET'])
@authentication_classes((TokenAuthentication,))
@permission_required('activity_logger.add')
@login_required
def activity_manager_view(request):
    """Manage activities - add new or finish existing one.

    Request structure:
    {
        'type': ('start', 'finish'),
        'establishment': 'establishment-slug',
        'activity_type': 'activity-type-slug',
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

        try:
            establishment = Establishment.objects.get(
                slug=request.data.get('establishment'))
        except Establishment.DoesNotExist:
            return HttpResponse(
                'Establishment not recognized.',
                status=422,
            )

        try:
            activity_type = ActivityType.objects.get(
                slug=request.data.get('activity_type'))
        except ActivityType.DoesNotExist:
            return HttpResponse(
                'Activity Type not recognized.',
                status=422,
            )

        new_item = Activity.objects.create(
            name='From API',
            activity_type=activity_type,
            establishment=establishment,
            user=request.user,
            start_time=timezone.now()
        )
        return Response(new_item.uuid)

    elif request_type == ACTIVITY_FINISH:

        activity_uuid = request.data.get('activity_uuid')

        try:
            item = Activity.objects.get(
                uuid=activity_uuid,
                user=request.user,
                end_time__isnull=False,
            )
        except Activity.DoesNotExist:
            return HttpResponse(
                'Invalid UUID',
                422
            )
        item.end_time = timezone.now()
        item.save()

        return Response("Success")
