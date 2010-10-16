"""

"""
# -*- encoding: utf-8 -*-

if __name__ == '__main__':

    options, args = parse_options()

    if options.patterns_file == None:
        options.patterns_file = os.path.join(
            options.directory,
            '.dojoignore'
        )

    try:
        print 'Monitoring files in %s' % options.directory
        print 'ignoring files in %s' % (options.patterns_file)
        print 'press ^C to quit'

        timer = Timer(options.round_time)
        monitor = Monitor(
            ui = UserInterface(timer)
            directory = get_document()[-1],
            commands = args,
            patterns_file = options.patterns_file,
            commit = options.commit,
        )

        gtk.main()

    except KeyboardInterrupt:
        print '\nleaving...'
        sys.exit(0)
