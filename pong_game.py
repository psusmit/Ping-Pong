from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from random import randint


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongPaddle(Widget):
    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    score1 = NumericProperty(0)  # Score for player 1
    score2 = NumericProperty(0)  # Score for player 2

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)
        self.keysPressed = set()


    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.keysPressed.add(keycode[1])

    def _on_keyboard_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.keysPressed:
            self.keysPressed.remove(text)

    def update(self, dt):
    # Move the ball
        self.ball.move()

    # Check for ball collision with paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    # Ball collision with top and bottom
        if (self.ball.y <= 0) or (self.ball.top >= self.height):
            self.ball.velocity_y *= -1

    # Ball went off to a side to score point?
        if self.ball.x < 0 or self.ball.right > self.width:
            if self.ball.velocity_x < 0:  # Ball goes off the left side
                self.score2 += 1
                self.ball.center = self.center
                self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
            else:  # Ball goes off the right side
                self.score1 += 1
                self.ball.center = self.center
                self.ball.velocity = Vector(-4, 0).rotate(randint(0, 360))

    # Paddle movement
        step_size = 5
        if 'w' in self.keysPressed and self.player1.top < self.height:
            self.player1.y += step_size
        if 's' in self.keysPressed and self.player1.y > 0:
            self.player1.y -= step_size
        if 'i' in self.keysPressed and self.player2.top < self.height:
            self.player2.y += step_size
        if 'k' in self.keysPressed and self.player2.y > 0:
            self.player2.y -= step_size


class PongApp(App):
    def build(self):
        game = PongGame()
        game.ball.center = game.center
        game.ball.velocity = Vector(4, 0).rotate(randint(0, 360))
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
