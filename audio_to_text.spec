# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_metadata

block_cipher = None

# Collect package metadata so importlib.metadata.version() works at runtime
datas = []
try:
    datas += collect_metadata('streamlit')
except Exception:
    # If collect_metadata fails at spec-eval time, fall back to an empty list
    datas += []

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=['transcriber', 'preload_models'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='audio_to_text',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='audio_to_text',
)
