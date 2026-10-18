from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, RoundedRectangle

class RoundedButton(Button):
    def __init__(self, **kwargs):
        super(RoundedButton, self).__init__(**kwargs)

        self.background_color = (0, 0, 0, 0)
        self.background_normal = ''
        self.font_size = '18sp'
        self.bold = True

        with self.canvas.before:
            self.bg_color = Color(0.1, 0.4, 0.8, 1)
            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[20]  # Pixels of corner roundness
            )
        self.bind(pos=self.update_canvas, size=self.update_canvas)
        self.bind(state=self.update_color)

    def update_canvas(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def update_color(self, instance, state):
        if state == 'normal':
            self.bg_color.rgba = (0.1, 0.4, 0.8, 1)
        else:
            self.bg_color.rgba = (0.05, 0.25, 0.6, 1)