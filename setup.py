import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name='MariaDB-SQLBuilder',
    long_description=README,
    long_description_content_type="text/markdown",
    version='0.0.1a',
    packages=["mariadb_sqlbuilder"],
    url='https://github.com/princessmiku/MariaDB-SQLBuilder',
    license='MIT',
    author='Miku',
    author_email='',
    description='MariaDB SQL Builder is a simple and thread safe way to use SQL. Use your own SQL or use the integrated SQL Builder tool.',
    python_requires='>=3.6.0'
)
