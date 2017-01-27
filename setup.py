#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
import codecs
import setuptools
import setuptools.command.test
if sys.version_info < (3, 6):
    raise Exception('vine 2.x requires Python 3.6 or higher.')
from pathlib import Path  # noqa

NAME = 'vine'

# -*- Classifiers -*-

classes = """
    Development Status :: 5 - Production/Stable
    Programming Language :: Python
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3.6
    License :: OSI Approved :: BSD License
    Intended Audience :: Developers
    Operating System :: OS Independent
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

# -*- Distribution Meta -*-

re_meta = re.compile(r'__(\w+?)__\s*=\s*(.*)')
re_doc = re.compile(r'^"""(.+?)"""')


def add_default(m):
    attr_name, attr_value = m.groups()
    return ((attr_name, attr_value.strip("\"'")),)


def add_doc(m):
    return (('doc', m.groups()[0]),)


pats = {re_meta: add_default,
        re_doc: add_doc}
here = Path(__file__).parent.absolute()
with open(here / 'vine' / '__init__.py') as meta_fh:
    meta = {}
    for line in meta_fh:
        if line.strip() == '# -eof meta-':
            break
        for pattern, handler in pats.items():
            m = pattern.match(line.strip())
            if m:
                meta.update(handler(m))


# -*- Installation Requires -*-

py_version = sys.version_info
is_jython = sys.platform.startswith('java')
is_pypy = hasattr(sys, 'pypy_version_info')


def strip_comments(l):
    return l.split('#', 1)[0].strip()


def reqs(f):
    return list(filter(None, [strip_comments(l) for l in open(
        Path.cwd() / 'requirements' / f).readlines()]))

# -*- Long Description -*-


if Path('README.rst').exists():
    long_description = codecs.open('README.rst', 'r', 'utf-8').read()
else:
    long_description = 'See http://pypi.python.org/pypi/vine'

# -*- Entry Points -*- #

# -*- %%% -*-


class pytest(setuptools.command.test.test):
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.pytest_args))


setuptools.setup(
    name=NAME,
    packages=setuptools.find_packages(exclude=['t', 't.*']),
    version=meta['version'],
    description=meta['doc'],
    long_description=long_description,
    keywords='promise promises lazy future futures',
    author=meta['author'],
    author_email=meta['contact'],
    url=meta['homepage'],
    platforms=['any'],
    classifiers=classifiers,
    license='BSD',
    install_requires=[],
    tests_require=reqs('test.txt'),
    cmdclass={'test': pytest},
    zip_safe=False,
    include_package_data=False,
)
