from setuptools import setup, find_packages

setup(
    name="CCParser",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'ccparser=ccparser.cli:main',
        ],
    },
    author="Vihanga Indusara",
    author_email="vihangadev@gmail.com",
    description="A library for credit card parsing, validation, and formatting",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/VihangaDev/CCParser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)