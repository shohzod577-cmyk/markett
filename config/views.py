"""
Home view for Market platform.
"""
from django.shortcuts import render, redirect
from django.utils.translation import activate
from django.conf import settings
from django.http import HttpResponseRedirect
from apps.products.models import Product, Category


def home_view(request):
    """
    Home page view with featured products and categories.
    """
    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('category').prefetch_related('images')[:8]

    categories = Category.objects.filter(
        is_active=True,
        parent=None
    )[: 12]


    # Generate star positions in Python
    import random
    stars = []
    for i in range(250):
        size = random.randint(2, 7)
        opacity = round(random.uniform(0.5, 1.0), 2)
        color = random.choice(['#fffbe6', '#fff', '#ffe066', '#fff9c4'])
        blur = random.randint(2, 10)
        twinkle = random.uniform(1.5, 4.5)
        star = {
            'top': random.randint(2, 97),
            'left': random.randint(2, 97),
            'size': size,
            'opacity': opacity,
            'color': color,
            'filter': f'drop-shadow(0 0 {blur}px {color}) brightness(1.7)',
            'twinkle': twinkle,
        }
        stars.append(star)
    context = {
        'featured_products': featured_products,
        'categories': categories,
        'stars': stars,
    }
    return render(request, 'home.html', context)


def custom_404_view(request, exception=None):
    """Custom 404 error page."""
    categories = Category.objects.filter(is_active=True, parent=None)[:8]
    return render(request, '404.html', {'categories': categories}, status=404)


def custom_500_view(request):
    """Custom 500 error page."""
    return render(request, '500.html', status=500)


def custom_403_view(request, exception=None):
    """Custom 403 error page."""
    return render(request, '403.html', status=403)

def about_view(request):
    """About us page."""
    return render(request, 'pages/about.html')


def contact_view(request):
    """Contact us page."""
    return render(request, 'pages/contact.html')


def faq_view(request):
    """FAQ page."""
    return render(request, 'pages/faq.html')


def help_center_view(request):
    """Help center page."""
    return render(request, 'pages/help_center.html')


def shipping_info_view(request):
    """Shipping information page."""
    return render(request, 'pages/shipping.html')


def returns_view(request):
    """Returns and refunds page."""
    return render(request, 'pages/returns.html')


def track_order_view(request):
    """Track order page."""
    return render(request, 'pages/track_order.html')


def careers_view(request):
    """Careers page."""
    return render(request, 'pages/careers.html')


def press_view(request):
    """Press page."""
    return render(request, 'pages/press.html')


def blog_view(request):
    """Blog page with sample posts."""
    posts = [
        {
            'id': 1,
            'title': 'Onlayn xarid qilishda xavfsizlik qoidalari',
            'slug': 'onlayn-xarid-xavfsizlik',
            'excerpt': 'Onlayn savdo-sotiq qilish qulay, lekin xavfsizlikga ham e\'tibor berish kerak. Ushbu maqolada biz sizga onlayn xarid qilishda qanday ehtiyot choralari ko\'rish kerakligini tushuntiramiz...',
            'date': '10 Yanvar 2026',
            'category': 'Maslahat',
            'badge_color': 'primary',
            'image': 'https://via.placeholder.com/800x400',
        },
        {
            'id': 2,
            'title': 'Yangi mahsulot turkumlari qo\'shildi',
            'slug': 'yangi-mahsulot-turkumlari',
            'excerpt': 'Hurmatli mijozlar! Halol Rizq savdo markazida yangi mahsulot turkumlari paydo bo\'ldi. Endi siz yana ko\'proq tanlash imkoniyatiga egasiz...',
            'date': '8 Yanvar 2026',
            'category': 'Yangilik',
            'badge_color': 'success',
            'image': 'https://via.placeholder.com/800x400',
        },
        {
            'id': 3,
            'title': 'Maishiy texnika tanlash bo\'yicha maslahatlar',
            'slug': 'maishiy-texnika-tanlash',
            'excerpt': 'Maishiy texnika xarid qilishda nimalarga e\'tibor berish kerak? Ushbu maqolada biz sizga foydali maslahatlar beramiz...',
            'date': '5 Yanvar 2026',
            'category': 'Qo\'llanma',
            'badge_color': 'warning',
            'image': 'https://via.placeholder.com/800x400',
        },
    ]
    return render(request, 'pages/blog.html', {'posts': posts})


