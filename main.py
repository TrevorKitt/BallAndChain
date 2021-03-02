import pygame as pg
from settings import *

class App:
    def __init__(self):
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.size = (self.width, self.height)
        self._display_surf = pg.display.set_mode(self.size)

    def on_event(self, event):
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_cleanup(self):
        pg.quit()

    def on_execute(self):
        while self._running:
            for event in pg.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            self.clock.tick(FPS)
        self.on_cleanup()

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
