#!/usr/bin/env python3
import setuptools

setuptools.setup(
    name='ToodleDoodle',
    version='1.0',
    description='Planning tool',
    scripts=[
        'init_db.py',
        'flask',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-WTF',
        'WTForms',
        'psycopg2-binary'
    ],
)
