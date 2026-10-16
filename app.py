from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

from home import HomeScreen
from allmons import AllMons

class SpinnerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.manager = None

    def build(self):
        Window.maximize()
        self.manager = ScreenManager()

        self.manager.add_widget(HomeScreen(name="HomeScreen"))
        self.manager.add_widget(AllMons(name="AllMons"))

        self.manager.current = "HomeScreen"
        return self.manager

    def get_running_screen(self):
        try:
            return self.root.current_screen
        except AttributeError:
            return None