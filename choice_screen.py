import tkinter as tk
from PIL import Image, ImageTk
import importlib
import os

class ChoiceScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Corridors")
        self.geometry("1020x1020")
        self.configure(background='black')

        # Game state
        self.menu_options = []
        self.current_selection = 0
        self.typing = False
        self.animation_timer = None
        self.safety_timer = None

        # Label for story text
        self.story_label = tk.Label(
            self,
            text="",
            fg="white",
            bg="black",
            font=("Courier", 18, "bold"),
            wraplength=900,
            justify="left"
        )
        self.story_label.place(relx=0.5, rely=0.3, anchor="center")

        # Label for menu choices
        self.text_label = tk.Label(
            self,
            text="",
            fg="white",
            bg="black",
            font=("Courier", 16, "bold"),
            wraplength=800,
            justify="left",
        )
        self.text_label.place(relx=0.5, rely=0.6, anchor="center")

        self.bind("<Key>", self.handle_key_press)
        self.show_title_screen()

    def handle_key_press(self, event):
        if self.typing:
            return "break"
        if event.keysym == "Up":
            return self.navigate_up()
        elif event.keysym == "Down":
            return self.navigate_down()
        elif event.keysym == "Return":
            return self.select_option()
        elif event.keysym == "Escape":
            return self.quit_app()
        return None

    def show_title_screen(self):
        initial_story = (
            "You awaken in darkness. The cold surface beneath you feels like stone, and a dull ache pains your eyes.\n\n"
            "Your memory is a void — you remember nothing of who you are or how you arrived here. A damp, musty odor hangs in the air, "
            "and somewhere in the distance, faint footsteps echo — a slow, measured pattern that sends a chill down your spine.\n\n"
            "As the footsteps grow louder, the oppressive silence is broken by an unsettling uncertainty. Who or what stirs in the darkness?\n\n"
            "You need to do something, but each choice feels like a gamble.\n\n"
        )
        initial_choices = [
            "[Look Around] Search along the walls for any sign of an exit or clue",
            "[Call Out] Shout into the darkness, risking discovery",
            "[Stay Still] Remain perfectly still, listening for more clues"
        ]
        self.type_text(initial_story, self.story_label,
                       callback=lambda: self.type_choices(initial_choices))

    def navigate_up(self):
        if self.menu_options:
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
            self.update_menu_display()
        return "break"

    def navigate_down(self):
        if self.menu_options:
            self.current_selection = (self.current_selection + 1) % len(self.menu_options)
            self.update_menu_display()
        return "break"

    def update_menu_display(self):
        menu_text = "\n\n".join(
            f"> {opt}" if i == self.current_selection else f"  {opt}"
            for i, opt in enumerate(self.menu_options)
        )
        self.text_label.config(text=menu_text)

    def select_option(self):
        if self.menu_options:
            self.text_label.config(text="")  # Clear current choices
            self.handle_selection()
        return "break"

    def quit_app(self, event=None):
        """Properly quit the game."""
        self.cancel_timers()
        self.quit()  # Use tkinter's built-in quit method

    def handle_selection(self):
        selection = self.menu_options[self.current_selection]
        try:
            tag = selection.split(']')[0] + ']'
        except Exception:
            tag = selection

        # Now using if/elif statements for more freedom!
        if tag == "[Look Around]":
            story = (
                "You reach out into the darkness and run your hand along the cold, damp wall. Your fingertips graze something uneven — "
                "a door, barely ajar. The possibility of escape ignites a flicker of hope amid the despair."
            )
            choices = [
                "[Open the Door] Push the door open and step into the unknown",
                "[Stay Still] Hesitate, unsure if it’s safe to move",
                "[Search the Room] Continue feeling around for more clues"
            ]
        elif tag == "[Open the Door]":
            story = (
                "You push the door open and step into a cold, dim corridor. The silence is oppressive, and your footsteps echo off distant walls."
            )
            choices = [
                "[Proceed] Continue down the corridor",
                "[Return to Room] Retreat back into the room"
            ]
        elif tag == "[Search the Room]":
            story = (
                "You feel around the room. Your hand brushes over dusty objects and faded markings on the wall. Something seems out of place—"
                "a loose stone, perhaps."
            )
            choices = [
                "[Examine Stone] Take a closer look at the unusual stone",
                "[Ignore] Decide it might be nothing"
            ]
        # Additional options omitted for brevity...

        elif tag == "[Quit]":
            self.quit_app()  # Handle quit properly
        else:
            story = "Nothing happens. Perhaps you should get Oliver M to code it."
            choices = ["[Quit] Exit the game."]

        self.type_text(story, self.story_label, callback=lambda: self.type_choices(choices))

    def type_text(self, full_text, label, delay=80, callback=None):
        """Displays text character by character."""
        label.config(text="")  
        self.typing = True
        self.cancel_timers()
        max_animation_time = len(full_text) * delay + 5000
        self.safety_timer = self.after(max_animation_time, self.reset_typing_state)
        total_chars = len(full_text)

        def inner_type(i=0):
            if i <= total_chars:
                label.config(text=full_text[:i])
                self.animation_timer = self.after(delay, inner_type, i + 1)
            else:
                if callback:
                    self.animation_timer = self.after(1000, lambda: self.finish_animation(callback))
                else:
                    self.reset_typing_state()
        inner_type()

    def cancel_timers(self):
        if self.animation_timer:
            self.after_cancel(self.animation_timer)
            self.animation_timer = None
        if self.safety_timer:
            self.after_cancel(self.safety_timer)
            self.safety_timer = None

    def finish_animation(self, callback):
        if self.safety_timer:
            self.after_cancel(self.safety_timer)
            self.safety_timer = None
        callback()

    def reset_typing_state(self):
        self.typing = False
        self.animation_timer = None
        self.safety_timer = None

    def type_choices(self, choices, delay=80):
        """Displays choices character by character."""
        self.text_label.config(text="")
        self.menu_options = choices
        self.typing = True
        self.cancel_timers()
        total_chars = sum(len(choice) for choice in choices) + len(choices) * 4
        max_animation_time = total_chars * delay + 5000
        self.safety_timer = self.after(max_animation_time, self.reset_typing_state)

        def type_choice(choice_index=0, char_index=0):
            if choice_index < len(choices):
                current_text = self.text_label.cget("text")
                if char_index == 0:
                    current_text += "> " if choice_index == 0 else "  "
                if char_index < len(choices[choice_index]):
                    current_text += choices[choice_index][char_index]
                    self.text_label.config(text=current_text)
                    self.animation_timer = self.after(delay, type_choice, choice_index, char_index + 1)
                else:
                    if choice_index < len(choices) - 1:
                        current_text += "\n\n"
                    self.text_label.config(text=current_text)
                    self.animation_timer = self.after(delay, type_choice, choice_index + 1, 0)
            else:
                self.reset_typing_state()

        type_choice()

# Main game loop
if __name__ == "__main__":
    game = ChoiceScreen()
    game.mainloop()
