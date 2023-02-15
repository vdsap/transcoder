import PyInstaller.__main__
import shutil
import os
from loguru import logger

logger.info('Compilling started')
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '-iicon.ico',
    '-n Transcoder',
])
logger.info('Compilling finished')
shutil.copyfile('dist/ Transcoder.exe','./Transcoder.exe')
logger.info('Copying finished')
shutil.rmtree('build')
logger.info('Removing build folder')
shutil.rmtree('dist')
logger.info('Removing dist folder')
os.remove(' Transcoder.spec')
logger.info('Removing spec file')