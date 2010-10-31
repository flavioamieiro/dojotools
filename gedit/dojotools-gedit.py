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
        print 'Plugin Dojo-tools initialized'

    def deactivate(self):
        self._window = None
        self._plugin = None
        print 'Plugin Dojo-tools deactivated'

    def update_ui(self):
        # Called whenever the window has been updated (active tab
        # changed, etc.)
        pass

class DojoToolsGedit(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        #timer = Timer(self.round_timer or 300)
        #self.ui = UserInterface(timer, window)
        self._instances[window] = DojoToolsGeditHelper(self, window)

    def start_plugin(self, window):
        timer = Timer(int(self.round_timer))
        self.ui = UserInterface(timer, window)

    def deactivate(self, window):
        self.ui.remove_output()
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        if not self.has_monitor() or not hasattr(self, 'document'):
            self.create_monitor(window)
        self._instances[window].update_ui()

    def is_configurable(self):
        return True

    #TODO: Mover as 3 proximas funcoes para o ui
    def enter_callback(self, widget, entry_commands, entry_timer):
        self.commands = entry_commands.get_text()
        self.round_timer = entry_timer.get_text()
        self.configure_dialog.hide()
        return True

    def create_configure_dialog(self):
        self.configure_dialog = gtk.Dialog('Dojotools configuration')
        self.configure_dialog.set_default_size(300, 100)
        entry_commands = gtk.Entry()
        entry_timer = gtk.Entry()
        entry_commands.set_text("Type the commands and press Enter when finished")
        entry_timer.set_text("Time in seconds")
        entry_timer.connect("activate", self.enter_callback, entry_commands, entry_timer)
        self.configure_dialog.vbox.pack_start(entry_commands, True, True, 0)
        self.configure_dialog.vbox.pack_start(entry_timer, True, True, 0)
        self.configure_dialog.show_all()

        return self.configure_dialog

    def has_monitor(self):
        return hasattr(self, 'monitor')

    def create_monitor(self, window):
        self.get_attributes_to_monitor(window)
        if hasattr(self, 'commands') \
            and hasattr(self, 'round_timer') \
            and hasattr(self, 'document'):
            if not hasattr(self, 'monitor'):
                self.start_plugin(window)
                self.monitor = Monitor(
                    ui = self.ui,
                    directory = self.directory,
                    commands = self.commands,
                    patterns_file = self.patterns_file,
                    commit = False,
                )
            return self.monitor

    def get_attributes_to_monitor(self, window):
        documents = window.get_documents()
        for document in documents:
            if document.get_uri():
                self.document = document.get_uri().strip('file://')
                self.directory = '/' + self.document.rpartition('/')[0] + '/'
                self.patterns_file = self.directory + '.ignore'

        try:
            print self.commands, 'commands'
        except:
            pass
