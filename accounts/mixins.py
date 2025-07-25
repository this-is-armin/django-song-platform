from django.shortcuts import redirect


class AnonymousRequiredMixin:
    REDIRECT_URL = 'core:home'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
    
    def handle_no_permission(self):
        return redirect(self.REDIRECT_URL)