from setuptools import setup

setup(
    name='ThemeMapper',
    version='0.5.7',
    description='Thememapper for Diazo',
    author='Brandon Tilstra',
    author_email='tilstra@gmail.com',
    packages=['thememapper'],
    package_dir={'static': 'thememapper/static','templates': 'thememapper/templates'},
    long_description=open('README.rst').read(),
    license='LICENSE.txt',
    url='http://pypi.python.org/pypi/ThemeMapper/',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
      ],
    install_requires=['Flask','requests'],
    entry_points = {
    'console_scripts': [
                        'thememapper = thememapper.thememapper:main'
                       ]
    },
    include_package_data=True,
    zip_safe=False
)