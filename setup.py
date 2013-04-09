from setuptools import setup

setup(
    name='locator',
    version='1.0',
    author='Piotr Kopalko',
    packages=['locator'],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'jinja2==2.6',
        'werkzeug==0.8.3',
        'flask==0.9',
        'flask-script==0.5.3',
        'flatland',
        'psycopg2==2.4.6',
        'flask-login==0.1.3',
        'sqlalchemy==0.8',
        'flask-sqlalchemy==0.16',
        'geoalchemy==0.7.1',
        'xlrd==0.9.0',
        'mysql-python==1.2.4',
        'distribute==0.6.28'
    ],
)
