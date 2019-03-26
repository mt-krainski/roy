from django.shortcuts import render, redirect
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, \
    permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@api_view(['GET'])
@authentication_classes((TokenAuthentication,))
@permission_classes((IsAuthenticated,))
def activity_manager(request):
    if not request.user.is_authenticated:
        # todo:
        # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return "You need to be logged in..."

    print(request)

    return Response("Success")

#     request.GET
#     request.POST
#     request.userk
