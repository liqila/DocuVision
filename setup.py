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
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/doc_parser',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
) 