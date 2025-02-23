from setuptools import setup, find_packages

setup(
    name="doc_parser",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "python-multipart",
        "aiofiles",
        "requests",
        "PyMuPDF",
        "python-docx",
        "python-pptx",
        "pandas",
        "openpyxl",
        "pyyaml",
        "Pillow>=10.0.0",
        "langchain>=0.1.0",
        "langchain-openai>=0.0.2",
        "openai>=1.0.0",
        "mangum>=0.17.0",
        "functions-framework>=3.0.0",
        "azure-functions>=1.11.0",
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'black',
            'isort',
            'mypy',
        ]
    },
    python_requires='>=3.9',
    description='A document parsing service supporting multiple formats',
    author='Frank Li',
    author_email='liqila@gmail.com',
    url='https://github.com/liqila/DocuVision',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
) 