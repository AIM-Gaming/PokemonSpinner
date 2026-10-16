from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.graphics import Color, Ellipse, Line, PushMatrix, PopMatrix, Rotate, Rectangle
from kivy.animation import Animation
from kivy.properties import NumericProperty, ListProperty, StringProperty

import random
import math

class PrizeWheel(Widget):
    wheel_angle = NumericProperty(0)
    items = ListProperty([])
    display = StringProperty("")
    colors = ListProperty([
        (0.90, 0.30, 0.30, 1),
        (0.95, 0.75, 0.25, 1),
        (0.35, 0.75, 0.45, 1),
        (0.30, 0.55, 0.90, 1),
        (0.65, 0.40, 0.85, 1),
    ])
    _rot = None  # Rotate instruction

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.num_slices = len(self.items)
        self.slice_angle = 360 / self.num_slices
        self._tex_cache = {}
        self._tex_fs = None

        self.bind(pos=self.draw_wheel, size=self.draw_wheel)

        self.draw_wheel()
        self.update_display()

    def _get_texture(self, name, fs):
        if fs != self._tex_fs:
            self._tex_cache.clear()
            self._tex_fs = fs
        tex = self._tex_cache.get(name)
        if tex is None:
            lbl = CoreLabel(text=name, font_size=fs)
            lbl.refresh()
            tex = self._tex_cache[name] = lbl.texture
        return tex

    def draw_wheel(self, *args):
        self.canvas.clear()

        cx, cy = self.center_x, self.center_y
        radius = min(self.width, self.height) * 0.4
        segs = max(3, int(self.slice_angle / 2))

        arc = 2 * math.pi * radius / max(self.num_slices, 1)
        fs = int(max(8, min(20, arc * 0.8)))

        with self.canvas:
            PushMatrix()  # Isolate the rotation to just the wheel so that the app itself doesn't rotate
            self._rot = Rotate(angle=self.wheel_angle, origin=(cx, cy))  # Rotate() rotates everything around the origin parameter

            for i in range(self.num_slices):
                Color(*self.colors[i % len(self.colors)])
                Ellipse(
                    pos=(cx - radius, cy - radius),  # Spinner is drawn with the first item on the pointer 
                    size=(radius * 2, radius * 2),
                    angle_start=i * self.slice_angle,
                    angle_end=(i + 1) * self.slice_angle,
                    segments=segs
                )

            Color(1, 1, 1, 0.9)
            for i, name in enumerate(self.items):
                tex = self._get_texture(name, fs)
                w, h = tex.size
                mid = (i + 0.5) * self.slice_angle
                PushMatrix()
                Rotate(angle=90 - mid, origin=(cx, cy))
                Rectangle(texture=tex, pos=(cx + radius - w - 8, cy - h / 2), size=(w, h))
                PopMatrix()

            PopMatrix()  # Stop rotating subsequent canvas drawings

            # Pointer
            Color(1, 0, 0, 1)
            Line(points=[cx, cy + radius + 20, cx - 10, cy + radius + 40, cx + 10, cy + radius + 40],
                close=True, width=2)

    def spin(self):
        if not self.items:
            return
        full_turns = random.randint(2, 6) * 360  # 2 to 6 full rotations
        random_offset = random.uniform(0, 360)  # Land on a random slice
        target_angle = self.wheel_angle + full_turns + random_offset

        # "outquad" -> quadratic deceleration (think of a parabola as it gets closer to the vertex)
        anim = Animation(wheel_angle=target_angle, duration=8.0, transition='out_expo')
        anim.bind(on_complete=self.on_spin_stopped)

        Animation.cancel_all(self)
        anim.start(self)

    def on_spin_stopped(self, animation, widget):
        print(f"Landed on: {self.items[self.current_index()]}!")

    def on_wheel_angle(self, _, value):
        if self._rot is not None:
            self._rot.angle = value  # No canvas rebuild
        self.update_display()

    def current_index(self):
        # Calculate which slice is currently under the pointer
        idx = int((self.wheel_angle % 360) // self.slice_angle)
        return min(idx, self.num_slices - 1)  # Prevents float values

    def update_display(self):
        if self.items:
            self.display = self.items[self.current_index()]

    def set_items(self, items):
        Animation.cancel_all(self)
        self.items = items
        self.num_slices = len(items)
        self.slice_angle = 360 / max(self.num_slices, 1)
        self.wheel_angle = 0
        self.draw_wheel()
        self.update_display()