from setuptools import setup

setup(
    name='zWayRest',
    version='0.1',
    long_description=__doc__,
    packages=['zwayrest'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-RESTful',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-OAuthlib',
        'psycopg2'
    ]
)
