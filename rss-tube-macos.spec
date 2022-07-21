# -*- mode: python -*-

block_cipher = None

a = Analysis(['rss_tube/__main__.py'],
             pathex=[os.getcwd()],
             binaries=[],
             datas=[('rss_tube/gui/themes', 'rss_tube/gui/themes'), ('version.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='rsstube',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          version='version.py',
          icon='logo.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='rsstube')
app = BUNDLE(coll,
             name='RSSTube.app',
             icon='logo.ico',
             bundle_identifier=None)
