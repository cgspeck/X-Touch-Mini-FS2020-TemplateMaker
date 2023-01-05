# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['template_maker\\main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('resources', 'resources'),
        ('build_tag', '.'),
        ('README.md', '.'),
        ('LICENSE', '.'),
        ('tests\data\config_generic_ap.json', 'examples'),
        ('scratch\config_generic_ap.svg', 'examples'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
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
    name='Xtouch Template Maker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
    version='versionfile.txt',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='xtouch-template-maker',
)
