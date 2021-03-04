from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    reqs = f.read().split('\n')[:-2]

setup(
    name='reo_toolkit',
    version='0.1',
    packages=find_packages(exclude=['tests*']),
    license='Kaitiakitanga License',
    description='A python package for manipulating māori language text',
    long_description=open('README.md', 'r', encoding = 'utf-8').read(),
    install_requires=['jamo', 'inflection', 'pyahocorasick', 'nltk'],
    url='https://github.com/TeHikuMedia/reo-toolkit',
    author='Caleb Moses',
    author_email='caleb@dragonfly.co.nz',
    include_package_data=True
)
