# setup.py
# cm2c python commons library
# 20170310 v1
# 20190825 v0.1.8

from setuptools import setup

setup(name='cm2c',
      version='0.1.8',
      description='cm2c python commons',
      url='https://github.com/carlosm3011/cm2c-python-commons',
      author='Carlos M. Martinez',
      author_email='carlos@xt6.us',
      license='BSD',
      packages=['cm2c', 'cm2c.commons', 'cm2c.commons.debug',
                'cm2c.commons.gen', 'cm2c.csvimport', 'cm2c.etc'],
      install_requires=['ipaddr'],
      zip_safe=False)
