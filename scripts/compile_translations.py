"""Compile .po files to .mo using polib"""
import polib
from pathlib import Path

locale_dir = Path(__file__).parent.parent / 'locale'

for lang_dir in locale_dir.iterdir():
    if lang_dir.is_dir():
        po_file = lang_dir / 'LC_MESSAGES' / 'django.po'
        mo_file = lang_dir / 'LC_MESSAGES' / 'django.mo'
        
        if po_file.exists():
            print(f"Compiling {po_file}...")
            try:
                po = polib.pofile(str(po_file))
                po.save_as_mofile(str(mo_file))
                print(f"✓ Created {mo_file}")
            except Exception as e:
                print(f"✗ Error: {e}")

print("\nDone! Restart the server to apply translations.")
