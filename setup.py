from setuptools import setup, find_packages

setup(
    name='thememapper.core',
    version='0.5.9',
    description='thememapper for Diazo',
    author='Brandon Tilstra',
    author_email='tilstra@gmail.com',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['thememapper'],
    package_dir={'static': 'thememapper/static','templates': 'thememapper/templates'},
    include_package_data=True,
    long_description=open('README.rst').read(),
    license='LICENSE.txt',
    url='http://pypi.python.org/pypi/thememapper/',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
      ],
    install_requires=['setuptools','Flask','requests','urlparse'],
    entry_points = {
    'console_scripts': [
                        'thememapper = thememapper.core.thememapper:main'
                       ]
    },
    zip_safe=False
)