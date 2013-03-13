from setuptools import setup

setup(
    name='ThemeMapper',
    version='0.5',
    description='Thememapper for Diazo',
    author='Brandon Tilstra',
    author_email='tilstra@gmail.com',
    packages=['thememapper'],
    long_description=open('README.txt').read(),
    license='LICENSE.txt',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
      ],
    install_requires=['Flask','pycurl'],
)