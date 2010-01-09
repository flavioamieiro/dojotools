#-*- coding: utf-8 -*-
"""


Dojotools - tools for your coding dojo session

Copyright (C) 2009 Flávio Amieiro <amieiro.flavio@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 dated June, 1991.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Library General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

If you find any bugs or have any suggestions email: amieiro.flavio@gmail.com
"""

import os
import subprocess
from time import sleep, ctime

def p():
    print 'modificado'

def git_commit_all(dir):
    """
    Adds all files and commits them
    """
    msg = ctime()
    p = subprocess.Popen("git add .; git commit -m '%s'" % msg, shell=True, cwd=dir)

    #if git returns 128 it means 'command not found' or 'not a git repo'
    if p.wait() == 128:
        raise OSError('Impossible to commit to repository. Make sure git is installed an this is a valid repository')


def filter_files(files, patterns):
    """
    Filter a list of strings based on each item in 'patterns'

    Be careful, 'patterns' is NOT a regex, we only test if the string
    *contains* each of the so called patterns
    """
    for p in patterns:
        files = [f for f in files if p not in f]
    return files


def monitor(dir='.', callable=git_commit_all, patterns=['.swp']):
    """
    Monitor a directory for changes, ignoring files matching any item in patterns and calls
    any callable when a file was changed.
    """
    old_sum = 0
    while True:

        m_time_list = []
        for root, dirs, files in os.walk(dir):
            # I have to ignore all the files in .git dir because any commit changes them
            # considering them would cause an infinite loop
            if '.git' in root:
                continue
            files = filter_files(files, patterns)
            m_time_list += [os.stat(os.path.join(root, file)).st_mtime for file in files]

        new_sum = sum(m_time_list)
        if new_sum != old_sum:
            callable(dir)
            old_sum = new_sum

        sleep(1)

if __name__ == '__main__':
    try:
        print 'Monitoring files'
        print 'press ^C to quit'
        monitor()
    except KeyboardInterrupt:
        print '\nleaving...'
