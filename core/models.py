from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    full_name = models.CharField(max_length=150, blank=True, verbose_name='Ad Soyad')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Telefon')
    card_number = models.CharField(max_length=25, blank=True, verbose_name='Kart nömrəsi')
    card_expiry = models.CharField(max_length=5, blank=True, verbose_name='Son tarix')
    card_holder = models.CharField(max_length=100, blank=True, verbose_name='Kart sahibi')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'İstifadəçi Profili'
        verbose_name_plural = 'İstifadəçi Profilləri'

    def __str__(self):
        return f'{self.user.username} — profil'

    @property
    def has_bank_card(self):
        return bool(self.card_number)

    @property
    def member_since(self):
        MONTHS_AZ = [
            '', 'Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'İyun',
            'İyul', 'Avqust', 'Sentyabr', 'Oktyabr', 'Noyabr', 'Dekabr'
        ]
        d = self.created_at
        return f'{MONTHS_AZ[d.month]} {d.year}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Complaint(models.Model):
    STATUS_CHOICES = [
        ('reviewing', 'Yoxlanılır'),
        ('confirmed', 'Təsdiqləndi'),
        ('returned', 'Qaytarıldı'),
    ]

    REASON_CHOICES = [
        ('cashier_refused', 'Kassir imtina etdi'),
        ('printer_broken', 'Printer işləmir dedi'),
        ('system_down', 'Sistem çöküb dedi'),
        ('no_receipt', 'Çek yoxdur dedi'),
        ('other', 'Başqa'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='complaints', verbose_name='İstifadəçi')
    shop_name = models.CharField(max_length=200, verbose_name='Mağaza adı')
    district = models.CharField(max_length=100, verbose_name='Rayon')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Məbləğ (₼)')
    date = models.DateField(verbose_name='Tarix')
    reason = models.CharField(max_length=50, choices=REASON_CHOICES, verbose_name='Səbəb')
    description = models.TextField(blank=True, verbose_name='İzahat')
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True, verbose_name='Fayl')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reviewing', verbose_name='Status')
    stars = models.IntegerField(default=4, verbose_name='Reytinq')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Şikayət'
        verbose_name_plural = 'Şikayətlər'

    def __str__(self):
        return f'{self.shop_name} — {self.date}'

    @property
    def vat_amount(self):
        return round(float(self.amount) * 0.18, 2)

    @property
    def stars_range(self):
        return range(self.stars)

    @property
    def empty_stars_range(self):
        return range(5 - self.stars)
