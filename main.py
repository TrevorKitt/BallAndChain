import pygame as pg
import math
from settings import *


class Ball(pg.sprite.Sprite):
    def __init__(self, radius, colour, position, app):
        super(Ball, self).__init__()
        self.radius = radius
        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey((0,0,0))
        self.rect = pg.draw.circle(self.image, colour, (self.radius, self.radius), self.radius)
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.rect.move(position)
        self.movement_vector = pg.math.Vector2(0,0)
        self.chains = []
        self.app = app

    def add_chain(self, chain):
        self.chains.append(chain)

    def pull(self, vector, pulling_chain=None):
        self.movement_vector += vector
        for chain in self.chains:
            if chain is not pulling_chain:
                chain.pull()

    def get_next_location(self):
        return pg.math.Vector2(self.rect.center) + self.movement_vector

    def move(self):
        for chain in self.chains:
            chain.pull()
        self.rect = self.rect.move(self.movement_vector.x, self.movement_vector.y)
        if self is self.app.grabbed_ball:
            self.movement_vector = pg.math.Vector2(0,0)


class Chain:
    def __init__(self, ball1, ball2, length, app):
        self.ball1 = ball1
        self.ball2 = ball2
        self.length = length
        self.app = app

    def get_distance(self):
        return math.hypot(self.ball1.rect.centerx - self.ball2.rect.centerx,
                          self.ball1.rect.centery - self.ball2.rect.centery)

    def get_next_distance(self):
        return math.hypot(self.ball1.get_next_location().x - self.ball2.get_next_location().x,
                          self.ball1.get_next_location().y - self.ball2.get_next_location().y)

    def generate_vectors(self):
        difference = self.get_next_distance() - self.length
        target = (difference/self.get_next_distance())*pg.math.Vector2(
            self.ball1.get_next_location().x - self.ball2.get_next_location().x,
            self.ball1.get_next_location().y - self.ball2.get_next_location().y)
        if self.ball1 is self.app.grabbed_ball:
            return 0*target, target
        elif self.ball2 is self.app.grabbed_ball:
            return -1*target, 0*target
        else:
            return -0.5*target, 0.5*target

    def pull(self):
        if self.get_next_distance() > self.length:
            vectors = self.generate_vectors()
            self.ball1.pull(vectors[0], self)
            self.ball2.pull(vectors[1], self)


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
        self.ball1 = Ball(25, (125, 35, 200), (325, 450), self)
        self.ball2 = Ball(25, (175, 35, 50), (475, 450), self)
        chain = Chain(self.ball1, self.ball2, 150, self)
        self.ball1.add_chain(chain)
        self.ball2.add_chain(chain)
        self.ball_group = pg.sprite.Group(self.ball1, self.ball2)
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
            x_pull = mouse_x - self.grab_offset_x - self.grabbed_ball.rect.x
            y_pull = mouse_y - self.grab_offset_y - self.grabbed_ball.rect.y
            self.grabbed_ball.pull(pg.math.Vector2(x_pull, y_pull))

    def on_loop(self):
        for ball in self.ball_group:
            ball.move()

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
