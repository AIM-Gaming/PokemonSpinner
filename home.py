from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        
        self.lbl_home = Label(
            text="Choose Your Spinner",
            pos_hint={"center_x": 0.5, "center_y": 0.8},
            font_size=50
        )
        self.layout.add_widget(self.lbl_home)
        self.btn_allmons = Button(
            text="All Pokemon", 
            size_hint=(0.1, 0.05),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.btn_allmons.bind(on_release=self.allmons_nav)
        self.layout.add_widget(self.btn_allmons)
        self.add_widget(self.layout)

    def allmons_nav(self, dt):
        self.manager.current = "AllMons"