from setuptools import setup, find_packages

setup(
    name="Rufus",
    version="0.1.0",
    description="Rufus Client for interacting with the Rufus scraping API",
    packages=find_packages(),
    install_requires=[
        "requests",
        "fastapi",  
        "uvicorn",  
        "openai",
        "beautifulsoup4",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
