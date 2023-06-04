from setuptools import setup
import os

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(name='yahoo-finance-api',
      version='0.0.1',
      description='Python wrapper for yahoo finance api',
      author='Alexander Haugerud',
      license='MIT',
      long_description=long_description,
      long_description_content_type='text/markdown',
      packages = ['yhf_api'],
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
      ],
      install_requires=['requests'],
      python_requires='>=3.8',
      include_package_data=True
)