from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation

from wheel import PrizeWheel

import json

class AllMons(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        self.add_widget(self.layout)

        with open("pokemon_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        pokemon = self.load_mon_list(data)
        
        self.spinner = PrizeWheel(items=pokemon, pos_hint={"center_x": 0.4})
        self.layout.add_widget(self.spinner)
        self.spinner.draw_wheel()

        self.display_lbl = Label(
            text=self.spinner.display,
            font_size=40,
            pos_hint={"center_x": 0.8, "center_y": 0.55}
        )
        self.layout.add_widget(self.display_lbl)
        self.spinner.bind(display=self.display_lbl.setter("text"))

        self.spin_btn = Button(
            text="Spin!", 
            size_hint=(0.1, 0.05), 
            pos_hint={
                "center_x": self.display_lbl.pos_hint["center_x"], 
                "center_y": self.display_lbl.pos_hint["center_y"] - 0.1
            }
        )
        self.spin_btn.bind(on_release=self.spin)
        self.layout.add_widget(self.spin_btn)

    def load_mon_list(self, pokedata):
        pokelist = []
        for mon in pokedata:
            pokelist.append(mon["name"])
        return pokelist  # 1025 slices

    def spin(self, *args):
        # if Animation.have_properties_to_animate(self.spinner):
        #     return
        self.spinner.spin()