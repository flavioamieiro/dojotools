import gobject

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

