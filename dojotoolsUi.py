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

from dojotools import Timer

IMAGE_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'dojotools-images/')
PASS_ICON = os.path.join(IMAGE_DIR, 'green_belt_small.png')
FAIL_ICON = os.path.join(IMAGE_DIR, 'red_belt_small.png')
KIMONO_ICON = os.path.join(IMAGE_DIR, 'kimono.png')

__all__ = ['UserInterface']

def enter_callback_ui(self, widget, entry_commands, entry_timer, DEFAULT_TIMER, window):
    self.commands = entry_commands.get_text()
    self.round_timer = entry_timer.get_text()
    self.configure_dialog.hide()

    #Refresh monitor commands
    if self.has_monitor():
        self.monitor.commands = self.commands

    #Refresh Ui
    try:
        timer = Timer(int(self.round_timer))
    except:
        timer = Timer(DEFAULT_TIMER)

    if self.ui != None:
        self.ui.re_initialize(timer)
    else:
        self.ui = UserInterface(timer, window.keys()[0])

    return True


def window_configure_dialog(self):
    self.configure_dialog = gtk.Dialog('Dojotools configuration')
    self.configure_dialog.set_default_size(300, 100)

    #entry comands - use text default ?
    entry_commands = gtk.Entry()
    if not self.has_commands():
        entry_commands.set_text("Commands to execute")
    else:
        entry_commands.set_text(self.commands)

    #entry_timer - use text default ?
    entry_timer = gtk.Entry()
    if not self.has_round_timer():
        entry_timer.set_text("Time in seconds, default is 300")
    else:
        entry_timer.set_text(self.round_timer)

    #Gabriel se metendo aqui e botando um botao de OK para ativar as coisas
    ok_button_box = gtk.HBox(False,0)
    ok_button = gtk.Button('OK')
    ok_button.connect("clicked", self.enter_callback, entry_commands, entry_timer)
    ok_button_box.pack_start(ok_button)
    ok_button_align = gtk.Alignment(0.5,0,0,0)
    ok_button_align.add(ok_button_box)

    self.configure_dialog.vbox.pack_start(entry_commands, True, True, 0)
    self.configure_dialog.vbox.pack_start(entry_timer, True, True, 0)
    self.configure_dialog.vbox.pack_start(ok_button_align, True, True, 0)
    self.configure_dialog.show_all()

    return self.configure_dialog

class OutputArea(gtk.VBox):
	"""
	Criado por gabriel.pa.oliveira@gmail.com para direcionar o output do dojotools para o bottom panel
	Roubado com todos os creditos do RunInPython.py
	"""

	def __init__(self, timer):
		gtk.VBox.__init__(self)

		# Save our Timer fr further control
		self.timer = timer

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

		#create our stocks
		self.stock_pause = gtk.Image()
		self.stock_pause.set_from_stock(gtk.STOCK_MEDIA_PAUSE,1)

		self.stock_play = gtk.Image()
		self.stock_play.set_from_stock(gtk.STOCK_MEDIA_PLAY,1)

		#create Stop/Start Button
		self.button_pause_play = gtk.Button()
		self.button_pause_play.set_image(self.stock_pause)
		self.button_pause_play.set_tooltip_text("Click to pause timer")
		self.button_pause_play.connect("clicked", self.button_pause_play_event)

		#create timer label
		self.timer_label = gtk.Label('00:00')

		#create our hbox_rigth to old our pass_icon
		hbox_rigth = gtk.HBox(True,0)

		#create pass-fault icon
		self.pass_icon = gtk.Image()
		self.pass_icon.set_from_file(PASS_ICON)
		self.pass_icon_state = "pass"

		#put it all in hbox
		hbox.pack_start(self.button_pause_play, True, True, 0)
		hbox.pack_start(self.timer_label, True, True, 10)
		hbox.pack_start(self.pass_icon)

		#create our align
		hAlign = gtk.Alignment(0,0,0,0)
		hAlign.add(hbox)

		#put hbox in VBox
		self.pack_start(hAlign)

		# Show everything
		self.show_all()

	def button_pause_play_event(self, widget):
		"""Reconhece a partir do tooltip qual o estado do botao, afim de saber se start/stop o timer """
		if "pause" in self.button_pause_play.get_tooltip_text():
			self.stop_timer()
			return;

		if "play" in  self.button_pause_play.get_tooltip_text():
			self.start_timer()
			return;

	def start_timer(self):
		"""Inicializa/Re-inicializa o timer e muda a imagem do botao de acordo """

		self.button_pause_play.set_image(self.stock_pause)
		self.button_pause_play.set_tooltip_text("Click to pause timer")

		#pause timer
		self.timer.start()

	def stop_timer(self):
		"""Pausa o timer e muda a imagem do botao de acordo """

		self.button_pause_play.set_image(self.stock_play)
		self.button_pause_play.set_tooltip_text("Click to play timer")

		#pause timer
		self.timer.pause()

	def add_output(self, line):
		""" Exibir a line no output e descer a barra de rolagem.
		Apenas o ultimo teste fica visivel"""

		if line != "":
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

		self.window = window
		self.create_output(self.window)

		self.pause_timer()

		gobject.timeout_add(1000, self.update_timer)

	def re_initialize(self, timer):
		""" When Ui is already crated, use it to re-init it """
		self.timer = timer
		self.current_status = 0
		self.pause_timer()

	def create_output(self, window):
		# Get the bottom panel.
		panel = window.get_bottom_panel()

		# Create an output area where we'll store the tests output.
		self.output_area = OutputArea(self.timer)

		# Add the item to the panel with kimono icon
		image = gtk.Image()
		image.set_from_file(KIMONO_ICON)
		panel.add_item(self.output_area, "Dojo Tools Output", image)

	def remove_output(self):
		panel = self.window.get_bottom_panel()

		panel.remove_item(self.output_area)

	def _set_icon(self):
		if self.current_status == 0:
			self.output_area.pass_icon.set_from_file(PASS_ICON)
			self.output_area.pass_icon_state = "pass"

		else:
			self.output_area.pass_icon.set_from_file(FAIL_ICON)
			self.output_area.pass_icon_state = "fail"

	def pause_timer(self, widget=None):
		self.output_area.stop_timer()

	def start_timer(self, widget=None):
		self.output_area.start_timer()

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

		self._set_icon()

		self.output_area.add_output(output)

	def update_timer(self):
		if self.timer.time_left:
			time_str = '%02d:%02d' % (
			(self.timer.time_left / 60),
			(self.timer.time_left % 60)
			)

			self.output_area.timer_label.set_text(time_str)

		else:
			self.pause_timer()
			self.warn_time_is_up()
			self.start_timer()

		return True
