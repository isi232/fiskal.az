from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=150, verbose_name='Ad Soyad')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Telefon')),
                ('card_number', models.CharField(blank=True, max_length=25, verbose_name='Kart nömrəsi')),
                ('card_expiry', models.CharField(blank=True, max_length=5, verbose_name='Son tarix')),
                ('card_holder', models.CharField(blank=True, max_length=100, verbose_name='Kart sahibi')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='userprofile',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'İstifadəçi Profili',
                'verbose_name_plural': 'İstifadəçi Profilləri',
            },
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_name', models.CharField(max_length=200, verbose_name='Mağaza adı')),
                ('district', models.CharField(max_length=100, verbose_name='Rayon')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Məbləğ (₼)')),
                ('date', models.DateField(verbose_name='Tarix')),
                ('reason', models.CharField(
                    choices=[
                        ('cashier_refused', 'Kassir imtina etdi'),
                        ('printer_broken', 'Printer işləmir dedi'),
                        ('system_down', 'Sistem çöküb dedi'),
                        ('no_receipt', 'Çek yoxdur dedi'),
                        ('other', 'Başqa'),
                    ],
                    max_length=50,
                    verbose_name='Səbəb',
                )),
                ('description', models.TextField(blank=True, verbose_name='İzahat')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments/', verbose_name='Fayl')),
                ('status', models.CharField(
                    choices=[
                        ('reviewing', 'Yoxlanılır'),
                        ('confirmed', 'Təsdiqləndi'),
                        ('returned', 'Qaytarıldı'),
                    ],
                    default='reviewing',
                    max_length=20,
                    verbose_name='Status',
                )),
                ('stars', models.IntegerField(default=4, verbose_name='Reytinq')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='complaints',
                    to=settings.AUTH_USER_MODEL,
                    verbose_name='İstifadəçi',
                )),
            ],
            options={
                'verbose_name': 'Şikayət',
                'verbose_name_plural': 'Şikayətlər',
                'ordering': ['-created_at'],
            },
        ),
    ]
