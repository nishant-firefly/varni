from setuptools import setup, find_packages

setup(
    name="varni",
    version="0.1.0",
    author="Nishant Saxena",
    author_email="nishant.saxena.varad@gmail.com",
    description="Varni: A low-code/no-code platform for managing database migrations and building Python applications.",
    long_description=open("varni/README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.varnitech.co",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: FastAPI",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
    ],
    python_requires='>=3.11',
    install_requires=[
        "SQLAlchemy>=1.3.0,<2.0.0",
        "alembic>=1.4.0,<2.0.0",
        "python-dotenv>=1.0.0",
        "fastapi>=0.60.0,<0.70.0",
        "uvicorn>=0.11.0,<0.16.0",
        "psycopg2>=2.8.0,<3.0.0",
        "elasticsearch>=7.0.0,<8.0.0",
    ],
    entry_points={
        'console_scripts': [
            'varni-db-setup=varni.dbs.migrations.varni_db_setup:main',
            'varni-migrate=varni.dbs.migrations.migration_tool:main',
        ],
    },
)
