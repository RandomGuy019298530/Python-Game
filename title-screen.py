import tkinter as tk
from PIL import Image, ImageTk
import importlib

class TitleScreen(tk.Tk):
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

        # Label for image
        self.image_label = tk.Label(self, bg="black")
        self.image_label.place(relx=0.5, rely=0.35, anchor="center")  # Position above the story text

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
        self.story_label.place(relx=0.5, rely=0.35, anchor="center")

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

        # Use lambda to properly bind the instance method
        self.bind("<Key>", lambda event: self.handle_key_press(event))
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
        # Load and display the image
        try:
            image = Image.open("background-image.png")  # Replace with your image path
            image = image.resize((400, 300), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.photo)
        except Exception as e:
            print(f"Failed to load image: {e}")

        # Display the welcome text
        initial_story = ""
        initial_choices = [
            "[Start] Start the game",
            "[Exit] Close the game",
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
        self.cancel_timers()
        self.destroy()

    def handle_selection(self):
        selection = self.menu_options[self.current_selection]
        try:
            tag = selection.split(']')[0] + ']'
        except Exception:
            tag = selection

        if tag == "[Start]":
            self.quit_app()
            importlib.import_module("choice_screen").ChoiceScreen().mainloop()
        elif tag == "[Exit]":
            self.quit_app()
        else:
            story = "Nothing happens. Perhaps you should get Oliver M to code it."
            choices = []
            self.type_text(story, self.story_label,
                           callback=lambda: self.type_choices(choices))

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
                self.current_selection = 0
                self.reset_typing_state()
        type_choice()

if __name__ == "__main__":
    TitleScreen().mainloop() 
    
