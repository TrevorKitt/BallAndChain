import pygame as pg

class App:
    def __init__(self):
        pg.init()

    def on_event(self, event):
        pass

    def on_loop(self):
        pass

    def on_render(self):
        pass

    def on_execute(self):
        pass

if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
