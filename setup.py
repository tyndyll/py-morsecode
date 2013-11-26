from distutils.core import setup

setup(
    name='MorseCode',
    version='1.0.0',
    author='Tyndyll',
    author_email='morse.code@tyndyll.net',
    packages=['morse'],
    scripts=['bin/telegraph.py'],
    url='http://pypi.python.org/pypi/MorseCode/',
    license='LICENSE.txt',
    description='Converting text to morse code pulses',
    long_description=open('README.txt').read(),
    install_requires=[
        "numpy",
        "scikits.audiolab",
    ],
)