#!/usr/bin/env python
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
import sys
import re
import subprocess
from optparse import OptionParser
import gtk
import gobject

from ui import UserInterface

class Timer(object):

    def __init__(self, round_time=300):
        self.round_time = round_time
        self.time_left = self.round_time

        gobject.timeout_add(1000, self.update)
        self.running = False

    def start(self):
        self.running = True

    def pause(self):
        self.running = False

    def update(self):
        if self.running:
            if self.time_left:
                self.time_left -= 1
            else:
                self.time_left = self.round_time

        return True


class Monitor(object):

    def __init__(self, ui, directory, commands, patterns_file):
        """
        'directory' is the directory to be watched for changes.

        --

        'commands' is a list with the commands to run when a file changes

        --

        'patterns_files' is the path to a file which contains a list that will
        be used to filter the files we're watching.
        """
        self.old_sum = 0
        self.directory = directory
        self.commands = commands
        self.patterns = self._get_patterns(patterns_file)
        self.ui = ui

        gobject.timeout_add(1000, self.check)

    def _get_patterns(self, patterns_file):
        """
        Reads `patterns_file' and returns a list of compiled regexes with
        every pattern found in the file + the file name.
        """
        try:
            with open(patterns_file, 'r') as f:
                patterns = [
                    p.strip().replace('*.', '.*\.')
                    for p in f.readlines()
                ]
        except IOError:
            sys.stdout.write(
                'Could not find %s. Patterns will not be ignored\n'
                % patterns_file
            )
            patterns = []

        # Add patterns_file to the ignored patterns so it won't be tracked
        patterns += [os.path.basename(patterns_file)]

        patterns = [re.compile(p) for p in patterns]

        return patterns

    def _filter_files(self, files):
        """
        Filter a list of strings based on each item in 'self.patterns'

        This function must be called every time `check` is called so we
        will not ignore newly created files in the directory (that is why
        files is not an instance attribute)
        """
        for p in self.patterns:
            files = [f for f in files if not p.match(f)]
        return files

    def run_command(self, test_cmd):
        """
        As the name says, runs a command and waits for it to finish
        """
        process = subprocess.Popen(
            test_cmd,
            shell = True,
            cwd = self.directory,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )

        output = process.stdout.read()
        output += process.stderr.read()
        status = process.wait()

        self.ui.show_command_results(status, output)

    def check(self):
        """
        Monitor self.directory for changes, ignoring files matching any item
        in self.patterns and runs any command in self.commands when a file has
        changed.
        """
        m_time_list = []
        for root, dirs, files in os.walk(self.directory):
            files = self._filter_files(files)
            # Be careful. The += operator works as the extend method
            # on mutable objects. For more information refer to
            # http://zephyrfalcon.org/labs/python_pitfalls.html
            m_time_list += [
                os.stat(os.path.join(root, f)).st_mtime for f in files
            ]

        new_sum = sum(m_time_list)
        if new_sum != self.old_sum:
            for command in self.commands:
                self.run_command(command)
            self.old_sum = new_sum

        # This method must return True so gobject.timeout_add runs it again
        return True


def parse_options():
    usage = "%prog [OPTIONS] COMMAND ..."
    description = """
        %prog watches a directory for changes. As soon as there are any changes
        to the files being watched, it runs the commands specified as positional
        arguments. You can specify as many commands as you wish, but don't forget
        to use quotes if you command has spaces in it.
    """.replace('  ', '')
    parser = OptionParser(usage, description=description)
    parser.add_option(
        '-d',
        '--directory',
        action = 'store',
        type = 'string',
        dest = 'directory',
        help = 'Watch DIRECTORY',
        metavar = 'DIRECTORY',
        default = os.path.abspath(os.path.curdir)
    )

    parser.add_option(
        '-p',
        '--patterns_file',
        action = 'store',
        type = 'string',
        dest = 'patterns_file',
        help = (
            'Defines the file with patterns to ignore. '
            'Make sure the patterns in the file are valid '
            'python regular expressions. '
            'Patterns like *.ext are also accepted.'
        ),
        metavar = 'PATTERNS_FILE',
        default = None,
    )

    parser.add_option(
        '-t',
        '--time',
        action = 'store',
        type = 'int',
        dest = 'round_time',
        help = 'Define the time of each round',
        default = 300
    )
    return parser.parse_args()


if __name__ == '__main__':

    options, args = parse_options()

    if options.patterns_file == None:
        options.patterns_file = os.path.join(
            options.directory,
            '.dojoignore'
        )

    try:
        print 'Monitoring files in %s' % options.directory
        print 'ignoring files in %s' % (options.patterns_file)
        print 'press ^C to quit'

        timer = Timer(options.round_time)
        ui = UserInterface(timer)
        monitor = Monitor(ui, options.directory, args, options.patterns_file)

        gtk.main()

    except KeyboardInterrupt:
        print '\nleaving...'
        sys.exit(0)
