#-*- coding: utf-8 -*-
"""


Dojotools - tools for your coding dojo session

Copyright (C) 2010 César Frias <cagfrias@gmail.com>, 
    Luiz Bonsaver <luiz.bonsaver@gmail.com>,
    Natasha Paiva <nattynpaiva@gmail.com>

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
import gtk
import gobject


IMAGE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images/')
PASS_ICON = os.path.join(IMAGE_DIR, 'green_belt.png')
FAIL_ICON = os.path.join(IMAGE_DIR, 'red_belt.png')

__all__ = ['UserInterface']

class UserInterface(object):

    def __init__(self, timer):
        self.timer = timer
        self.current_status = 0

        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(PASS_ICON)
        self._create_menu()
        self.status_icon.set_visible(True)

        self.start_timer()

        gobject.timeout_add(1000, self.update_timer)

    def _create_menu(self):
        self.menu = gtk.Menu()

        self.pause_item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PAUSE)
        self.pause_item.connect('activate', self.pause_timer)

        self.play_item = gtk.ImageMenuItem(gtk.STOCK_MEDIA_PLAY)
        self.play_item.connect('activate', self.start_timer)

        self.quit_item = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.quit_item.connect('activate', gtk.main_quit, gtk)

        self.separator = gtk.MenuItem()

        self.menu.append(self.pause_item)
        self.menu.append(self.play_item)
        self.menu.append(self.separator)
        self.menu.append(self.quit_item)

        self.status_icon.connect('popup-menu', self._show_menu, self.menu)

    def _show_menu(self, widget, button, time, data):
        data.show_all()
        data.popup(None, None, None, button, time)

    def _set_icon(self):
        self.status_icon.set_from_file(
            PASS_ICON if self.current_status == 0 else FAIL_ICON
        )

    def pause_timer(self, widget=None):
        self.status_icon.set_from_stock(gtk.STOCK_MEDIA_PAUSE)
        self.timer.pause()

    def start_timer(self, widget=None):
        self._set_icon()
        self.timer.start()

    def warn_time_is_up(self):
        """Shows a dialog warning the pilot that his time is up"""
        dialog = gtk.Dialog('Dojotools', buttons=(gtk.STOCK_OK, 0))
        dialog.set_default_size(180, 120)
        dialog.vbox.pack_start(gtk.Label('Your time is up!'))
        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def show_command_results(self, status, output):
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

        self.current_status = status

        if self.timer.running:
            self._set_icon()

        test_output_dialog = gtk.Dialog('Dojotools', buttons=(gtk.STOCK_OK, 0))
        test_output_dialog.set_default_size(800, 300)
        test_output_dialog.vbox.pack_start(gtk.Label(output))
        test_output_dialog.show_all()
        test_output_dialog.run()
        test_output_dialog.destroy()


    def update_timer(self):
        if self.timer.time_left:
            time_str = '%02d:%02d' % (
                (self.timer.time_left / 60),
                (self.timer.time_left % 60)
            )
            self.status_icon.set_tooltip(time_str)
        else:
            self.pause_timer()
            self.warn_time_is_up()
            self.start_timer()

        return True
