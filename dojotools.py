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
import subprocess
from optparse import OptionParser
from time import ctime
import gtk
import gobject

try:
    import pynotify
except ImportError:
    pynotify = None
    sys.stderr.write('\n\n*** Could not import pynotify. Make sure it is installed so you can see the notifications ***\n\n\n')

IMAGE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images/')
PASS_ICON = os.path.join(IMAGE_DIR, 'green_belt.png')
FAIL_ICON = os.path.join(IMAGE_DIR, 'red_belt.png')


class Monitor(object):


    def __init__(self, directory, commands, patterns, round_time=300):
        """
        'directory' is the directory to be watched for changes.

        --

        'commands' is a list with the commands to run when a file changes

        --

        'patterns' is a list that will be used to filter the files we're
        watching.

        Be careful, 'patterns' is NOT a regex, we only test if the string
        *contains* each of the so called patterns

        """
        self.old_sum = 0
        self.directory = directory
        self.commands = commands
        self.patterns = patterns

        self._create_icon()

        gobject.timeout_add(1000, self.check)
        gobject.timeout_add(1000, self.update_timer)

        self.round_time = round_time
        self.time_left = round_time

    def _create_icon(self):
        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(PASS_ICON)

        self.menu = gtk.Menu()
        self.quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.quit_item.connect('activate', gtk.main_quit, gtk)

        self.menu.append(self.quit_item)

        self.status_icon.connect('popup-menu', self.show_menu, self.menu)
        self.status_icon.set_visible(True)

    def show_menu(self, widget, button, time, data):
        data.show_all()
        data.popup(None, None, None, button, time)

    def _warn_time_is_up(self):
        """Shows a dialog warning the pilot that his time is up"""
        dialog = gtk.Dialog('Dojotools', buttons=(gtk.STOCK_OK, 0))
        dialog.set_default_size(180, 120)
        dialog.set_keep_above(True)
        dialog.vbox.pack_start(gtk.Label('Your time is up!'))
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def _show_command_results(self, status, output):
        """
        Shows the output to the users.

        For now, it will write the output to stdout,
        change the icon depending on the status (green
        if the tests are passing, red otherwise) and,
        if pynotify is installed, show a notification.

        If you use this in Ubuntu, I'm sorry for you.
        Canonical just decided to break libnotify in so
        many ways that it is *impossible* to use it sanely.

        """

        sys.stdout.write(output)

        self.status_icon.set_from_file(PASS_ICON if status == 0 else FAIL_ICON)

        if pynotify:
            pynotify.init('dojotools')
            message = pynotify.Notification('Dojotools', output)
            message.attach_to_status_icon(self.status_icon)
            message.set_urgency(pynotify.URGENCY_NORMAL if status == 0 else pynotify.URGENCY_CRITICAL)
            message.show()

    def update_timer(self):
        if self.time_left:
            self.time_left -= 1
            time_str = '%02d:%02d' % ((self.time_left / 60), (self.time_left % 60))
            self.status_icon.set_tooltip(time_str)
        else:
            self._warn_time_is_up()
            self.time_left = self.round_time

        return True

    def _filter_files(self, files):
        """
        Filter a list of strings based on each item in 'self.patterns'

        This function must be called every time `check` is called so we
        will not ignore newly created files in the directory (that is why
        files is not an instance attribute)
        """
        for p in self.patterns:
            files = [f for f in files if p not in f]
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

        self._show_command_results(status, output)


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
        '--pattern',
        action = 'append',
        type = 'string',
        dest = 'patterns',
        help = ' '.join([
            'Ignore PATTERN.',
            'You may define this as many times as you want',
            'like in -p .txt -p .swp'
            ]),
        metavar = 'PATTERN',
        default = [],
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

    try:
        print 'Monitoring files in %s' % options.directory
        if options.patterns:
            print 'ignoring files with %s in their name' % ' '.join(options.patterns)
        print 'press ^C to quit'

        monitor = Monitor(options.directory, args, options.patterns, options.round_time)

        gtk.main()

    except KeyboardInterrupt:
        print '\nleaving...'
        sys.exit(0)
