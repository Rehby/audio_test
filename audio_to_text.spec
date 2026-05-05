# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules, copy_metadata


project_root = Path(SPECPATH)
datas = [
    (str(project_root / "app.py"), "."),
    (str(project_root / "transcriber.py"), "."),
]

models_dir = project_root / "models"
if models_dir.exists():
    datas.append((str(models_dir), "models"))

datas += copy_metadata("streamlit")
datas += copy_metadata("faster-whisper")
datas += copy_metadata("ctranslate2")
datas += copy_metadata("tokenizers")

hiddenimports = []
hiddenimports += collect_submodules("streamlit")
hiddenimports += collect_submodules("faster_whisper")
hiddenimports += collect_submodules("ctranslate2")
hiddenimports += collect_submodules("tokenizers")


a = Analysis(
    [str(project_root / "launcher.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="AudioToText",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)