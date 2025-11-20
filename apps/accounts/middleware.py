from django.utils import timezone

class ActivityTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Store the last activity time in the session
            # This complements SESSION_SAVE_EVERY_REQUEST which rotates the expiry
            request.session['last_activity'] = timezone.now().isoformat()
        
        response = self.get_response(request)
        return response
