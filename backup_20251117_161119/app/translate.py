import os
import shutil
import polib
import click
from flask.cli import AppGroup
from app.my_translate import translate  # Google Translate wrapper

translate_cli = AppGroup('translate')

@translate_cli.command('init')
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system(f'pybabel extract -F babel.cfg -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(f'pybabel init -i messages.pot -d app/translations -l {lang}'):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')

@translate_cli.command('update')
def update():
    """Update all languages."""
    if os.system(f'pybabel extract -F babel.cfg -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(f'pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate_cli.command('compile')
def compile():
    """Compile all languages."""
    if os.system(f'pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

@translate_cli.command('autofill')
@click.argument('lang')
@click.option('--src', default='en', help='Source language (default: en)')
def autofill(lang, src):
    """Auto-fill .po file for a given language using Google Translate."""
    po_path = f'app/translations/{lang}/LC_MESSAGES/messages.po'
    if not os.path.exists(po_path):
        print(f"Error: File not found → {po_path}")
        return

    backup_path = po_path + '.bak'
    shutil.copy(po_path, backup_path)
    print(f"Backup saved to {backup_path}")

    po = polib.pofile(po_path)
    updated = False

    for entry in po.untranslated_entries():
        if entry.msgid.strip():
            translated_text = translate(entry.msgid, src, lang)
            entry.msgstr = translated_text
            updated = True
            print(f'Translated: "{entry.msgid}" → "{translated_text}"')

    if updated:
        po.save(po_path)
        print(f'Updated .po file saved to {po_path}')
    else:
        print('No untranslated entries found.')

def register(app):
    app.cli.add_command(translate_cli)