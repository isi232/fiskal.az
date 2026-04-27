from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Complaint, UserProfile
from .forms import RegisterForm


DISTRICTS = [
    'Nərimanov', 'Nəsimi', 'Yasamal', 'Sabunçu',
    'Suraxanı', 'Binəqədi', 'Xəzər', 'Nizami',
]


# ===== AUTH =====

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
        )
        profile = user.userprofile
        profile.full_name = form.cleaned_data['full_name']
        profile.phone = form.cleaned_data.get('phone', '')
        profile.save()
        login(request, user)
        messages.success(request, 'Qeydiyyat uğurla tamamlandı!')
        return redirect('home')

    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır.')

    from django.contrib.auth.forms import AuthenticationForm
    form = AuthenticationForm(request, data=request.POST or None)
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('login')


# ===== MAIN VIEWS =====

@login_required
def home(request):
    complaints = Complaint.objects.filter(user=request.user)
    total = complaints.count()
    confirmed = complaints.filter(status__in=['confirmed', 'returned']).count()
    returned_qs = complaints.filter(status='returned')
    refunded = round(sum(c.vat_amount for c in returned_qs), 2)
    context = {
        'complaints': complaints,
        'stats': {
            'total': total,
            'confirmed': confirmed,
            'refunded': refunded,
        },
    }
    return render(request, 'core/home.html', context)


@login_required
def complaint_view(request):
    if request.method == 'POST':
        shop_name = request.POST.get('shop_name', '').strip()
        amount = request.POST.get('amount', '').strip()
        district = request.POST.get('district', '').strip()
        date = request.POST.get('date', '').strip()
        reason = request.POST.get('reason', '').strip()
        description = request.POST.get('description', '').strip()
        attachment = request.FILES.get('attachment')

        if not shop_name or not amount:
            messages.error(request, 'Mağaza adı və məbləği mütləq daxil edilməlidir.')
            return render(request, 'core/complaint.html', {
                'districts': DISTRICTS,
                'form_data': request.POST,
            })

        try:
            amount_val = float(amount)
            if amount_val <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, 'Məbləğ düzgün daxil edilməyib.')
            return render(request, 'core/complaint.html', {
                'districts': DISTRICTS,
                'form_data': request.POST,
            })

        Complaint.objects.create(
            user=request.user,
            shop_name=shop_name,
            amount=amount_val,
            district=district,
            date=date or None,
            reason=reason,
            description=description,
            attachment=attachment,
            status='reviewing',
        )
        messages.success(request, 'success')
        return redirect('complaint')

    return render(request, 'core/complaint.html', {'districts': DISTRICTS})


@login_required
def analytics(request):
    all_complaints = Complaint.objects.all()
    user_complaints = Complaint.objects.filter(user=request.user)

    shop_counts = (
        all_complaints.values('shop_name')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )
    max_count = shop_counts[0]['count'] if shop_counts else 1
    top_shops = [
        {
            'name': s['shop_name'],
            'complaint_count': s['count'],
            'risk_pct': min(round((s['count'] / max_count) * 100), 100),
        }
        for s in shop_counts
    ]

    total_count = user_complaints.count()
    confirmed_count = user_complaints.filter(status__in=['confirmed', 'returned']).count()
    returned_qs = user_complaints.filter(status='returned')
    total_refunded = round(sum(c.vat_amount for c in returned_qs), 2)

    context = {
        'top_shops': top_shops,
        'chart_data': [42, 58, 35, 71, 89, 64, all_complaints.count() or 95],
        'total_count': total_count,
        'confirmed_count': confirmed_count,
        'total_refunded': total_refunded,
    }
    return render(request, 'core/analytics.html', context)


@login_required
def map_view(request):
    district_data = (
        Complaint.objects.values('district')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    max_count = district_data[0]['count'] if district_data else 1
    districts = [
        {
            'name': d['district'],
            'complaint_count': d['count'],
            'bar_pct': min(round((d['count'] / max_count) * 100), 100),
        }
        for d in district_data
    ]
    return render(request, 'core/map.html', {'districts': districts})


@login_required
def profile(request):
    complaints = Complaint.objects.filter(user=request.user)
    returned_qs = complaints.filter(status='returned')
    refunded = round(sum(c.vat_amount for c in returned_qs), 2)
    activity = [
        {
            'shop_name': c.shop_name,
            'date': c.date,
            'status': c.status,
            'status_label': c.get_status_display(),
            'vat_amount': c.vat_amount,
        }
        for c in complaints[:5]
    ]
    user_profile = request.user.userprofile
    context = {
        'profile': {
            'full_name': user_profile.full_name or request.user.username,
            'phone': user_profile.phone,
            'member_since': user_profile.member_since,
        },
        'stats': {
            'total': complaints.count(),
            'confirmed': complaints.filter(status__in=['confirmed', 'returned']).count(),
            'refunded': refunded,
        },
        'activity': activity,
    }
    return render(request, 'core/profile.html', context)


@login_required
def add_card(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number', '').replace(' ', '')
        card_expiry = request.POST.get('card_expiry', '').strip()
        card_holder = request.POST.get('card_holder', '').strip().upper()

        if len(card_number) < 16 or not card_expiry or not card_holder:
            messages.error(request, 'Bütün kart məlumatlarını düzgün daxil edin.')
            return render(request, 'core/add_card.html')

        profile = request.user.userprofile
        masked = '**** **** **** ' + card_number[-4:]
        profile.card_number = masked
        profile.card_expiry = card_expiry
        profile.card_holder = card_holder
        profile.save()

        messages.success(request, 'Bank kartı uğurla əlavə edildi!')
        return redirect('profile')

    return render(request, 'core/add_card.html')
