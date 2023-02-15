import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '-i Q075.ico',
    '-n Transcoder',
])