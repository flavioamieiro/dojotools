"""

"""
# -*- encoding: utf-8 -*-

import os
import gtk
import gedit
import gobject

from ui import UserInterface
from dojotools import Monitor, Timer

class DojoToolsGeditHelper:
    def __init__(self, plugin, window):
        self._window = window
        self._plugin = plugin

    def deactivate(self):
        self._window = None
        self._plugin = None

    def update_ui(self):
        # Called whenever the window has been updated (active tab
        # changed, etc.)
        pass

class DojoToolsGedit(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        timer = Timer(300)
        self.ui = UserInterface(timer, window)
        self._instances[window] = DojoToolsGeditHelper(self, window)

    def deactivate(self, window):
        self.ui.remove_output()
        self._instances[window].deactivate()
        del self._instances[window]

    #TODO: Precisa ser refatorada, acho que o hasattr resolve isso
    def update_ui(self, window):
        if not self.has_monitor() or self.document == '':
            self.create_monitor(window)
        self._instances[window].update_ui()

    def is_configurable(self):
        return True

    #TODO: Mover as 3 próximas funções para o ui
    def enter_callback(self, widget, entry):
        self.entry_text = entry.get_text()

    def create_configure_dialog(self):
        configure_dialog = gtk.Dialog('Dojotools configuration')
        configure_dialog.set_default_size(300, 100)
        entry = gtk.Entry()
        entry.set_text("Type the commands and press Enter")
        entry.connect("activate", self.enter_callback, entry)
        configure_dialog.vbox.pack_start(entry, True, True, 0)
        entry.show()
        configure_dialog.show()

        return configure_dialog

    def has_monitor(self):
        try:
            if self.monitor:
                return True
            else:
                return False
        except:
            return False

    def create_monitor(self, window):
        self.commands = str()
        self.get_attributes_to_monitor(window)
        if self.commands != '':
            self.monitor = Monitor(
                ui = self.ui,
                directory = self.directory,
                commands = self.commands,
                patterns_file = self.patterns_file,
                commit = False,
            )
            return self.monitor

    #TODO: Pegar dados a partir da janela de configuração
    def get_attributes_to_monitor(self, window):
        documents = window.get_documents()
        commands = list()
        for document in documents:
            if document.get_uri():
                self.document = document.get_uri().strip('file://')
                self.commands = 'python /' + self.document
                self.directory = '/' + self.document.rpartition('/')[0] + '/'
                self.patterns_file = '/' + self.directory + '.ignore'

        try:
            print self.document, self.commands, self.directory, self.patterns_file
        except:
            pass
