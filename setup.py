from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="enfos-solo-survival",
    version="0.1.0",
    author="Findus Stenberg",
    author_email="findus.stenberg@gmail.com",
    description="Enfo's SOLO: X Hero Siege Edition - Survival Game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mandorenix/Enfos-Solo-Survival",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    install_requires=[
        "numpy>=1.21.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.900",
        ],
        "graphics": [
            "pygame>=2.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "solo-x=main:main",
            "solo-x-launcher=launcher:main",
        ],
    },
)
