from distutils.core import setup

setup(
    name='githubmirror',
    version='0.1dev',
    packages=['githubmirror', ],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['github-mirror = githubmirror:main'],
    }
)
