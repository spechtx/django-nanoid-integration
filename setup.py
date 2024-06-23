"""Save your Django uploaded files using NanoIDs for file names or store them in directories named with NanoIDs."""
from setuptools import setup, find_packages

setup(
    name='django-nanoid-integration',
    version='0.1.0',
    author='Christian H. Specht',
    author_email='cs@spechtx.de',
    description=__doc__,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/spechtx/django-nanoid-integration',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
	license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'Django>=1.7',
		'nanoid'
    ],
)
