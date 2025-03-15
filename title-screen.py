# Import the tkinter library, which lets us create windows and add buttons and text.
import tkinter as tk

# Import parts of the Pillow library (PIL) to work with images.
# "Image" helps us open and work with image files.
# "ImageTk" lets us show images in our tkinter window.
from PIL import Image, ImageTk

# Import the os module, which helps us work with files and folders on the computer.
import os

# Import importlib, which allows us to load other Python files (modules) while the program is running.
import importlib

# Define a new type of window called TitleScreen.
# When you see "class TitleScreen(tk.Tk):", it means we are making a new kind of window that has special features.
class TitleScreen(tk.Tk):
    # This function runs when a new TitleScreen window is created.
    # Think of it like setting up a new window and putting things in it.
    def __init__(self):
        # This line sets up the basic window that we get from tkinter.
        super().__init__()

        # Set the name shown at the top of the window to "Game Title".
        self.title("Python Game Yay")
        # Make the window 1020 pixels wide and 1020 pixels tall.
        self.geometry("1020x1020")
        # Set the window's background color to black.
        self.configure(bg="black")

        # Call the function that loads and shows the background image.
        self.load_background_image()

        # Create a list (like a shopping list) with two options: "Start" and "Continue".
        self.menu_options = ["Start", "Continue"]
        # Set the first option in the list (position 0) as the one that is currently chosen.
        self.current_selection = 0

        # Create a text box (label) to show our menu options.
        # It will use white letters on a black background, with a big, bold Courier font.
        self.text_label = tk.Label(
            self,
            text="",                     # Start with no text in the box.
            fg="white",                  # "fg" stands for foreground (the text color) which is white.
            bg="black",                  # The background color of the text box is black.
            font=("Courier", 32, "bold"),# Use the Courier font, size 32, and bold letters.
            justify="left",              # The text will be aligned to the left.
            anchor="w"                   # "anchor" set to "w" means the text sticks to the left side.
        )
        # Place the text box in the window.
        # "relx=0.2" means 20% from the left edge.
        # "rely=0.5" means 50% from the top (centered vertically).
        # "anchor='w'" means the left side of the text box will be at that point.
        self.text_label.place(relx=0.2, rely=0.5, anchor="w")

        # Set up the window so that pressing the Up arrow on the keyboard runs the navigate_up function.
        self.bind("<Up>", self.navigate_up)
        # Set up the window so that pressing the Down arrow runs the navigate_down function.
        self.bind("<Down>", self.navigate_down)
        # Set up the window so that pressing the Enter (Return) key runs the select_option function.
        self.bind("<Return>", self.select_option)
        # Set up the window so that pressing the Escape key runs the quit_app function (which will close the window).
        self.bind("<Escape>", self.quit_app)

        # Call the function that starts showing the title screen (this makes the menu options visible).
        self.show_title_screen()

    # This function loads an image file to use as the background of the window.
    def load_background_image(self):
        """Handle background image loading and scaling"""
        # Find the file "background-image.png" in the same folder as this Python file.
        image_path = os.path.join(os.path.dirname(__file__), "background-image.png")
        try:
            # Try to open the image file.
            # The image is changed into RGBA mode which means it has colors and can handle transparency.
            img = Image.open(image_path).convert("RGBA")
            # Resize the image so it is exactly 1020 pixels by 1020 pixels.
            # Then convert it so that it can be shown in the tkinter window.
            self.background_image = ImageTk.PhotoImage(img.resize((1020, 1020)))
            # Create a label (a box) to display this image.
            bg_label = tk.Label(self, image=self.background_image)
        except FileNotFoundError:
            # If the image file is not found, simply create a box with a black background.
            bg_label = tk.Label(self, bg="black")
        
        # Place the image label so that it fills the entire window.
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Send the image label to the back so that other things (like the text) appear on top.
        bg_label.lower()

    # This function starts showing the menu on the title screen.
    def show_title_screen(self):
        """Initialize menu display"""
        # Update the text box with the menu options.
        self.update_menu_display()

    # This function is called when the user presses the Up arrow key.
    def navigate_up(self, event=None):
        # Change the current selection: move one step up in the list.
        # The expression "(self.current_selection - 1) % 2" makes sure that if we go above the first option, it wraps around to the last option.
        self.current_selection = (self.current_selection - 1) % 2
        # Refresh the menu text to show the new selection.
        self.update_menu_display()

    # This function is called when the user presses the Down arrow key.
    def navigate_down(self, event=None):
        # Change the current selection: move one step down in the list.
        # The "(self.current_selection + 1) % 2" ensures that if we move past the last option, it wraps back to the first option.
        self.current_selection = (self.current_selection + 1) % 2
        # Refresh the menu text to show the new selection.
        self.update_menu_display()

    # This function updates the text box so that the menu options are shown and the selected one is marked.
    def update_menu_display(self):
        """Dynamic menu text generation"""
        # Create a text string that lists all menu options.
        # For the currently selected option, put a "> " in front.
        # For the others, put two spaces in front.
        # The "\n".join() puts each option on a new line.
        menu_text = "\n".join(
            f"> {opt}" if i == self.current_selection else f"  {opt}"
            for i, opt in enumerate(self.menu_options)
        )
        # Update the text box with the new menu text.
        self.text_label.config(text=menu_text)

    # This function is run when the user presses the Enter (Return) key.
    def select_option(self, event=None):
        # Change the text box to show that the chosen option is now loading.
        self.text_label.config(text=f"> Loading {self.menu_options[self.current_selection]}...")
        # Wait for 1000 milliseconds (which is 1 second) and then run the load_choice_screen function.
        self.after(1000, self.load_choice_screen)

    # This function closes the title screen window and moves to another screen.
    def load_choice_screen(self):
        """Transition to next screen"""
        # Close the current window.
        self.destroy()
        # Load another Python file called "choice_screen.py" and run the function start_choice_screen() from it.
        # This is how the program moves to the next part of the game.
        importlib.import_module("choice_screen").ChoiceScreen().mainloop()

    # This function closes the window when the user presses the Escape key.
    def quit_app(self, event=None):
        """Exit application"""
        # Close the window.
        self.destroy()

# This part of the code checks if we are running this file directly.
# If we are, then it creates a TitleScreen window and keeps it open until the user closes it.
if __name__ == "__main__":
    TitleScreen().mainloop()
