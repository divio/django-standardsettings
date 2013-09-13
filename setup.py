# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='django-standardsettings',
    version=__import__('standardsettings').__version__,
    description='standardised dotenv based settings for common deployments',
    long_description=readme,
    author='Stefan Foulis',
    author_email='stefan@foulis.ch',
    url='https://github.com/divio/django-standardsettings',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'django-dotenv',
        'django-getenv',
        'dj-database-url',
        'dj-email-url',
    ]
)