try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup



setup(name='easyrad',
      version='0.0.1',
      description='Easy for doing radiology in python',
      long_description=open('README.md').read(),
      url='https://www.github.com/kmader/radiology_binder',
      license='Apache',
      author='Kevin Mader',
      packages=['easyrad'],
      install_requires=['numpy', 'pandas', ],
      extras_require={
        'plots':  ["matplotlib"]
        }
      )
