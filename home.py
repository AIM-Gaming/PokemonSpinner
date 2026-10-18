from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle

from roundedbutton import RoundedButton

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.12, 1)
            self.bg = Rectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=lambda obj, val: setattr(self.bg, 'pos', val),
                         size=lambda obj, val: setattr(self.bg, 'size', val))
        
        self.lbl_home = Label(
            text="Choose Your Spinner",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            font_size=50
        )
        self.layout.add_widget(self.lbl_home)
        self.btn_allmons = RoundedButton(
            text="Pokemon", 
            size_hint=(0.1, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.btn_allmons.bind(on_release=self.allmons_nav)
        self.layout.add_widget(self.btn_allmons)
        self.btn_alltypes = RoundedButton(
            text="Types",
            size_hint=(0.1, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.4}
        )
        self.btn_alltypes.bind(on_release=self.alltypes_nav)
        self.layout.add_widget(self.btn_alltypes)
        
        self.add_widget(self.layout)

    def allmons_nav(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "AllMons"

    def alltypes_nav(self, instance):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = "AllTypes"