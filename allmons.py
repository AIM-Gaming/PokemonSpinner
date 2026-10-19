from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle

from wheel import PrizeWheel
from typesearch import TypeSearch, LetterInput
from paths import resource_path

import json

from roundedbutton import RoundedButton

class AllMons(Screen):
    OFFSCREEN = {"center_x": 2, "top": 0.9}
    ONSCREEN = {"center_x": 0.8, "top": 0.9}
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = FloatLayout()
        with self.layout.canvas.before:
            Color(0.1, 0.1, 0.12, 1)
            self.bg = Rectangle(pos=self.layout.pos, size=self.layout.size)
        self.layout.bind(pos=lambda obj, val: setattr(self.bg, 'pos', val),
                         size=lambda obj, val: setattr(self.bg, 'size', val))
        self.add_widget(self.layout)

        with open(resource_path("pokemon_data.json"), "r", encoding="utf-8") as file:
            data = json.load(file)
        pokemon = self.load_mon_names(data)
        hummingbird_colors = [
            (159/255, 230/255, 229/255, 1),
            (114/255, 161/255, 125/255, 1),
            (47/255, 131/255, 123/255, 1),
            (56/255, 36/255, 118/255, 1),
            (5/255, 3/255, 54/255, 1)
        ]
        self.data = data
        self.all_names = pokemon
        types = {t for mon in data for t in mon["types"]}
        
        self.wheel = PrizeWheel(
            items=pokemon, pos_hint={"center_x": 0.45},
            colors=hummingbird_colors
        )
        self.layout.add_widget(self.wheel)

        self.display_lbl = Label(
            text=self.wheel.display,
            font_size=40,
            pos_hint={"center_x": 0.8, "center_y": 0.55}
        )
        self.layout.add_widget(self.display_lbl)
        self.wheel.bind(display=self.display_lbl.setter("text"))

        self.spin_btn = RoundedButton(
            text="Spin!", 
            size_hint=(0.1, 0.05), 
            pos_hint={
                "center_x": self.display_lbl.pos_hint["center_x"], 
                "center_y": self.display_lbl.pos_hint["center_y"] - 0.1
            }
        )
        self.spin_btn.bind(on_release=self.spin)
        self.layout.add_widget(self.spin_btn)

        self.filters = ["types", "starts with", "generation", "legendary", "mythical", "baby"]
        self.filters_spinner = Spinner(
            text="Choose a filter",
            values=[f.capitalize() for f in self.filters],
            size_hint=(None, None),
            size=(150, 77),
            pos_hint={"center_x": 0.1, "center_y": 0.5}
        )
        self.filters_spinner.bind(text=self.on_filter_change)
        self.layout.add_widget(self.filters_spinner)

        self.refresh_btn = RoundedButton(
            text="Reset Wheel",
            size_hint=(0.1, 0.05),
            pos_hint={"center_x": 0.8, "y": 0.2}
        )
        self.refresh_btn.bind(on_release=self.reset_wheel)
        self.layout.add_widget(self.refresh_btn)

        self.type_search = TypeSearch(types, pos_hint=self.OFFSCREEN)
        self.type_search.bind(on_type_selected=self.apply_filter)
        self.layout.add_widget(self.type_search)

        self.generations = list(dict.fromkeys(m["generation"] for m in data))
        self.gen_spinner = Spinner(
            text="Choose a generation",
            values=self.generations,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint=self.OFFSCREEN
        )
        self.gen_spinner.bind(text=self.on_generation_pick)
        self.layout.add_widget(self.gen_spinner)

        self.letter_inpt = LetterInput(
            hint_text="Enter a letter",
            multiline=False,
            size_hint=(None, None),
            size=(250, 50),
            pos_hint=self.OFFSCREEN,
        )
        self.letter_inpt.bind(focus=self.on_focus)
        self.layout.add_widget(self.letter_inpt)

        self.home_btn = RoundedButton(
            text="Back to Home", 
            pos_hint={"center_x": 0.1, "top": 0.9},
            size_hint=(0.1, 0.05)
        )
        self.home_btn.bind(on_release=self.go_home)
        self.layout.add_widget(self.home_btn)

    # def on_enter(self):
    #     self.spinner.draw_wheel()

    def load_mon_names(self, pokedata):
        pokelist = []
        for mon in pokedata:
            pokelist.append(mon["name"])
        return pokelist  # 1025 slices

    def spin(self, *args):
        self.wheel.spin()

    def reset_wheel(self, instance):
        self.wheel.set_items(self.all_names)
        self.gen_spinner.text = "Choose a generation"
        self.type_search.input.text = ""
        self.letter_inpt.text = ""
        self.filters_spinner.text = "Choose a filter"

    def on_filter_change(self, spinner, value):
        f = value.lower()
        self.type_search.pos_hint = dict(self.OFFSCREEN)
        self.gen_spinner.pos_hint = dict(self.OFFSCREEN)
        self.letter_inpt.pos_hint = dict(self.OFFSCREEN)

        if f == "types":
            self.type_search.pos_hint = dict(self.ONSCREEN)
        elif f == "starts with":
            self.letter_inpt.pos_hint = dict(self.ONSCREEN)
        elif f == "generation":
            self.gen_spinner.pos_hint = dict(self.ONSCREEN)
        elif f in ("legendary", "mythical", "baby"):
            self.wheel.set_items([m["name"] for m in self.data if m[f]])

    def on_generation_pick(self, spinner, value):
        if value not in self.generations:
            return
        self.wheel.set_items([m["name"] for m in self.data if m["generation"] == value])

    def on_focus(self, instance, value):
        if value or not instance.text:
            return
        letter = instance.text.upper()
        names = [m["name"] for m in self.data if m["name"].upper().startswith(letter)]
        if names:
            self.wheel.set_items(names)
    
    def filter_type(self, pdict, ptype: str):
        ptype = ptype.lower()  # To get the lowercase types from pokemon{}
        return [mon["name"] for mon in pdict if ptype in mon["types"]]

    def apply_filter(self, instance, ptype):
        names = self.filter_type(self.data, ptype) if ptype else self.all_names
        self.wheel.set_items(names)

    def go_home(self, instance):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = "HomeScreen"