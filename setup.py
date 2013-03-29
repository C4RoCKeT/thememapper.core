from setuptools import setup, find_packages

setup(
    name='thememapper.core',
    version='0.5.9',
    description='thememapper for Diazo',
    long_description=open('README.rst').read(),
    author='Brandon Tilstra',
    author_email='tilstra@gmail.com',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['thememapper'],
    package_dir={'static': 'thememapper/static','templates': 'thememapper/templates'},
    include_package_data=True,
    license='gpl',
    url='http://pypi.python.org/pypi/thememapper/',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
      ],
    install_requires=['setuptools','Flask','requests','tornado'],
    entry_points = {
    'console_scripts': [
                        'thememapper = thememapper.core.main:start_thememapper'
                       ]
    },
    zip_safe=False
)
