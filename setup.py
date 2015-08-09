# -*- coding: utf-8 -*-

from setuptools import setup


def read_readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='ChatRelater',
    version='0.2',
    description='Analyze and visualize relations between chat users.',
    long_description=read_readme(),
    license='MIT',
    author='Jochen Kupperschmidt',
    author_email='homework@nwsnet.de',
    url='http://homework.nwsnet.de/releases/1856/#chat-relater',
    packages=['chatrelater'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Communications :: Chat',
        'Topic :: Internet :: Log Analysis',
    ],
)
