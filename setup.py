"""
Flask-Compass
=============

Flask-Compass provides a simple integration of Compass_ into Flask applications
especially to help during the development process.

The extension scans the project's directory for Compass configuration files
in order to compile the associated Compass project.


Note that you need to have compass installed before being able to use this
extension.

Links
-----

* `Documentation <http://packages.python.org/Flask-Compass>`_

.. _compass: http://compass-style.org/

"""
from setuptools import setup

version = '0.2'

setup(
    name='Flask-Compass',
    version=version,
    url='https://github.com/zerok/flask-compass',
    license='BSD',
    author='Horst Gutmann',
    author_email='zerok@zerokspot.com',
    description='Adds automatic Compass compilation to Flask',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
