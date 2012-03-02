from distutils.core import setup
import py2exe, pygame
import glob, shutil

shutil.rmtree('dist')

setup(windows=["science.py"], name='Science', version='1.0', author='mrdmnd')

shutil.copytree('maps', 'dist/maps')
shutil.copytree('media', 'dist/media')
shutil.copyfile('freesansbold.ttf', 'dist/freesansbold.ttf')
shutil.rmtree('build')