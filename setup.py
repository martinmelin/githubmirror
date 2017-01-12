from setuptools import setup

setup(
    name='githubmirror',
    version='0.3.6',
    packages=['githubmirror', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    description='A small script to keep a copy of every repo in a Github org.',
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').read(),
    author='Martin Melin',
    author_email='martin@tictail.com',
    url='http://github.com/martinmelin/githubmirror',
    entry_points={
        'console_scripts': ['github-mirror = githubmirror:cmd'],
    }
)
