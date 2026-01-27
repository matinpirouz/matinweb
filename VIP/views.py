from django.shortcuts import render, redirect
from .create_invoice import create_invoice_pdf
import json
from decouple import config, Csv
import requests

url_send_invoice = f'https://tapi.bale.ai/bot{config("BALE_HOLOO_TEFLON_BOT_TOKEN")}/sendDocument'

def create_invoice(request):
    if request.user.is_staff:
        if request.method == 'POST':
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
            try:
                payload = {
                    'chat_id': 1687820101,
                    'document': f"{config('SITE_URL')}invoice{invoice_number}.pdf",
                    'caption': f"فاکتور {invoice_number}"
                }
                requests.post(url_send_invoice, data=payload, timeout=10)
            except Exception as e:
                print(e)
            return redirect(f'/media/invoice{invoice_number}.pdf')
        else:
            
            return render(request, 'VIP/create_invoice.html')

    else:
        return render(request, 'errors/403.html', status=403)
