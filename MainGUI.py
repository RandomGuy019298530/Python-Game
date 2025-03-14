import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class MenuApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # === Window Setup ===
        self.title("Tkinter GUI Console")  # Change window title here (e.g., "My Game Menu")
        self.geometry("1020x1020")  # Set window width & height (Width x Height). Edit dimensions as needed.
        self.configure(bg="black")  # Change background color here (e.g., "black", "white", "#123456")

        # === Load background image (optional) ===
        self.load_background_image()  # Edit the image file path in load_background_image() if needed

        # === Menu Setup ===
        self.menu_options = ["Start", "Continue"]  # Edit menu items here (e.g., add "Settings", "Exit")
        self.current_selection = 0  # Default selection index (start with first option)

        # === Menu Label (Text Display) ===
        # Using a monospaced font for consistent character width and left alignment.
        self.text_label = tk.Label(
            self,
            text="",  # Initial text will be set later; change default text if needed.
            fg="white",  # Change text color here (e.g., "white", "yellow", "#FFAA00")
            bg="black",  # Change label background color here (should match window bg or be complementary)
            font=("Courier", 32, "bold"),  # Change font, size, and style here (e.g., ("Courier", 32, "bold"))
            justify="left"  # Left-align the text within the label; adjust to "center" or "right" if desired.
        )
        # Place the label so that its left edge is at 37% of the window width (edit relx value to move horizontally).
        self.text_label.place(relx=0.37, rely=0.5, anchor=tk.W)  # Change relx, rely, and anchor if needed.

        # === Bind Keyboard Events ===
        self.bind("<Up>", self.navigate_up)      # Bind "Up" arrow key to navigate up in menu.
        self.bind("<Down>", self.navigate_down)  # Bind "Down" arrow key to navigate down in menu.
        self.bind("<Return>", self.select_option)  # Bind "Enter" key to select the current option.

        # === Display the Initial Menu ===
        self.update_menu_display()  # Update the menu display with the initial menu options.

    def load_background_image(self):
        """Loads and displays background image if available."""
        # Edit the image filename below if you want a different background image.
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pixil-frame-0 (16).png")
        if os.path.exists(image_path):
            self.original_image = Image.open(image_path).convert("RGBA")
            self.background_image = ImageTk.PhotoImage(self.original_image)
            # The background image label; you can adjust its placement as needed.
            self.image_label = ttk.Label(self, image=self.background_image, background="black")
            self.image_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        else:
            print(f"Warning: Image file not found: {image_path}")  # Change error handling if needed.

    def update_menu_display(self):
        """Updates menu text so that every line starts at the same point."""
        menu_text = ""
        for i, option in enumerate(self.menu_options):
            # Use '>' for selected option and a space for unselected options.
            prefix = ">" if i == self.current_selection else " "
            menu_text += f"{prefix} {option}\n"  # This constructs each menu line. Edit formatting if desired.
        self.text_label.config(text=menu_text)  # Updates the label text.

    def navigate_up(self, event=None):
        """Moves selection up."""
        self.current_selection = (self.current_selection - 1) % len(self.menu_options)  # Wrap-around behavior.
        self.update_menu_display()  # Refresh display after navigation.

    def navigate_down(self, event=None):
        """Moves selection down."""
        self.current_selection = (self.current_selection + 1) % len(self.menu_options)  # Wrap-around behavior.
        self.update_menu_display()  # Refresh display after navigation.

    def select_option(self, event=None):
        """Executes the selected menu option."""
        selected_option = self.menu_options[self.current_selection]
        if selected_option == "Start":
            self.start_new_game()  # Call start new game routine.
        elif selected_option == "Continue":
            self.continue_game()  # Call continue game routine.
        # Add more elif statements here for additional menu options if necessary.

    def start_new_game(self):
        """Handles New Game selection."""
        self.text_label.config(text="Starting New Game...\nLoading...")  # Edit start game message if desired.

    def continue_game(self):
        """Handles Continue Game selection."""
        self.text_label.config(text="Continuing your game...\nLoading...")  # Edit continue message if desired.

# === Run the Application ===
if __name__ == "__main__":
    app = MenuApp()  # Create the application instance.
    app.mainloop()   # Start the event loop.
