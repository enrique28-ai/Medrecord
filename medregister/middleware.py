# middleware.py
from django.utils import timezone
from zoneinfo import ZoneInfo, available_timezones

class UserTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tz = None

        # ① Preferencia guardada
        if request.user.is_authenticated and hasattr(request.user, "userprofile"):
            tz = request.user.userprofile.timezone

        # ② Detectada por navegador (cookie)
        if not tz:
            tz = request.COOKIES.get("user_tz")

        # ③ Valida y activa
        if tz in available_timezones():
            timezone.activate(ZoneInfo(tz))
        else:
            timezone.deactivate()   # caerá en TIME_ZONE de settings

        return self.get_response(request)
