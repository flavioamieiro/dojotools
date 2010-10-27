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

class OutputArea(gtk.HBox):
    """
    Criado por gabriel.pa.oliveira@gmail.com para direcionar o output do dojotools para o bottom panel
    Roubado com todos os creditos do RunInPython.py    
    """

    def __init__(self, geditwindow):
        gtk.HBox.__init__(self)

        self.geditwindow = geditwindow

        # Create a ListStore for the output we'll receive from the Python interpreter
        self.output_data = gtk.ListStore(str)

        # Create a TreeView (we'll use it just as a list though) for the output data
        self.output_list = gtk.TreeView(self.output_data)

        # Create a cell for the list
        cell = gtk.TreeViewColumn("Dojo Tools")

        # Add the cell to the TreeView
        self.output_list.append_column(cell)

        # Create a text renderer for our cell
        text_renderer = gtk.CellRendererText()

        # Add that text renderer to the cell
        cell.pack_start(text_renderer, True)

        # Set it to text
        cell.add_attribute(text_renderer, "text", 0)

        # Create a scrolled window for the TreeView and add the TreeView to that scrolled window.
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.add(self.output_list)

        # Add the scrolled window to this HBox
        self.pack_start(scrolled_window)

        #TODO: add another panel above/below that scrolled_window with icon-red-green and timer

        # Show everything
        self.show_all()

    def add_output(self, line):
        """ Deveria exibir a linha no output  e descer a barra de rolagem"""

        if (line != ""):
            # Add the new data to the TreeView we made
            self.output_data.append( (line,) )

            # Scroll to the end of the TreeView
            self.output_list.set_cursor(len(self.output_data) - 1)


class UserInterface(object):

    def __init__(self, timer, window=None):
        self.timer = timer
        self.current_status = 0

        self.status_icon = gtk.StatusIcon()
        self.status_icon.set_from_file(PASS_ICON)
        self._create_menu()
        self.status_icon.set_visible(True)

        self.window = window
        self.create_output(self.window)

        self.start_timer()

        gobject.timeout_add(1000, self.update_timer)

    def create_output(self, window):
        # Get the bottom panel.
        panel = window.get_bottom_panel()

        # Create an output area object (HBox) where we'll store the Python interpreter's output.
        self.output_area = OutputArea(window)

        # Add the item to the panel.
        panel.add_item(self.output_area, "Dojo Tools Output", gtk.Image())

    def remove_output(self):
        panel = self.window.get_bottom_panel()

        panel.remove_item(self.output_area)

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

        self.output_area.add_output(output)

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
