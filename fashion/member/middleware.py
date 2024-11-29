from django.shortcuts import redirect
from django.urls import reverse

class CheckSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not (request.path.startswith('/login/') or request.path.startswith('/register/')) and 'user_id' not in request.session:
            return redirect(reverse('login'))  # Chuyển hướng đến trang login

        response = self.get_response(request)
        return response