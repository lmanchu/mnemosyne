# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\lmanwindows\\Dropbox\\Dev\\mnemosyne\\app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\lmanwindows\\Dropbox\\Dev\\mnemosyne\\dashboard.html', '.'), ('C:\\Users\\lmanwindows\\Dropbox\\Dev\\mnemosyne\\onboarding.html', '.'), ('C:\\Users\\lmanwindows\\Dropbox\\Dev\\mnemosyne\\persona-editor.html', '.')],
    hiddenimports=['mss', 'mss.windows', 'PIL', 'PIL.Image', 'mcp', 'mcp.server', 'mcp.server.fastmcp', 'api', 'capture', 'daemon', 'mcp_server', 'persona', 'pipeline', 'provider_gemini', 'storage'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='mnemosyne',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='mnemosyne',
)
