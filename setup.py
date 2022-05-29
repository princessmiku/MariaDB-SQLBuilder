import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

VERSION = '0.4.0'

setup(
    name='MariaDB-SQLBuilder',
    long_description=README,
    long_description_content_type="text/markdown",
    version=VERSION,
    packages=["mariadb_sqlbuilder",
              "mariadb_sqlbuilder.builder",
              "mariadb_sqlbuilder.execution"
              ],
    url='https://github.com/princessmiku/MariaDB-SQLBuilder',
    license='MIT',
    author='Miku',
    author_email='',
    description='MariaDB SQL Builder is a simple and thread safe way to use Maria SQL. Use your own SQL or use the integrated Maria SQL Builder tool.',
    keywords=['python', 'database', 'mariadb', 'sql', 'builder', 'script builder', 'mariadb sql', 'orm'],
    python_requires='>=3.6.0',
    install_requires=[
        "mariadb>=1.0.11",
        "sqlparse>=0.4.2"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
