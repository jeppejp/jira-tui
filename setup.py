#!/usr/bin/env python3

from distutils.core import setup

setup(name='JiraTui',
      version='1.0',
      description='Faster way to find and open jira issues',
      author='Jeppe Petersen',
      author_email='jeppejp@gmail.com',
      url='',
      packages=['JiraTui', ],
      entry_points={'console_scripts': ['jiratui = JiraTui.Main:main']})
