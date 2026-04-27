## Layihə Strukturu

```
fiskal_new/
├── manage.py
├── db.sqlite3              ← avtomatik yaranır
│
├── fiskal/                 ← layihə konfiqurasiyası
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── core/                   ← əsas app
    ├── models.py           ← Complaint + UserProfile
    ├── views.py            ← bütün viewlar
    ├── urls.py             ← URL marşrutlaşdırması
    ├── forms.py            ← qeydiyyat forması
    ├── admin.py            ← admin panel
    ├── apps.py
    ├── migrations/
    │   └── 0001_initial.py
    ├── static/core/
    │   ├── css/
    │   │   └── main.css    ← bütün stillər burada
    │   └── js/
    │       └── main.js     ← bütün JavaScript burada
    └── templates/
        ├── registration/
        │   └── login.html  ← giriş səhifəsi
        └── core/
            ├── base.html   ← əsas şablon
            ├── register.html
            ├── home.html
            ├── complaint.html
            ├── analytics.html
            ├── map.html
            ├── profile.html
            └── add_card.html
```

---

## URL-lər

| URL | Səhifə |
|-----|--------|
| `/` | Ana səhifə (login tələb edir) |
| `/giris/` | Giriş |
| `/qeydiyyat/` | Qeydiyyat |
| `/cixis/` | Çıxış (POST) |
| `/sikayet/` | Şikayət əlavə et |
| `/analitika/` | Statistika |
| `/xerite/` | Rayon xəritəsi |
| `/profil/` | Profil |
| `/kart-elave-et/` | Bank kartı |
| `/admin/` | Admin panel |

---

## Funksionallıq

### Hər düymə işləyir:
- **Axtar** — şikayət kartlarını axtarır, nəticə göstərir
- **Kart əlavə et** (banner) — modal açır, kart saxlayır
- **Bildirişlər** — ayarlar modalı
- **Dil** — dil seçimi modalı
- **Dəstək** — əlaqə modalı
- **Məxfilik** — siyasət modalı
- **Çıxış** — hesabdan çıxır
- **Tab keçidi** — kartları filtrləyir
- **Fayl yükləmə** — drag&drop + klik dəstəkli
- **Şikayət göndər** — DB-ə yazır, uğur mesajı göstərir
- **Mövzu dəyiş** (🌙/☀️) — qaranlıq/aydın rejim saxlanır

### Giriş/Qeydiyyat:
- Qeydiyyat zamanı UserProfile avtomatik yaranır
- Şifrə validasiyası (min 6 simvol, uyğunluq)
- İstifadəçi adının unikallığı yoxlanır
- Login olmayan istifadəçilər `/giris/`-ə yönləndirilir

### Database:
- SQLite (dəyişdirmək lazım deyil)
- `UserProfile`: ad, telefon, bank kartı
- `Complaint`: şikayət, istifadəçiyə bağlı, status, ƏDV hesabı
