"""

"""
# -*- encoding: utf-8 -*-

import os
import gtk
import gedit
import gobject

from dojotoolsUi import UserInterface
from dojotoolsUi import window_configure_dialog
from dojotoolsUi import enter_callback_ui
from dojotools import Monitor, Timer

DEFAULT_TIMER = 300

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

        #Init for Ui knows itself
        self.ui = None

        self._instances = {}

    def activate(self, window):
        self._instances[window] = DojoToolsGeditHelper(self, window)

    def start_plugin(self, window):

        try:
            timer = Timer(int(self.round_timer))
        except:
            timer = Timer(DEFAULT_TIMER)

        if self.ui != None:
	        self.ui.re_initialize(timer)
        else:
            self.ui = UserInterface(timer, window)

    def deactivate(self, window):
        self.ui.remove_output()
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        if not self.has_monitor() or not self.has_document():
            self.create_monitor(window)
        self._instances[window].update_ui()

    def is_configurable(self):
        return True

    def enter_callback(self, widget, entry_commands, entry_timer):
        return enter_callback_ui(self, widget, entry_commands, entry_timer, DEFAULT_TIMER)

    def create_configure_dialog(self):
        return window_configure_dialog(self)

    def has_monitor(self):
        return hasattr(self, 'monitor')

    def has_document(self):
        return hasattr(self, 'document')

    def has_round_timer(self):
        return hasattr(self, 'round_timer')

    def has_commands(self):
        return hasattr(self, 'commands')

    def create_monitor(self, window):
        self.get_attributes_to_monitor(window)
        if self.has_commands() and self.has_round_timer() and self.has_document():
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
