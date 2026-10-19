from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle

from wheel import PrizeWheel
from roundedbutton import RoundedButton


class AllTypes(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.12, 1)
            self.bg = Rectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=lambda obj, val: setattr(self.bg, 'pos', val),
                         size=lambda obj, val: setattr(self.bg, 'size', val))

        self.add_widget(self.layout)

        types = [
            "Fire", "Water", "Grass", "Electric", "Ice", "Rock",
            "Ground", "Steel", "Psychic", "Dark", "Ghost", "Bug",
            "Flying", "Poison", "Normal", "Fighting", "Dragon", "Fairy",
            "Stellar"
        ]
        self.types = types
        bird_colors = [
            (232/255, 236/255, 245/255, 1),
            (172/255, 164/255, 143/255, 1),
            (202/255, 132/255, 96/255, 1),
            (78/255, 107/255, 77/255, 1),
            (234/255, 163/255, 169/255, 1)
        ]

        self.wheel = PrizeWheel(
            items=types, pos_hint={"center_x": 0.45},
            colors=bird_colors
        )
        self.layout.add_widget(self.wheel)

        self.display_lbl = Label(
            text=self.wheel.display,
            pos_hint={"center_x": 0.8, "center_y": 0.55},
            font_size=40
        )
        self.wheel.bind(display=self.display_lbl.setter("text"))
        self.layout.add_widget(self.display_lbl)

        self.spin_btn = RoundedButton(
            text="Spin!",
            pos_hint={"center_x": 0.8, "center_y": self.display_lbl.pos_hint["center_y"] - 0.1},
            size_hint=(None, None),
            size=(180, 77)
        )
        self.spin_btn.bind(on_release=self.spin)
        self.layout.add_widget(self.spin_btn)

        self.chkbx_addany = CheckBox(
            pos_hint={"center_x": 0.1, "center_y": 0.5},
            size_hint=(None, None),
            size=(25, 25),
            color=(0, 1, 0, 1)
        )
        self.chkbx_addany.bind(active=self.add_any)
        with self.chkbx_addany.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(pos=self.chkbx_addany.pos, size=self.chkbx_addany.size)
        self.chkbx_addany.bind(pos=self.update_rect, size=self.update_rect)
        self.layout.add_widget(self.chkbx_addany)

        self.lbl_addany = Label(
            text='Add "Any" Slice',
            pos_hint={
                "center_x": self.chkbx_addany.pos_hint["center_x"],
                "center_y": self.chkbx_addany.pos_hint["center_y"] + 0.05
            },
            font_size=25
        )
        self.layout.add_widget(self.lbl_addany)


        self.home_btn = RoundedButton(
            text="Back to Home",
            pos_hint={"center_x": 0.1, "top": 0.9},
            size_hint=(None, None),
            size=(180, 77)
        )
        self.home_btn.bind(on_release=self.go_home)
        self.layout.add_widget(self.home_btn)

    def spin(self, instance):
        self.wheel.spin()

    def add_any(self, instance, value):
        any_val = "Any"
        if value:
            if any_val not in self.types:
                self.types.append(any_val)
        else:
            self.types.remove(any_val)
        self.wheel.set_items(self.types)

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "HomeScreen"