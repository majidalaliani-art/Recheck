from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.shortcuts import redirect

class AdminRequiredMixin(LoginRequiredMixin, AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        staff = request.user
        if not staff.is_superuser and not staff.is_staff:
            return redirect('Base:login')

        return super().dispatch(request, *args, **kwargs)
