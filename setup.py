from setuptools import setup, find_packages
import os


here = os.path.abspath(os.path.dirname(__file__))


# Get the long description from the README file
with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme_file:
    long_description = readme_file.read()

setup(
    name='pydeps',
    version='0.1.0',

    description='Manage dependencies between applications',
    long_description=long_description,

    url='https://github.com/sylicia/pydeps',

    author='Cyrielle Camanes (sylicia)',
    author_email='cyrielle.camanes@gmail.com',

    license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Intended Audience :: Customer Service',
        'Topic :: Utilities',
        'Topic :: System :: Systems Administration',
        'Topic :: Home Automation',

        'Environment :: Console',

        'Natural Language :: English',

        'Programming Language :: Python :: 2.7'
    ],

    keywords=['management', 'application', 'dependencies'],

    packages=['pydeps'],
    package_dir={'pydeps': 'pydeps'},
    install_requires=['docopt', 'PyYAML', 'jinja2'],
    extras_require={
        'test': ['pytest', 'coverage']
    },
    scripts=['scripts/graph_dot'],
    data_files=[
        ('graph_dot', ['data/graph_dot.j2'])
    ]
)
