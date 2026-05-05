# -*- mode: python ; coding: utf-8 -*-

try:
    # Newer PyInstaller exposes a helper named `copy_metadata`.
    from PyInstaller.utils.hooks import copy_metadata as collect_metadata
except Exception:
    try:
        # Older versions may provide `collect_metadata` directly.
        from PyInstaller.utils.hooks import collect_metadata
    except Exception:
        collect_metadata = None

block_cipher = None

# Collect package metadata so importlib.metadata.version() works at runtime
datas = []
if collect_metadata is not None:
    try:
        datas += collect_metadata('streamlit')
    except Exception:
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
