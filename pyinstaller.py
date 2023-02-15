import PyInstaller.__main__
import shutil
import os

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '-iicon.ico',
    '-n Transcoder',
])
shutil.copyfile('dist/ Transcoder.exe','./Transcoder.exe')
shutil.rmtree('build')
shutil.rmtree('dist')
os.remove(' Transcoder.spec')