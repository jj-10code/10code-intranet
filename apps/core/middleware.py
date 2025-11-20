from django.middleware.csrf import get_token
from inertia import share

class InertiaShareMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        share(request, csrf_token=get_token(request))
        response = self.get_response(request)
        return response
