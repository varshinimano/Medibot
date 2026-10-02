from setuptools import find_packages, setup


setup(
    name="medical-chatbot",
    version="0.0.0",
    author="Varshini",
    author_email="varshinimano2005@gmail.com",
    packages=find_packages(),
    install_requires=[]
)

# __init__.py
#      ↓
# src is recognized as a package
#      ↓
# find_packages()
#      ↓
# finds src
#      ↓
# setup.py knows which package(s) belong to the project