# Ko'p Tillilik (Internationalization) - Qo'llanma

## Qo'shilgan Tillar

Saytda endi 3 til mavjud:
1. **O'zbek tili** (uz) - Asosiy til
2. **Русский язык** (ru) - Rus tili
3. **English** (en) - Ingliz tili

## Foydalanuvchilar Uchun

### Tilni O'zgartirish

1. Sayt yuqori qismidagi navbar'da **Til belgisi** (🌐) ni bosing
2. Ochilgan menyudan kerakli tilni tanlang:
   - O'zbek
   - Русский
   - English
3. Sahifa avtomatik ravishda yangilanadi

### URL Formati

Til URL'da avtomatik ko'rinadi (standart til uchun ko'rinmaydi):
- O'zbek (standart): `http://127.0.0.1:8000/`
- Rus: `http://127.0.0.1:8000/ru/`
- Ingliz: `http://127.0.0.1:8000/en/`

## Admin Panel Uchun

Admin panel ham avtomatik ravishda tanlangan tilda ochiladi:
- O'zbek: `http://127.0.0.1:8000/admin/`
- Rus: `http://127.0.0.1:8000/ru/admin/`
- Ingliz: `http://127.0.0.1:8000/en/admin/`

## Dasturchilar Uchun

### Yangi So'zlarni Tarjima Qilish

Template fayllarida:
```html
{% load i18n %}
<h1>{% trans "Hello World" %}</h1>
```

Python kodda:
```python
from django.utils.translation import gettext_lazy as _

message = _("This is translatable")
```

### Tarjima Fayllarini Yangilash

1. `locale/uz/LC_MESSAGES/django.po` ni tahrirlang
2. `locale/ru/LC_MESSAGES/django.po` ni tahrirlang
3. `locale/en/LC_MESSAGES/django.po` ni tahrirlang

Har bir fayl ichida:
```po
msgid "Hello"
msgstr "Salom"  # O'zbek uchun
msgstr "Привет"  # Rus uchun
msgstr "Hello"   # Ingliz uchun
```

### Tarjimalarni Kompilyatsiya Qilish

```bash
python compile_translations.py
```

yoki gettext o'rnatilgan bo'lsa:
```bash
python manage.py compilemessages
```

## Texnik Ma'lumotlar

### Settings.py da Sozlamalar

```python
LANGUAGE_CODE = 'uz'
LANGUAGES = [
    ('uz', 'O\'zbek'),
    ('ru', 'Русский'),
    ('en', 'English'),
]
LOCALE_PATHS = [BASE_DIR / 'locale']
```

### Middleware

```python
MIDDLEWARE = [
    ...
    'django.middleware.locale.LocaleMiddleware',  # Til uchun
    ...
]
```

## Xususiyatlar

✅ Foydalanuvchi tanlagan til session'da saqlanadi
✅ Admin panel ham tarjima qilinadi
✅ URL'lar til prefixi bilan
✅ Browser tili avtomatik aniqlash
✅ SEO-friendly URL tuzilishi

## Kelajakda Qo'shilishi Mumkin

- 🔄 Mahsulot nomlarini tarjima qilish
- 🔄 Kategoriya nomlarini tarjima qilish
- 🔄 Email xabarlarini tarjima qilish
- 🔄 PDF hujjatlarini tarjima qilish

## Muammolarni Hal Qilish

### Tarjimalar ko'rinmayapti?

1. Serverni qayta ishga tushiring:
   ```bash
   python manage.py runserver
   ```

2. Browser cache'ni tozalang (Ctrl + Shift + Delete)

3. Tarjima fayllarini qayta kompilyatsiya qiling:
   ```bash
   python compile_translations.py
   ```

### Yangi til qo'shish

1. `config/settings.py`da `LANGUAGES` ga qo'shing
2. `locale/TILKODI/LC_MESSAGES/django.po` yarating
3. Tarjimalarni yozing
4. Kompilyatsiya qiling
