# -*- coding: utf-8 -*-
SET_TIME = 'Alterar tempo (%d segs)'
RESET_TIME = 'Resetar tempo'
NO_RUNNING = u"Nenhum projeto em execução"
PAUSE = 'Pausar'
START = 'Reproduzir'
TIME_IS_UP = 'Your time is up!'
WRITE_TIME = 'Escolha o tempo (em segundos)!'
VALUE_ERROR = u"Caracter inválido. Suas alterações não foram salvas"

KILL = "Matar %s"

ARDUINO_ERROR = u'Algum erro de comunicação com o Arduino ocorreu!'

INTERRUPTED_EXECUTION = u"Execução interrompida"

PATTERNS_NOT_FOUND = 'Could not find %s. Patterns will not be ignored\n' 

PYNOTIFY_IMPORT_ERROR1 = '\n\n*** Could not import pynotify. '
PYNOTIFY_IMPORT_ERROR2 = ('Make sure it is installed so you '
                          'can see the notifications ***\n\n\n')

GIT_ERROR1 = 'Impossible to commit to repository. '
GIT_ERROR2 = 'Make sure git is installed and this is a valid repository'

DESCRIPTION = """
    %prog watches a directory for changes. As soon as there are any changes
    to the files being watched, it runs the commands specified as positional
    arguments. You can specify as many commands as you wish, but don't forget
    to use quotes if you command has spaces in it.
""".replace('  ', '')
GIT_HELP = ('if this flag is used, a git commit will '
            'be issued whenever the files change')
DIRECTORY_HELP = 'Watch DIRECTORY'
PATTERNS_HELP = 'Defines the file with patterns to ignore. '
TIME_HELP = 'Define the time of each round'
ARDUINO_HELP = 'If this flag is used an interface with Arduino will be used'
MULTITHREAD_HELP = 'If this flag is used the program will run in a thread'
BEFORE_HELP = ('Run this command before running tests.'
               'WARNING: It will not run in thread, so be careful with your commands'
)
MONITORING = 'Monitoring files in %s'
IGNORING = 'ignoring files in %s'
QUIT = 'press ^C to quit'

LEAVING = '\nleaving...'