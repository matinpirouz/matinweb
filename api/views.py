from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from account.models import BaleToken
import secrets

@csrf_exempt
@require_POST
def register_view(request):
    # پاک‌سازی توکن‌های منقضی‌شده
    BaleToken.objects.filter(expiration_date__lt=timezone.now()).delete()

    # شناسایی دستگاه از IP
    device_ip = get_client_ip(request)
    now = timezone.now()

    token = request.POST.get("token")
    user_id = request.POST.get("user_id")
    phone_number = request.POST.get("phone_number")
    first_name = request.POST.get("first_name")

    # اگر توکن و user_id ارسال شد → آپدیت رکورد
    if token and user_id:
        try:
            bale_token = BaleToken.objects.get(token=token)
            bale_token.bale_id = user_id
            bale_token.first_name = first_name
            if phone_number:
                bale_token.phone_number = phone_number
            bale_token.save()
            return JsonResponse({"ok": True, "message": "User ID updated successfully"})
        except BaleToken.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Token not found"}, status=404)

    # اگر فقط توکن ارسال شد → اطلاعات موجود را برگردان
    if token and not user_id:
        try:
            bale_token = BaleToken.objects.get(token=token)
            return JsonResponse({
                "ok": True,
                "user_id": bale_token.bale_id,
                "first_name": bale_token.first_name,
                "phone_number": bale_token.phone_number,
                "token": bale_token.token,
                "now": now,
                "expires_at": bale_token.expiration_date
            })
        except BaleToken.DoesNotExist:
            return JsonResponse({"ok": False, "error": "Token not found"}, status=404)

    # حالت پیش‌فرض: درخواست جدید برای توکن
    existing_token = BaleToken.objects.filter(
        device_identifier=device_ip,
        expiration_date__gt=now
    ).first()

    if existing_token:
        return JsonResponse(
            {
                "ok": True,
                "token": existing_token.token,
                "now": now,
                "expires_at": existing_token.expiration_date,
                "is_new": False
            },
            status=200
        )

    # ساخت توکن جدید
    new_token = secrets.token_urlsafe(64)
    expiration = now + timezone.timedelta(minutes=10)
    bale_token = BaleToken.objects.create(
        token=new_token,
        expiration_date=expiration,
        device_identifier=device_ip
    )

    return JsonResponse(
        {
            "ok": True,
            "token": bale_token.token,
            "now": now,
            "expires_at": bale_token.expiration_date,
            "is_new": True
        },
        status=201
    )


def get_client_ip(request):
    """دریافت IP کاربر"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
