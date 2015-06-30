from setuptools import setup

setup(
    name='Django-Youtuber',
    version='0.1.0',
    author='Rakan Alhneiti',
    author_email='rakan.alhneiti@gmail.com',

    # Packages
    packages=[
        'youtuber',
        'youtuber/management',
        'youtuber/migrations',
        'youtuber/tests'
    ],
    include_package_data=True,

    # Details
    url='https://github.com/rakanalh/django-youtuber',

    license='LICENSE.txt',
    description='Django app for fetching videos from channels or playlists.',
    long_description=open('README.md').read(),

    # Dependent packages (distributions)
    install_requires=[
        'django',
        'celery',
        'requests'
    ],
)
