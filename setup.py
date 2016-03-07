# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages
import upload as app

setup(
    name="upload",
    version=app.__version__,
    description='HTML5 Upload library with django backend and image manipulation tools',
    long_description=open('README.rst').read(),
    license='BSD License',
    platforms=['OS Independent'],
    keywords='django, app, upload, photos, files, crop, gallery',
    author='fmalina',
    author_email='fmalina@gmail.com',
    url="https://github.com/fmalina/uploads",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split(),
)
