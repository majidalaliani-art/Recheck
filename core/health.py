from django.db import connection
from django.core.cache import cache
from django.http import JsonResponse


def health_check(request):
    """
    Health check endpoint returning system status including DB and cache connectivity.
    """
    status = {"status": "ok", "db": "ok", "cache": "ok"}
    http_status = 200

    # Test Database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception as e:
        status["db"] = f"error: {str(e)}"
        status["status"] = "error"
        http_status = 503

    # Test Cache
    try:
        cache.set("health_check_test", "1", timeout=5)
        if cache.get("health_check_test") != "1":
            status["cache"] = "cache get failed"
            if status["status"] == "ok":
                status["status"] = "degraded"
    except Exception as e:
        status["cache"] = f"error: {str(e)}"
        if status["status"] == "ok":
            status["status"] = "degraded"

    return JsonResponse(status, status=http_status)
