import pygame as pg
from settings import *


class Ball(pg.sprite.Sprite):
    def __init__(self, radius, colour):
        super(Ball, self).__init__()
        self.radius = radius
        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0,0,0))
        self.rect = pg.draw.circle(self.image, colour, (self.radius, self.radius), self.radius)
        self.mask = pg.mask.from_surface(self.image)


class App:
    def __init__(self):
        pg.init()
        self._running = True
        self.clock = pg.time.Clock()
        self.width, self.height = WINDOW_WIDTH, WINDOW_HEIGHT
        self.size = (self.width, self.height)
        self._display_surf = pg.display.set_mode(self.size)
        self.background = pg.Surface(self.size)
        self.background.fill((255,255,255))
        self.ball = Ball(25, (125, 35, 200))
        self.ball_group = pg.sprite.Group(self.ball)
        self.grabbed_ball = None
        self.grab_offset_x = 0
        self.grab_offset_y = 0

    def on_event(self, event):
        if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            self._running = False
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            for ball in self.ball_group:
                if ball.rect.collidepoint(event.pos):
                    mouse_x, mouse_y = event.pos
                    grab_offset_x = mouse_x - ball.rect.x
                    grab_offset_y = mouse_y - ball.rect.y
                    if ball.mask.get_at((grab_offset_x, grab_offset_y)):
                        self.grabbed_ball = ball
                        self.grab_offset_x = grab_offset_x
                        self.grab_offset_y = grab_offset_y
        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.grabbed_ball = None
        elif self.grabbed_ball and event.type == pg.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            self.grabbed_ball.rect.x = mouse_x - self.grab_offset_x
            self.grabbed_ball.rect.y = mouse_y - self.grab_offset_y

    def on_loop(self):
        pass

    def on_render(self):
        self._display_surf.blit(self.background, (0,0))
        self.ball_group.draw(self._display_surf)
        pg.display.flip()

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
