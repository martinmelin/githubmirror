from setuptools import setup

setup(
    name='githubmirror',
    version='0.1',
    packages=['githubmirror', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read(),
    entry_points={
        'console_scripts': ['github-mirror = githubmirror:cmd'],
    }
)
