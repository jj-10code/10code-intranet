from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone

class ActivityTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if user is still active
            if not request.user.is_active:
                # User has been deactivated, logout and redirect
                logout(request)
                return redirect('login')
            
            # Store the last activity time in the session
            # This complements SESSION_SAVE_EVERY_REQUEST which rotates the expiry
            request.session['last_activity'] = timezone.now().isoformat()
        
        response = self.get_response(request)
        return response
