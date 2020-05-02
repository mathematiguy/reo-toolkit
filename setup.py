from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    reqs = f.read().split()[:-1]

setup(
    name='reo_toolkit',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='Kaitiakitanga License',
    description='A python package for manipulating māori language text',
    long_description=open('README.md').read(),
    install_requires=reqs,
    url='https://github.com/TeHikuMedia/reo-toolkit',
    author='Caleb Moses',
    author_email='caleb@dragonfly.co.nz'
)
