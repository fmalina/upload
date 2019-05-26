from setuptools import setup, find_packages
import upload

setup(
    name="upload",
    version=upload.__version__,
    description='HTML5 Upload library with django backend and image\
    manipulation tools',
    long_description=open('README.rst').read(),
    license='BSD License',
    platforms=['OS Independent'],
    keywords='upload, photos, files, django, app, crop, gallery',
    author='fmalina',
    author_email='francis@vizualbod.com',
    url="https://github.com/fmalina/upload",
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split(),
)
