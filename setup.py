from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

setup(
    name='jenkins_client',
    packages=find_packages(),
    version='0.1.0',
    description='A client for Jenkins',
    author='Yorgos Katsaros',
    license='MIT',
    long_description=readme,
    url="https://github.com/Orfium/jenkins_client",
    install_requires=["jenkinsapi", "requests"],
)
