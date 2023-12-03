from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Logic executed on each request before the view is called
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            if not request.user.profile.is_email_active and request.path != '/management/verify-email/' and request.path != '/admin/':
                return redirect('verify_email')  # Replace 'your_specific_url' with the actual URL or URL name
        return None