from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from account.models import BaleToken
import secrets


@csrf_exempt
@require_POST
def register_view(request):
    now = timezone.now()

    # پاک‌سازی توکن‌های منقضی‌شده
    BaleToken.objects.filter(expiration_date__lt=now).delete()

    device_id = request.POST.get("device_id")
    token = request.POST.get("token")
    user_id = request.POST.get("user_id")
    first_name = request.POST.get("first_name")
    phone_number = request.POST.get("phone_number")

    if not device_id:
        return JsonResponse({"ok": False, "error": "device_id is required"}, status=400)

    # ======================
    # 1. دریافت وضعیت توکن
    # ======================
    if token and not user_id:
        try:
            bale_token = BaleToken.objects.get(
                token=token,
                device_identifier=device_id,
                expiration_date__gt=now
            )
            return JsonResponse({
                "ok": True,
                "token": bale_token.token,
                "user_id": bale_token.bale_id,
                "first_name": bale_token.first_name,
                "phone_number": bale_token.phone_number,
                "now": now,
                "expires_at": bale_token.expiration_date,
            })
        except BaleToken.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Invalid or expired token"}, status=404)

    # ======================
    # 2. آپدیت از سمت ربات بله
    # ======================
    if token and user_id:
        try:
            bale_token = BaleToken.objects.get(
                token=token,
                expiration_date__gt=now
            )
            bale_token.bale_id = user_id
            bale_token.first_name = first_name
            bale_token.phone_number = phone_number
            bale_token.save()

            return JsonResponse({"ok": True})
        except BaleToken.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Token not found"}, status=404)

    # ======================
    # 3. درخواست توکن جدید
    # ======================
    existing = BaleToken.objects.filter(
        device_identifier=device_id,
        expiration_date__gt=now
    ).first()

    if existing:
        return JsonResponse({
            "ok": True,
            "token": existing.token,
            "now": now,
            "expires_at": existing.expiration_date,
            "is_new": False
        })

    new_token = secrets.token_urlsafe(48)
    expiration = now + timezone.timedelta(minutes=10)

    BaleToken.objects.create(
        token=new_token,
        device_identifier=device_id,
        expiration_date=expiration
    )

    return JsonResponse({
        "ok": True,
        "token": new_token,
        "now": now,
        "expires_at": expiration,
        "is_new": True
    }, status=201)
