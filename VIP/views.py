from django.shortcuts import render, redirect
from django.http import FileResponse
from django.core.exceptions import PermissionDenied
from .create_invoice import create_invoice_pdf
import json
from decouple import config, Csv
import requests
from django.apps import apps
from django.contrib import messages


BaleAccount = apps.get_model('account', 'BaleAccount')


    
url_send_invoice = f'https://tapi.bale.ai/bot{config("BALE_HOLOO_TEFLON_BOT_TOKEN")}/sendDocument'

def is_vip(user):
    return user.is_authenticated and user.groups.filter(name="VIP").exists()

def create_invoice(request):
    if not is_vip(request.user):
        raise PermissionDenied
    if request.method == 'POST':
        download_pdf = 'download_pdf' in request.POST
        shop_name = request.POST.get("shop_name")
        invoice_type = request.POST.get("invoice_type")
        shop_phone_number = request.POST.get("shop_phone_number")
        invoice_number = request.POST.get("invoice_number") or ""
        customer_name = request.POST.get("customer_name")
        date = request.POST.get("date")
        items = json.loads(request.POST.get("items"))
        discription = request.POST.get("discription")
        discount = int(request.POST.get("discount", 0)) if request.POST.get("discount") != '' else 0
        previous_debt = int(request.POST.get("previous_debt", 0)) if request.POST.get("previous_debt") != '' else 0
        
        invoice = create_invoice_pdf(
            shop_name=shop_name,
            invoice_type=invoice_type,
            shop_phone_number=shop_phone_number,
            invoice_number=invoice_number,
            customer_name=customer_name,
            date=date,
            items=items,
            discription=discription,
            discount=discount,
            previous_debt=previous_debt,
            filename=f"invoice{invoice_number}.pdf"
        )
        
        files = {'document': (f"invoice{invoice_number}.pdf", invoice, 'application/pdf')}


        try:
            data = {
                'chat_id': BaleAccount.objects.filter(user=request.user).first().bale_id
            }
        except Exception as e:
            print(e)

        try:
            response = requests.post(url_send_invoice, data=data, files=files, timeout=10)
            if response.ok:
                messages.success(request, "فاکتور با موفقیت ساخته و در بله برای شما ارسال شد.")
            else:
                messages.success(request, "فاکتور با موفقیت ساخته شد.")
                messages.error(request, "خطایی در ارسال فاکتور در بله برای شما به وجود آمد به همین دلیل فاکتور دانلود شد.")
                return FileResponse(invoice, as_attachment=False, filename=f"invoice{invoice_number}.pdf")
        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, "خطایی در ارسال فاکتور در بله برای شما به وجود آمد به همین دلیل فاکتور دانلود شد.")
            return FileResponse(invoice, as_attachment=False, filename=f"invoice{invoice_number}.pdf")
        if download_pdf:
            invoice.seek(0)
            return FileResponse(invoice, as_attachment=False, filename=f"invoice{invoice_number}.pdf")
        return redirect(request.path)

    return render(request, 'VIP/create_invoice.html')

