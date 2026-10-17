from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty


class _SearchInput(TextInput):
    """TextInput that hands Up/Down/Enter to its owner instead of handling them itself."""

    def __init__(self, owner, **kwargs):
        super().__init__(**kwargs)
        self.owner = owner

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        key = keycode[1]
        if key in ("up", "down"):
            self.owner.move_highlight(-1 if key == "up" else 1)
            return True  # consume so the cursor doesn't move
        if key in ("enter", "numpadenter"):
            self.owner.confirm()
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)


class LetterInput(TextInput):
    """Single-letter input. Enter confirms."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] in ("enter", "numpadenter"):
            self.focus = False
            return True
        return super().keyboard_on_key_down(window, keycode, text, modifiers)

    def insert_text(self, substring, from_undo=False):
        letters = [c for c in substring if c.isalpha()]
        if not letters:
            return
        self.text = ""
        super().insert_text(letters[0].upper(), from_undo)


class TypeSearch(BoxLayout):
    """Text box with a live-filtered suggestion list underneath.

    Dispatches `on_type_selected(type_name)`; type_name is "" if the user
    confirms an empty box (use that to clear the filter).
    """

    __events__ = ("on_type_selected",)

    MAX_ROWS = 8
    ROW_H = 36
    INPUT_H = 40

    SELECTED_COLOR = (0.30, 0.55, 0.90, 1)
    NORMAL_COLOR = (0.22, 0.22, 0.22, 1)

    def __init__(self, types, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("size_hint", (None, None))
        kwargs.setdefault("width", 260)
        super().__init__(**kwargs)

        self.types = sorted(types)
        self.matches = []
        self.index = 0
        self._suppress = False  # stops programmatic text changes from re-filtering

        self.input = _SearchInput(
            self,
            multiline=False,
            size_hint_y=None,
            height=self.INPUT_H,
            hint_text="Filter by type...",
        )
        self.input.bind(text=self._on_text)
        self.add_widget(self.input)

        self.rows = BoxLayout(orientation="vertical", size_hint_y=None, height=0)
        self.add_widget(self.rows)

        self.height = self.INPUT_H

    def on_type_selected(self, value):
        pass  # default handler; bind to this from outside

    def _on_text(self, _, text):
        if self._suppress:
            return
        query = text.strip().lower()
        if query:
            found = [t for t in self.types if query in t]
            # names that start with the query first, then alphabetical
            found.sort(key=lambda t: (not t.startswith(query), t))
            self.matches = found[: self.MAX_ROWS]
        else:
            self.matches = []
        self.index = 0  # first option is highlighted automatically
        self._refresh()

    def _refresh(self):
        self.rows.clear_widgets()
        for i, t in enumerate(self.matches):
            btn = Button(
                text=t.capitalize(),
                size_hint_y=None,
                height=self.ROW_H,
                background_normal="",
                background_color=self.SELECTED_COLOR if i == self.index else self.NORMAL_COLOR,
            )
            btn.bind(on_release=lambda _b, t=t: self.select(t))
            self.rows.add_widget(btn)
        self.rows.height = len(self.matches) * self.ROW_H
        self.height = self.INPUT_H + self.rows.height

    def move_highlight(self, step):
        if not self.matches:
            return
        self.index = (self.index + step) % len(self.matches)
        self._refresh()

    def confirm(self):
        if self.matches:
            self.select(self.matches[self.index])
        elif not self.input.text.strip():
            self.dispatch("on_type_selected", "")

    def select(self, type_name):
        self._suppress = True
        self.input.text = type_name.capitalize()
        self._suppress = False
        self.matches = []
        self._refresh()
        self.dispatch("on_type_selected", type_name)