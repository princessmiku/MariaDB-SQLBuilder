import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = '1.1.1'

setup(
    name='MariaDB-SQLBuilder',
    long_description=README,
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=[
        "mariadb_sqlbuilder",
        "mariadb_sqlbuilder.builder",
        "mariadb_sqlbuilder.sqlscript",
        "mariadb_sqlbuilder.helpful",
    ],
    url='https://github.com/princessmiku/MariaDB-SQLBuilder',
    license='LGPL 2.1',
    author='Miku',
    author_email='',
    description='MariaDB SQL Builder is a simple way to use Maria SQL. '
                'Use your own SQL or use the integrated Maria SQL Builder tool.',
    keywords=['database', 'mariadb', 'sql', 'builder', 'script builder', 'mariadb sql'],
    python_requires='>=3.7.0',
    install_requires=[
        "mariadb>=1.1.6",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
