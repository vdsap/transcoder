import PyInstaller.__main__
import shutil
import os
from loguru import logger

logger.info('Compiling started')
try:
    os.remove('Transcoder.zip')
    logger.info('zip deleted')
except:
    print('Previous file not found')
PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '-iicon.ico',
    '-n Transcoder',
])
logger.info('Compiling finished')
shutil.copyfile('dist/ Transcoder.exe', './Transcoder.exe')
logger.info('Copying finished')
shutil.rmtree('build')
logger.info('Removing build folder')
shutil.rmtree('dist')
logger.info('Removing dist folder')
os.remove(' Transcoder.spec')
logger.info('Removing spec file')
try:
    os.mkdir('release')
    os.mkdir('release/Transcoder')
except:
    pass
logger.info('Created release directory')
shutil.copyfile('Transcoder.exe', 'release/Transcoder/Transcoder.exe')
logger.info('Transcoder.exe copied')
shutil.copyfile('ffmpeg.exe', 'release/Transcoder/ffmpeg.exe')
logger.info('Ffmpeg.exe copied')
logger.info('Creating zip')
shutil.make_archive('Transcoder', 'zip', 'release')
logger.info('Archive made')
shutil.rmtree('release')
logger.info('Release directory removed')
logger.info('Compiling complete')
