from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-token-ecosystem",
    version="0.1.0",
    author="AI Token Ecosystem Team",
    description="High-tech AI Token Ecosystem with blockchain protection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lushkah/ai-token-ecosystem",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=[
        "web3>=6.0.0",
        "numpy>=1.21.0",
        "cryptography>=3.4.8",
        "pycryptodome>=3.15.0",
        "pandas>=1.3.0",
    ],
)
