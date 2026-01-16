from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from .models import BaleAccount, BaleToken
from django.utils import timezone

def register_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        if request.method == 'POST':
            now = timezone.now()
            form = UserCreationForm(request.POST)
            if form.is_valid():
                token = request.POST.get('token')
                device_id = request.POST.get("device_id")

                bale_id = request.POST.get('bale_id')
                phone_number = request.POST.get('phone_number')
                try:
                    bale_token = BaleToken.objects.get(
                        token=token,
                        device_identifier=device_id,
                        expiration_date__gt=now
                    )

                except BaleToken.DoesNotExist:
                    messages.error(request, "توکن نامعتبر یا منقضی شده است. لطفا مجددا تلاش کنید.")
                else:
                    username = request.POST.get("username")
                    if bale_id == bale_token.bale_id and phone_number == bale_token.phone_number and device_id == bale_token.device_identifier and username == bale_token.phone_number:
                        user = form.save()
                        user.first_name = request.POST.get("first_name")
                        user.last_name = request.POST.get("last_name")
                        user.save()
                        bale_account = BaleAccount.objects.create(
                            user=user,
                            bale_id=bale_id,
                            phone_number=phone_number,
                        )
                        messages.success(request, "ثبت نام شما با موفقیت انجام شد. لطفا وارد شوید.")
                        return redirect('account:login')
                    else:
                        messages.error(request, f"خطایی به وجود آمد.")
            else:
                for field, error in form.errors.items():
                    if "A user with that username already exists." in error:
                        messages.error(request, "این شماره موبایل قبلاً ثبت شده است. لطفا وارد شوید.")
                        return redirect('account:login')
                    elif "The two password fields didn’t match." in error:
                        messages.error(request, "رمز عبور و تایید رمز عبور مطابقت ندارد.")
                    else:
                        messages.error(request, error)

        else:
            form = UserCreationForm()
                
        return render(request, 'account/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('main:home')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "ورود به متین وب با موفقیت انجام شد.")
                    return redirect('main:home')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        if "Please enter a correct username and password" in error:
                            messages.error(request, "شماره موبایل یا رمز عبور اشتباه است.")
                        else:
                            messages.error(request, error)
        else:
            form = AuthenticationForm()
    
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    if request.user.is_authenticated:    
        logout(request)
        messages.success(request, "خروج از متین وب با موفقیت انجام شد.")
    return redirect('main:home')