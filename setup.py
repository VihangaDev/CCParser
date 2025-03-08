from setuptools import setup, find_packages

setup(
    name="ccparser",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ccparser=ccparser.cli:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for credit card parsing, validation, and formatting",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/yourusername/ccparser",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)