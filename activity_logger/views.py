from django.shortcuts import render, redirect


def activity_manager(request):
    if not request.user.is_authenticated:
        # todo:
        # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
        return "You need to be logged in..."

    print(request)

    return "Empty"

#     request.GET
#     request.POST
#     request.user
