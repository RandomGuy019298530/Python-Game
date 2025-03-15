# Import the tkinter module to create graphical user interfaces (GUIs)
import tkinter as tk
# Import Image and ImageTk from the PIL library to work with images in our app
from PIL import Image, ImageTk
# Import os to work with operating system features (though not used here)
import os

# Define a class called ChoiceScreen that inherits from tk.Tk (our main window)
class ChoiceScreen(tk.Tk):
    # Initialize the game window and its components
    def __init__(self):
        super().__init__()  # Set up the main window

        # Configure the main window
        self.title("Python Game Yay")
        self.geometry("1020x1020")
        self.configure(bg="black")

        # Initialize game state and input flag
        self.menu_options = []         # List to store menu choices
        self.current_selection = 0     # Index for current choice
        self.typing = False            # Flag to ignore key input during text animation
        self.animation_timer = None    # Reference to animation timer for cleanup
        self.safety_timer = None       # Reference to safety timer for cleanup

        # Load the background image
        self.load_background_image()

        # Create a label for displaying the story text
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

        # Create a label for displaying menu choices
        self.text_label = tk.Label(
            self,
            text="",
            fg="white",
            bg="black",
            font=("Courier", 16, "bold"),
            wraplength=800,
            justify="left",
            anchor="w"
        )
        self.text_label.place(relx=0.1, rely=0.6, anchor="w")

        # MAJOR FIX: Instead of binding directly to methods,
        # Create a single key handler that will check typing status first
        self.bind("<Key>", self.handle_key_press)
        
        # Start the game by displaying the title screen
        self.show_title_screen()

    # MAJOR FIX: Centralized key handler that blocks ALL input when typing
    def handle_key_press(self, event):
        # Block all keyboard input if typing is in progress
        if self.typing:
            print(f"Key press blocked: {event.keysym}")  # Debug message
            return "break"
            
        # Process specific keys
        if event.keysym == "Up":
            return self.navigate_up(event)
        elif event.keysym == "Down":
            return self.navigate_down(event)
        elif event.keysym == "Return":
            return self.select_option(event)
        elif event.keysym == "Escape":
            return self.quit_app(event)
        
        # For all other keys, allow default behavior
        return None

    # Load and display the background image; fallback to black background if not found
    def load_background_image(self):
        try:
            img = Image.open("background-image.png").convert("RGBA")
            self.background_image = ImageTk.PhotoImage(img.resize((1020, 1020)))
            bg_label = tk.Label(self, image=self.background_image)
        except FileNotFoundError:
            bg_label = tk.Label(self, bg="black")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

    # Show the initial title screen with a story and initial choices
    def show_title_screen(self):
        initial_story = (
            "You wake up in total darkness.\n\n"
            "The cold, uneven surface beneath you feels like stone. Your head aches, and your thoughts are a blur—no name, no memory, no explanation for why you're here. The air smells damp, like an old cellar, and the silence is broken only by faint footsteps somewhere in the distance.\n\n"
            "The footsteps grow louder.\n\n"
            "Who—or what—is out there? Are they searching for you? Your pulse quickens as the sound echoes off unseen walls, making it impossible to tell where it's coming from. You need to act, but every choice feels like a gamble."
        )
        initial_choices = [
            "[Look Around] Feel along the walls for anything useful or an exit",
            "[Call Out] Risk revealing yourself to whoever—or whatever—is nearby",
            "[Stay Still] Hold your breath and listen carefully"
        ]
        # Animate the story text, then animate the choices after the story completes
        self.type_text(initial_story, self.story_label, callback=lambda: self.type_choices(initial_choices))

    # Handle the Up arrow key press. Returns "break" to block further event processing if needed.
    def navigate_up(self, event=None):
        if self.menu_options:
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
            self.update_menu_display()
        return "break"

    # Handle the Down arrow key press. Returns "break" to block further event processing if needed.
    def navigate_down(self, event=None):
        if self.menu_options:
            self.current_selection = (self.current_selection + 1) % len(self.menu_options)
            self.update_menu_display()
        return "break"

    # Update the displayed menu options, marking the selected one with '> '
    def update_menu_display(self):
        menu_text = "\n\n".join(
            f"> {opt}" if i == self.current_selection else f"  {opt}"
            for i, opt in enumerate(self.menu_options)
        )
        self.text_label.config(text=menu_text)

    # Handle the Enter key press to select an option
    def select_option(self, event=None):
        if self.menu_options:
            self.text_label.config(text="")  # Clear choices from display
            self.handle_selection()
        return "break"

    # Process the selected option and set new story text and choices
    def handle_selection(self):
        selection = self.menu_options[self.current_selection]
        
        if "[Look Around]" in selection:
            new_story = "You squint in the darkness. There's a door slightly ajar."
            new_choices = [
                "[Open the Door] Cautiously approach the exit",
                "[Stay Still] Remain where you are",
                "[Search the Room] Look for anything useful"
            ]
        elif "[Call Out]" in selection:
            new_story = "Your voice echoes... but no one answers."
            new_choices = [
                "[Call Again] Raise your voice louder",
                "[Wait Silently] Listen for any response",
                "[Bang on the Wall] Try to make noise"
            ]
        elif "[Stay Still]" in selection:
            new_story = "You hold your breath, listening. Faint footsteps echo nearby."
            new_choices = [
                "[Hide] Look for cover",
                "[Call Out] Try to communicate",
                "[Stay Silent] Remain motionless"
            ]
        elif "[Hide]" in selection:
            new_story = "You quickly dive behind an old wooden crate. Your heart pounds as footsteps echo nearby."
            new_choices = [
                "[Stay Hidden] Remain behind the crate",
                "[Peek Out] Try to see what's coming",
                "[Hold Your Breath] Stay as quiet as possible"
            ]
        elif "[Stay Hidden]" in selection:
            new_story = "You hold your breath as the footsteps stop just inches away."
            new_choices = [
                "[Close Your Eyes] Hope you're not seen",
                "[Try to Move] Shift to a better position",
                "[Hold Your Breath Longer] Stay absolutely still"
            ]
        elif "[Peek Out]" in selection:
            new_story = "You carefully peek out from behind the crate. A shadow moves in the doorway."
            new_choices = [
                "[Stay Hidden] Duck back behind cover",
                "[Step Out] Reveal yourself",
                "[Wait] Keep watching silently"
            ]
        elif "[Hold Your Breath]" in selection:
            new_story = "Your lungs burn as you stay completely still. The footsteps stop right in front of you."
            new_choices = [
                "[Exhale Quietly] Release your breath slowly",
                "[Wait a Little Longer] Push your limits",
                "[Try to Move] Shift position carefully"
            ]
        elif "Quit" in selection:
            self.quit_app()
            return
        else:
            new_story = (
                "An unexpected error has occurred. Perhaps this choice has not been coded yet? "
                "If so, make Oliver M do it."
            )
            new_choices = ["[Quit] Exit the game"]

        # Animate the new story text and then the new choices
        self.type_text(new_story, self.story_label, callback=lambda: self.type_choices(new_choices))

    # Update available choices and reset the selection index
    def set_new_choices(self, new_choices):
        self.menu_options = new_choices
        self.current_selection = 0
        self.update_menu_display()

    # FIX: Improved type_text method that properly handles typing state
    def type_text(self, full_text, label, delay=50, callback=None):
        # Clear existing text and block key input during animation
        label.config(text="")
        self.typing = True
        print("Typing started - input blocked")  # Debug message
        
        # Cancel any existing animation and safety timers
        self.cancel_timers()
        
        # Set safety timeout - ensure typing state gets reset even if animation fails
        max_animation_time = len(full_text) * delay + 5000  # Added more buffer time
        self.safety_timer = self.after(max_animation_time, self.reset_typing_state)

        # FIX: Instead of typing full text at once, use a counter to track progress
        char_count = 0
        total_chars = len(full_text)

        def inner_type(i=0):
            nonlocal char_count
            if i <= len(full_text):
                label.config(text=full_text[:i])
                char_count = i
                self.animation_timer = self.after(delay, inner_type, i + 1)
            else:
                # Animation complete
                if callback:
                    # Wait a second before calling callback
                    self.animation_timer = self.after(1000, lambda: self.finish_animation(callback))
                else:
                    # Only reset typing state if this is the final animation
                    self.reset_typing_state()

        inner_type()

    # Helper method to cancel all timers
    def cancel_timers(self):
        # Cancel any existing animation timer
        if self.animation_timer:
            self.after_cancel(self.animation_timer)
            self.animation_timer = None
        
        # Cancel any existing safety timer
        if self.safety_timer:
            self.after_cancel(self.safety_timer)
            self.safety_timer = None
    
    # Helper method to reset typing state and execute callbacks safely
    def finish_animation(self, callback):
        # Cancel the safety timer
        if self.safety_timer:
            self.after_cancel(self.safety_timer)
            self.safety_timer = None
            
        # Call the provided callback
        try:
            callback()
        except Exception as e:
            print(f"Error in animation callback: {e}")
            # Make sure we reset typing state in case of an error
            self.reset_typing_state()
    
    # Method to safely reset typing state
    def reset_typing_state(self):
        # Only print debug message if typing was actually in progress
        if self.typing:
            print("Typing ended - input unblocked")  # Debug message
        
        self.typing = False
        self.animation_timer = None
        self.safety_timer = None

    # FIX: Improved type_choices method that correctly handles typing state
    def type_choices(self, choices, delay=50):
        self.text_label.config(text="")  # Clear existing choices
        self.menu_options = choices
        self.typing = True
        print("Choices typing started - input blocked")  # Debug message
        
        # Cancel any existing timers
        self.cancel_timers()
        
        # Set safety timeout
        total_chars = sum(len(choice) for choice in choices) + len(choices) * 4  # Include formatting chars
        max_animation_time = total_chars * delay + 5000  # Added more buffer time
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
                    self.text_label.config(text=current_text + "\n\n")
                    self.animation_timer = self.after(delay, type_choice, choice_index + 1, 0)
            else:
                # Animation complete - NOW we can reset the typing state
                self.current_selection = 0
                self.reset_typing_state()

        type_choice()

    # Quit the application by closing the window
    def quit_app(self, event=None):
        # Clean up any pending timers
        self.cancel_timers()
        self.destroy()

# Entry point: create an instance of ChoiceScreen and start the main loop
if __name__ == "__main__":
    ChoiceScreen().mainloop()