#-*- coding: utf-8 -*-
import threading
import gobject
import os
import sys
import subprocess
import datetime 
import arduino
import lang
from fnmatch import fnmatch


def git_commit(self, directory, author=None):
    """
    Adds all files and commits them using git
    """
    msg = ctime()

    if not author:
        command = "git add . && git commit -m '%s'" % (msg)
    else:    
        command = "git add . && git commit -m '%s' --author='%s <dojotools@dojo>'" % (msg, self.who_plays)
        
    process = subprocess.Popen(
        command,
        shell=True,
        cwd=directory,
    )

    #if git returns 128 it means 'command not found' or 'not a git repo'
    if process.wait() == 128:
        error = (lang.GIT_ERROR1+
                lang.GIT_ERROR2)
        raise OSError(error)
            

class DojoPlayer(object):
    def __init__(self, directory, who):
        self.directory = directory
        self.who = who
        self.name = "Unknown"
        
    def commit(self):
        git_commit(self.directory, author=self.name if self.who else None)        
    



class RunThread (threading.Thread):
    """Thread class to run and terminate commands."""

    def __init__ (self, test_cmd,  monitor):
        super(RunThread, self).__init__()
        self._stop = threading.Event()
        self.test_cmd = test_cmd
        self.directory = monitor.directory
        self.arduino = monitor.arduino
        self.ui = monitor.ui
        self.start_time = '%02d:%02d:%02d' % (
                (datetime.datetime.now().hour),
                (datetime.datetime.now().minute),
                (datetime.datetime.now().second),
            )
        self.process = None
        
    def run(self):
        """
        runs a command and waits for it to finish
        """
        self.ui.set_kill_label(lang.KILL % (self.__repr__()))
        self.process = subprocess.Popen(
            self.test_cmd,
            shell = True,
            cwd = self.directory,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )

        output = self.process.stdout.read()
        output += self.process.stderr.read()
        status = self.process.wait()
        try:
            if self.arduino:
                arduino.send_message(status, last=self.status)
                self.status = status
        except:
            print lang.ARDUINO_ERROR
        
        self.ui.set_kill_label()
        self.stop()
        self.ui.show_command_results(status, output)
        return output
                
    def stop (self):
        """Stop thread and terminate running command"""
        if not self.ui.kill_item.get_label() == lang.NO_RUNNING:
            self.ui.show_command_results(True, lang.INTERRUPTED_EXECUTION)
        self.ui.set_kill_label()
        
        try:
            self.process.stdout.close() 
            self.process.stderr.close() 
            self.process.terminate()   
              
        except:
            pass
        
        self._stop.set()
        self._Thread__stop()

    def stopped (self):
        return self._stop.isSet()
        
    def __repr__(self):
        return self.start_time+" - "+self.test_cmd.split()[-1]

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

    def __init__(self, ui, directory, commands, patterns_file, commit=False, arduino=False, use_thread=False, before=""):
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
        self.commit = commit
        self.arduino = arduino
        self.use_thread = use_thread
        self.before = before
        self.status = False
     
        gobject.timeout_add(1000, self.check)

    def _get_patterns(self, patterns_file):
        """
        Reads `patterns_file' and returns a list of patterns found in
        the patterns file, so they can be used in fnmatch.

        Patterns should be Unix style.

        For more information, type help(fnmatch) in a python shell
        """
        try:
            with open(patterns_file, 'r') as f:
                patterns = [pattern.strip() for pattern in  f.readlines()]
        except IOError:
            sys.stdout.write(
                lang.PATTERNS_NOT_FOUND
                % patterns_file
            )
            patterns = []

        # Add patterns_file to the ignored patterns so it won't be tracked
        patterns += [os.path.basename(patterns_file)]

        return patterns

    def _filter_files(self, files):
        """
        Filter a list of strings based on each item in 'self.patterns'

        This function must be called every time `check` is called so we
        will not ignore newly created files in the directory (that is why
        files is not an instance attribute)
        """
        for p in self.patterns:
            files = [f for f in files if not fnmatch(f, p)]
        return files

    def run_command(self, test_cmd):
        """
        As the name says, runs a command 
        """
        if self.before:
            self._normal_run(self.before, before_command=True)
            
        if self.use_thread:
            self._run_by_thread(test_cmd)
        else:
            self._normal_run(test_cmd)
        
    def _run_by_thread(self, test_cmd):
        """
        Runs command in a thread without waiting for it to finish
        """
        thread = RunThread(test_cmd, self)
        thread.start()
        self.ui.thread = thread
        
    def _normal_run(self, test_cmd, before_command=False):
        """
        Runs a command and waits for it to finish"
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
        try:
            if self.arduino:
                arduino.send_message(status, last=self.status)
                self.status = status
        except:
            print lang.ARDUINO_ERROR
        if not before_command:
            self.ui.show_command_results(status, output)
        else:
            sys.stdout.write(output)
        
    def check(self):
        """
        Monitor self.directory for changes, ignoring files matching any item
        in self.patterns and runs any command in self.commands when a file has
        changed.
        """
        m_time_list = []
        for root, dirs, files in os.walk(self.directory):
            # We must ignore all the files in .git directory because
            # any commit changes them. Taking this directory into
            # consideration would cause an infinite loop.
            if '.git' in root:
                continue
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
            if self.commit:
                self.ui.git_commit_all()
            self.old_sum = new_sum

        # This method must return True so gobject.timeout_add runs it again
        return True
