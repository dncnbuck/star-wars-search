import re
from setuptools import setup, find_packages

with open('swsearch/version', 'r') as fd:
    version = re.search(r'([0-9.\-A-Za-z]+)', fd.read().strip()).group(1)

setup(name='swsearch',
      version="{ver}".format(ver=version),
      description='A simple tool to show which StarWars characters are associated with a search term.',
      long_description=open('README.md').read(),
      url='',
      author='Duncan Buck',
      author_email='dncnbuck@gmail.com',
      license='RG',
      packages=find_packages(),
      package_data={
          'swsearch': ['*.md', '*.sh', 'data/*.json', 'docs/*'],
      },
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'requests',
        '',
        'flake8',
        'coverage',
        'pytest',
        'pytest-cov',
      ],
      entry_points={
          'console_scripts': [
              'swsearch = swsearch.__main__:main',
          ]},
      test_suite="swsearch.test"
      )
