import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="des_ini_utils",
    version="1.0.0",
    author="Nicholas Muise",
    author_email="nmuise@sefas.com",
    description="A tool to compare and dump the contents of producer install.ini files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    python_requires=">=2.7",
    install_requires=[
        "future"
    ],
    entry_points={
        "console_scripts": [
            "inicompare = src.utils:inicompare",
            "inidump = src.utils:inidump"
        ]
    }
)