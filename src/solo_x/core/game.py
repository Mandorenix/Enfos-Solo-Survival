class Game:
    def __init__(self):
        self._running = False
    def start(self):
        self._running = True
    def stop(self):
        self._running = False