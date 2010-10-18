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
        self.ui = UserInterface(timer)
        self._instances[window] = DojoToolsGeditHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        if not self.has_monitor() or self.commands == []:
            self.create_monitor(window)
        self._instances[window].update_ui()

    def has_monitor(self):
        try:
            if self.monitor:
                return True
            else:
                return False
        except:
            return False

    def create_monitor(self, window):
        commands = list()
        commands = self.get_commands(window)
        if commands != []:
            self.monitor = Monitor(
                ui = self.ui,
                directory = '/home/cesar/Dojo/codigosDojo/setembro/25/',
                commands = commands,
                patterns_file = '/home/cesar/Dojo/codigosDojo/setembro/25/.ignore',
                commit = False,
            )
            return self.monitor

    def get_commands(self, window):
        documents = window.get_documents()
        self.commands = list()
        for document in documents:
            if document.get_uri():
                teste = document.get_uri().strip('file://')
                self.commands = 'python /' + teste
        return self.commands

