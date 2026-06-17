from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pyoslc',
    version='0.2.0',
    author='Contact Software',
    author_email='fp@contact.de',
    description='SDK for implementing OSLC API using Python.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cslab/pyoslc',
    packages=find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
    ],
    keywords='OSLC, SDK, REST, API, RDF, JSON-LD',
    python_requires='>=3.10',
    install_requires=[
        "python-dotenv>=1.0.0",
        "RDFLib>=7.0.0",
        "Flask>=3.0,<4.0",
        "Flask-RESTx>=1.3.0",
        "Flask-CORS>=4.0.0",
        "Flask-WTF>=1.2.0",
        "Flask-SQLAlchemy>=3.1.0",
        "Flask-Login>=0.6.0",
        "cachelib>=0.13.0",
        "Authlib>=1.0,<2.0",
        "requests>=2.31.0",
        "Werkzeug>=3.0,<4.0",
    ],
    extras_require={
        'dotenv': ['python-dotenv'],
        'dev': ['check-manifest'],
        'test': ['pytest>=8.0', 'pytest-cov', 'pytest-html'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/cslab/pyoslc/issues',
        'Source': 'https://github.com/cslab/pyoslc',
    },
)
