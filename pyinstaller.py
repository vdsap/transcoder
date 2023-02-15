import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '-iicon.ico',
    '-n Transcoder',
])