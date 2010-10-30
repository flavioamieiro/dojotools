#-*- coding: utf-8 -*-
"""


Dojotools - tools for your coding dojo session

Copyright (C) 2010
	César Frias <cagfrias@gmail.com>, 
    Luiz Bonsaver <luiz.bonsaver@gmail.com>,
    Natasha Paiva <nattynpaiva@gmail.com>
    Gabriel Oliveira <gabriel.pa.oliveira@gmail.com>

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
PASS_ICON = os.path.join(IMAGE_DIR, 'green_belt_small.png')
FAIL_ICON = os.path.join(IMAGE_DIR, 'red_belt_small.png')
KIMONO_ICON = os.path.join(IMAGE_DIR, 'kimono.png')

__all__ = ['UserInterface']

# a common ui definition for toolbar additions
ui_str = """<ui>
  <toolbar name="ToolBar">
    <separator />
    <toolitem name="DojoTimer" action="DojoTimer" />
  </toolbar>
</ui>
"""

class OutputArea(gtk.VBox):
    """
    Criado por gabriel.pa.oliveira@gmail.com para direcionar o output do dojotools para o bottom panel
    Roubado com todos os creditos do RunInPython.py    
    """

    def __init__(self, geditwindow, button_pause_play_event=None):
		gtk.VBox.__init__(self)

		# Create a ListStore for the output we'll receive from the Python interpreter
		self.output_data = gtk.ListStore(str)

		# Create a TreeView (we'll use it just as a list though) for the output data
		self.output_list = gtk.TreeView(self.output_data)

		# Create a cell for the list without tittle
		cell = gtk.TreeViewColumn(None)

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

		# Add the scrolled window to this VBox
		self.pack_start(scrolled_window)

		# Mark a flag for we do not try to set an empty tree
		self.empty_output = True

		# Create our Bar to Hold Icons - parameters (itensHasSameSpace , Spacing)
		hbox = gtk.HBox(True, 0)

		#create pass-fault icon
		self.pass_icon = gtk.Image()
		self.pass_icon.set_from_file(PASS_ICON)
		self.pass_icon.set_pixel_size(-10)
		self.pass_icon_state = "pass"

		#create Stop/Start Button
		#self.button_pause_play = gtk.Button("Click to Pause Timer")
		#self.button_pause_play.connect("clicked", button_pause_play_event, )

		#create timer label 
		self.timer_label = gtk.Label('00:00')

		#put it all in hbox
		hbox.pack_start(self.timer_label)
		hbox.pack_end(self.pass_icon)

		#put hbox in VBox
		self.pack_start(hbox)

		# Show everything
		self.show_all()

    def add_output(self, line):
        """ Deveria exibir a linha no output  e descer a barra de rolagem"""

        if (line != ""):
        	# If we have an empty_output we could not get our iterator or set nothing, so...    
            if self.empty_output:
            	# Just add the output line
            	self.output_data.append( (line,) )

            	# And down the flag
            	self.empty_output = False
            else:
            	# Add the result to our list - in the same row
            	iterator = self.output_data.get_iter_first()
            	self.output_data.set(iterator, 0, line )

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

		self._insert_ui_items()

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

	def create_output(self, window):
		# Get the bottom panel.
		panel = window.get_bottom_panel()

		# Create an output area where we'll store the tests output.
		self.output_area = OutputArea(window)

		# Add the item to the panel with kimono icon
		image = gtk.Image()
		image.set_from_file(KIMONO_ICON)
		panel.add_item(self.output_area, "Dojo Tools Output", image)

	def remove_output(self):
		panel = self.window.get_bottom_panel()

		panel.remove_item(self.output_area)

	def _insert_ui_items(self):
		# Get the GtkUIManager
		self._manager = self.window.get_ui_manager()

		# Create a new action group
		self._action_group = gtk.ActionGroup("DojoToolsPluginActions")

		# Create a toggle action (convenience way: see 16.1.2.2. in PyGTK Manual)
		self._action_group.add_toggle_actions([("DojoTimer",gtk.STOCK_MEDIA_PLAY,_("DojoTimer"),"","",self.on_toggle_stopDojo,False)])

		# Insert the action group
		self._manager.insert_action_group(self._action_group, -1)

		# Add my item to the "Views" menu and to the Toolbar
		self._ui_id = self._manager.add_ui_from_string(ui_str)

	def remove_ui_items(self):
		self._manager.remove_ui(self._ui_id)

	def on_toggle_stopDojo(self, action):

		_current_action = self._action_group.get_action("DojoTimer")
		_is_active = _current_action.get_active()

		if _is_active:
			_current_action.stock_id = gtk.STOCK_MEDIA_PAUSE
			self.timer.pause()
		else:
			_current_action.stock_id = gtk.STOCK_MEDIA_PLAY
			self.timer.start()

	def _show_menu(self, widget, button, time, data):
		data.show_all()
		data.popup(None, None, None, button, time)

	def _set_icon(self):
		if self.current_status == 0:
			if self.output_area.pass_icon_state == "fail":
				self.pass_icon.set_from_file(PASS_ICON)
				self.pass_icon_state = "pass"

			else: #already OK Icon
				pass

		else:
			if self.output_area.pass_icon_state == "pass":
				self.pass_icon.set_from_file(FAIL_ICON)
				self.pass_icon_state = "fail"

			else: #already OK icon
				pass

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

			self.output_area.timer_label.set_text(time_str)
		else:
			self.pause_timer()
			self.warn_time_is_up()
			self.start_timer()

		return True