def blog_detail_view(request, slug):
    """Blog post detail page."""
    posts_data = {
        'onlayn-xarid-xavfsizlik': {
            'title': 'Onlayn xarid qilishda xavfsizlik qoidalari',
            'slug': 'onlayn-xarid-xavfsizlik',
            'date': '10 Yanvar 2026',
            'category': 'Maslahat',
            'badge_color': 'primary',
            'image': 'https://via.placeholder.com/800x400',
            'read_time': '5',
            'views': '1,234',
            'tags': ['xavfsizlik', 'onlayn xarid', 'maslahat', 'to\'lov'],
            'content': '''
                <h2>Onlayn xarid qilish - qulay va xavfsiz</h2>
                <p>Zamonaviy dunyoda onlayn xarid qilish tobora ommalashib bormoqda. Bu juda qulay, vaqt tejaydi va keng tanlovni taqdim etadi. Ammo, xavfsizlikka ham e'tibor berish kerak.</p>
                
                <h2>Asosiy xavfsizlik qoidalari</h2>
                <p><strong>1. Ishonchli saytlardan xarid qiling</strong></p>
                <p>Faqat taniqli va ishonchli onlayn do'konlardan xarid qiling. Saytning SSL sertifikati borligini tekshiring (manzil qatorida qulf belgisi).</p>
                
                <p><strong>2. Kuchli parol ishlatang</strong></p>
                <p>Har bir sayt uchun alohida va murakkab parol yarating. Parol menejeri dasturlaridan foydalanish tavsiya etiladi.</p>
                
                <p><strong>3. Umumiy Wi-Fi tarmoqlarida ehtiyot bo'ling</strong></p>
                <p>Umumiy Wi-Fi orqali onlayn xarid qilishdan saqlaning. Agar zarurat tug'ilsa, VPN ishlatishni unutmang.</p>
                
                <p><strong>4. Karta ma'lumotlarini saqlamang</strong></p>
                <p>Agar sayt karta ma'lumotlaringizni saqlashni taklif qilsa, ehtiyot bo'ling. Har safar qo'lda kiritish xavfsizroq.</p>
                
                <p><strong>5. To'lov tarixini kuzatib boring</strong></p>
                <p>Bank hisobingizni muntazam tekshiring va shubhali operatsiyalarni darhol bank xodimlariga xabar qiling.</p>
                
                <h2>Halol Rizq savdo markazida xavfsizlik</h2>
                <p>Biz mijozlarimizning xavfsizligini birinchi o'ringa qo'yamiz:</p>
                <ul>
                    <li>256-bit SSL shifrlash</li>
                    <li>Xavfsiz to'lov tizimlari (Payme, Click, Uzum)</li>
                    <li>Ma'lumotlar maxfiyligi kafolati</li>
                    <li>24/7 texnik yordam</li>
                </ul>
                
                <blockquote>
                "Xavfsizlik - bizning ustuvor vazifamiz. Har bir mijozning ishonchini qadrlaymiz va himoyalaymiz."
                </blockquote>
                
                <h2>Xulosa</h2>
                <p>Onlayn xarid qilish xavfsiz bo'lishi uchun oddiy qoidalarga amal qilish kifoya. Halol Rizq savdo markazi sizning xavfsizligingiz uchun barcha zamonaviy texnologiyalardan foydalanadi.</p>
                
                <p>Xarid qilishdan zavq oling va xavfsiz bo'ling! 🛡️</p>
            '''
        },
        'yangi-mahsulot-turkumlari': {
            'title': 'Yangi mahsulot turkumlari qo\'shildi',
            'slug': 'yangi-mahsulot-turkumlari',
            'date': '8 Yanvar 2026',
            'category': 'Yangilik',
            'badge_color': 'success',
            'image': 'https://via.placeholder.com/800x400',
            'read_time': '3',
            'views': '2,156',
            'tags': ['yangilik', 'mahsulotlar', 'katalog'],
            'content': '''
                <h2>Yangi mahsulotlar bilan tanishing!</h2>
                <p>Hurmatli mijozlar! Halol Rizq savdo markazida yangi mahsulot turkumlari paydo bo'ldi. Endi siz yana ko'proq tanlash imkoniyatiga egasiz.</p>
                
                <h2>Qo'shilgan turkumlar</h2>
                <ul>
                    <li><strong>Aqlli uy jihozlari</strong> - zamonaviy aqlli uy texnologiyalari</li>
                    <li><strong>Sport va fitnes</strong> - salomatlik uchun mahsulotlar</li>
                    <li><strong>Bolalar o'yinchoqlari</strong> - xavfsiz va sifatli o'yinchoqlar</li>
                    <li><strong>Kitoblar</strong> - turli xil adabiyotlar</li>
                </ul>
                
                <h2>Maxsus takliflar</h2>
                <p>Yangi turkumlar bo'yicha maxsus chegirmalar!</p>
                <ul>
                    <li>Birinchi xaridda 15% chegirma</li>
                    <li>Bepul yetkazib berish</li>
                    <li>Sovg'alar va bonuslar</li>
                </ul>
                
                <p>Yangi mahsulotlar bilan tanishish uchun katalogni ko'rib chiqing! 🎁</p>
            '''
        },
        'maishiy-texnika-tanlash': {
            'title': 'Maishiy texnika tanlash bo\'yicha maslahatlar',
            'slug': 'maishiy-texnika-tanlash',
            'date': '5 Yanvar 2026',
            'category': 'Qo\'llanma',
            'badge_color': 'warning',
            'image': 'https://via.placeholder.com/800x400',
            'read_time': '7',
            'views': '3,421',
            'tags': ['maishiy texnika', 'maslahat', 'qo\'llanma', 'tanlash'],
            'content': '''
                <h2>To'g'ri maishiy texnika qanday tanlanadi?</h2>
                <p>Maishiy texnika xarid qilishda nimalarga e'tibor berish kerak? Ushbu maqolada biz sizga foydali maslahatlar beramiz.</p>
                
                <h2>Asosiy mezonlar</h2>
                
                <p><strong>1. Energiya tejamkorligi</strong></p>
                <p>A+++ yoki A++ energiya sinfi bo'lgan texnikani tanlang. Bu elektr energiyasidan tejashga yordam beradi.</p>
                
                <p><strong>2. Brend va kafolat</strong></p>
                <p>Taniqli brendlarni afzal ko'ring va kafolat muddatiga e'tibor bering. Halol Rizq barcha mahsulotlarga rasmiy kafolat beradi.</p>
                
                <p><strong>3. Funksiyalar</strong></p>
                <p>Kerakli funksiyalarni oldindan aniqlang. Ortiqcha funksiyalar uchun to'lash shart emas.</p>
                
                <p><strong>4. O'lchami va sig'imi</strong></p>
                <p>Uyingiz va oilangiz hajmiga mos keluvchi o'lchamni tanlang.</p>
                
                <p><strong>5. Narx va sifat nisbati</strong></p>
                <p>Eng arzon variant har doim yaxshi emas. Sifat va narx muvozanatini toping.</p>
                
                <h2>Mashhur mahsulotlar</h2>
                <ul>
                    <li>Muzlatgichlar - Samsung, LG, Artel</li>
                    <li>Kir yuvish mashinalari - Bosch, Indesit, Beko</li>
                    <li>Mikroto'lqinli pechlar - Panasonic, Samsung</li>
                    <li>Changyutgichlar - Philips, Dyson, Xiaomi</li>
                </ul>
                
                <blockquote>
                "To'g'ri tanlov - uzoq yillik xizmat kafolati"
                </blockquote>
                
                <h2>Xulosa</h2>
                <p>Maishiy texnika tanlashda shoshilmang, barcha xususiyatlarni sinchiklab o'rganing va Halol Rizq mutaxassislari bilan maslahatlashing!</p>
                
                <p>Sifatli xarid qiling! 🏠✨</p>
            '''
        },
    }
    
    post = posts_data.get(slug)
    if not post:
        from django.http import Http404
        raise Http404("Blog post topilmadi")
    
    return render(request, 'pages/blog_detail.html', {'post': post})

def custom_400_view(request, exception=None):
    """Custom 400 error page."""
    return render(request, '400.html', status=400)


def set_language_view(request):
    """
    Custom language switching view with proper session handling.
    """
    if request.method == 'POST':
        language = request.POST.get('language')
        next_url = request.POST.get('next', '/')
        
        if language and language in dict(settings.LANGUAGES):
            activate(language)
            
            request.session['_language'] = language
            
            import re
            
            clean_path = re.sub(r'^/(uz|ru|en)(/|$)', '/', next_url)
            if clean_path == '//':
                clean_path = '/'
            
            new_url = f'/{language}{clean_path}' if clean_path != '/' else f'/{language}/'
            
            response = HttpResponseRedirect(new_url)
            
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                language,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )
            
            return response
    
    return redirect('home')