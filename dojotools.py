import os
from time import sleep, ctime

def p():
    print 'modificado'

def filter_files(files, patterns):
    """
    Filter a list of strings based on each item in 'patterns'

    Be careful, 'patterns' is NOT a regex, we only test if the string
    *contains* each of the so called patterns
    """
    for p in patterns:
        files = [f for f in files if p not in f]
    return files


def monitor(dir='.', callable=p, patterns=['.git', '.swp']):
    """
    Monitor a directory for changes, ignoring files matching any item in patterns and calls
    any callable when a file was changed.
    """
    old_sum = 0
    while True:

        m_time_list = []
        for root, dirs, files in os.walk(dir):
            files = filter_files(files, patterns)
            m_time_list += [os.stat(os.path.join(root, file)).st_mtime for file in files]

        new_sum = sum(m_time_list)
        if new_sum != old_sum:
            callable()
            old_sum = new_sum

        sleep(1)

if __name__ == '__main__':
    try:
        print 'Monitoring files'
        print 'press ^C to quit'
        monitor()
    except KeyboardInterrupt:
        print '\nleaving...'
