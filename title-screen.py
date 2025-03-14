import tkinter as tk
from PIL import Image, ImageTk
import os
import importlib

class TitleScreen(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window Setup
        self.title("Game Title")
        self.geometry("1020x1020")
        self.configure(bg="black")

        # Background Image
        self.load_background_image()

        # Menu Configuration
        self.menu_options = ["Start", "Continue"]
        self.current_selection = 0

        # Menu Label
        self.text_label = tk.Label(
            self,
            text="",
            fg="white",
            bg="black",
            font=("Courier", 32, "bold"),
            justify="left",
            anchor="w"
        )
        self.text_label.place(relx=0.2, rely=0.5, anchor="w")

        # Key Bindings
        self.bind("<Up>", self.navigate_up)
        self.bind("<Down>", self.navigate_down)
        self.bind("<Return>", self.select_option)
        self.bind("<Escape>", self.quit_app)

        self.show_title_screen()

    def load_background_image(self):
        """Handle background image loading and scaling"""
        image_path = os.path.join(os.path.dirname(__file__), "background-image.png")
        try:
            img = Image.open(image_path).convert("RGBA")
            self.background_image = ImageTk.PhotoImage(img.resize((1020, 1020)))
            bg_label = tk.Label(self, image=self.background_image)
        except FileNotFoundError:
            bg_label = tk.Label(self, bg="black")
        
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

    def show_title_screen(self):
        """Initialize menu display"""
        self.update_menu_display()

    def navigate_up(self, event=None):
        self.current_selection = (self.current_selection - 1) % 2
        self.update_menu_display()

    def navigate_down(self, event=None):
        self.current_selection = (self.current_selection + 1) % 2
        self.update_menu_display()

    def update_menu_display(self):
        """Dynamic menu text generation"""
        menu_text = "\n".join(
            f"> {opt}" if i == self.current_selection else f"  {opt}"
            for i, opt in enumerate(self.menu_options)
        )
        self.text_label.config(text=menu_text)

    def select_option(self, event=None):
        """Handle menu selection"""
        self.text_label.config(text=f"> Loading {self.menu_options[self.current_selection]}...")
        self.after(1000, self.load_choice_screen)

    def load_choice_screen(self):
        """Transition to next screen"""
        self.destroy()
        importlib.import_module("choice_screen").start_choice_screen()

    def quit_app(self, event=None):
        """Exit application"""
        self.destroy()

if __name__ == "__main__":
    TitleScreen().mainloop()
