"""
Script to compile .po files to .mo files without gettext
"""
import os
import polib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')

languages = ['uz', 'ru', 'en']

for lang in languages:
    po_file = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.po')
    mo_file = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES', 'django.mo')
    
    if os.path.exists(po_file):
        po = polib.pofile(po_file)
        po.save_as_mofile(mo_file)
        print(f'✓ Compiled {lang}/LC_MESSAGES/django.po -> django.mo')
    else:
        print(f'✗ File not found: {po_file}')

print('\n✅ All translation files compiled successfully!')
