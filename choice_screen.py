# Import the tkinter module to create graphical user interfaces (GUIs)
import tkinter as tk
# Import Image and ImageTk from the PIL library to work with images in our app
from PIL import Image, ImageTk
# Import os to work with operating system features (though not used here)
import os

class ChoiceScreen(tk.Tk):
    def __init__(self):
        super().__init__()  # Set up the main window

        # Configure the main window
        self.title("Python Game Yay")
        self.geometry("1020x1020")
        self.configure(bg="black")

        # Initialize game state and input flag
        self.menu_options = []         # List to store menu choices
        self.current_selection = 0     # Index for current choice
        self.typing = False            # Flag to block key input during text animation
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

        # Bind all key presses to our centralized key handler
        self.bind("<Key>", self.handle_key_press)

        # Start the game by displaying the title screen
        self.show_title_screen()

    def handle_key_press(self, event):
        # Block input if a typing animation is in progress
        if self.typing:
            print(f"Key press blocked: {event.keysym}")
            return "break"
        if event.keysym == "Up":
            return self.navigate_up(event)
        elif event.keysym == "Down":
            return self.navigate_down(event)
        elif event.keysym == "Return":
            return self.select_option(event)
        elif event.keysym == "Escape":
            return self.quit_app(event)
        return None

    def load_background_image(self):
        try:
            img = Image.open("background-image.png").convert("RGBA")
            self.background_image = ImageTk.PhotoImage(img.resize((1020, 1020)))
            bg_label = tk.Label(self, image=self.background_image)
        except FileNotFoundError:
            bg_label = tk.Label(self, bg="black")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.lower()

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

    def navigate_up(self, event=None):
        if self.menu_options:
            self.current_selection = (self.current_selection - 1) % len(self.menu_options)
            self.update_menu_display()
        return "break"

    def navigate_down(self, event=None):
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

    def select_option(self, event=None):
        if self.menu_options:
            self.text_label.config(text="")  # Clear current choices
            self.handle_selection()
        return "break"
    
    def quit_app(self, event=None):
        self.cancel_timers()
        self.destroy()

    def handle_selection(self):
        # Extract the tag from the selected option.
        selection = self.menu_options[self.current_selection]
        print("Handling selection:", selection)
        try:
            tag = selection.split(']')[0] + ']'
        except Exception:
            tag = selection

        # Special disambiguation if needed.
        if tag == "[Follow Path]" and "Step forward!" in selection:
            tag = "[Follow Path new reality]"

        # Dictionary mapping tags to (story, choices)
        paths = {
            "[Look Around]": (
                "You reach out into the darkness and run your hand along the cold, damp wall. Your fingertips graze something uneven — a door, barely ajar. "
                "The possibility of escape ignites a flicker of hope amid the despair.",
                [
                    "[Open the Door] Push the door open and step into the unknown",
                    "[Stay Still] Hesitate, unsure if it’s safe to move",
                    "[Search the Room] Continue feeling around for more clues"
                ]
            ),
            "[Open the Door]": (
                "You push the door open and step into a cold, dim corridor. The silence is oppressive, and your footsteps echo off distant walls.",
                [
                    "[Proceed] Continue down the corridor",
                    "[Return to Room] Retreat back into the room"
                ]
            ),
            "[Search the Room]": (
                "You feel around the room. Your hand brushes over dusty objects and faded markings on the wall. Something seems out of place—a loose stone, perhaps.",
                [
                    "[Examine Stone] Take a closer look at the unusual stone",
                    "[Ignore] Decide it might be nothing"
                ]
            ),
            "[Proceed]": (
                "You walk down the corridor. The air grows colder and your footsteps become a steady rhythm. The corridor seems endless, yet you sense an exit ahead.",
                [
                    "[Follow Path] Continue forward into the unknown",
                    "[Return to Room] Turn back to the safety of the room"
                ]
            ),
            "[Return to Room]": (
                "You decide the corridor is too unsettling and retreat back into the room. The darkness of the room now seems even more oppressive.",
                [
                    "[Search the Room] Look around again carefully",
                    "[Stay Still] Remain where you are, hoping for a different outcome"
                ]
            ),
            "[Examine Stone]": (
                "Upon closer examination, the stone is dislodged from the wall, revealing a small cavity behind it. A faint light glimmers from within, hinting at secrets long forgotten.",
                [
                    "[Open Cavity] Investigate the hidden cavity",
                    "[Replace Stone] Put the stone back and leave it alone"
                ]
            ),
            "[Ignore]": (
                "You decide it might be nothing, but the uneasy feeling lingers. The room feels colder now, and you wonder if you missed something important.",
                [
                    "[Search the Room] Try searching the room again",
                    "[Call Out] Attempt to break the silence"
                ]
            ),
            "[Open Cavity]": (
                "You open the cavity. Inside, you discover an old, dusty key. It seems to beckon you with a silent promise of escape or further mystery.",
                [
                    "[Take Key] Take the key and consider your next move",
                    "[Leave Key] Decide not to disturb it and search elsewhere"
                ]
            ),
            "[Replace Stone]": (
                "You replace the stone, but the memory of the hidden light haunts you. The room remains silent and full of secrets.",
                [
                    "[Search the Room] Look for other clues",
                    "[Call Out] Attempt to communicate with the darkness"
                ]
            ),
            "[Take Key]": (
                "You take the key. It feels cold and heavy in your hand, yet it exudes a sense of importance. Perhaps it will open a door to a new path.",
                [
                    "[Open the Door] Return to the door with the key",
                    "[Follow Path] Proceed further into the mystery"
                ]
            ),
            "[Leave Key]": (
                "You leave the key behind, but a lingering regret fills you. The key might have been your only chance to unlock the secrets of this place.",
                [
                    "[Search the Room] Continue searching the room",
                    "[Call Out] Shout into the darkness in frustration"
                ]
            ),
            "[Call Out]": (
                "You call out into the void. Your voice echoes back at you, distorted and empty. For a long, tense moment, only silence responds — until a whisper replies, indistinct yet unnerving.",
                [
                    "[Call Again] Shout louder, challenging the silence",
                    "[Wait Silently] Hold your breath, straining to catch any further sound",
                    "[Bang on the Wall] Hit the wall, desperate for a response"
                ]
            ),
            "[Stay Still]": (
                "You freeze, merging with the darkness. The quiet is almost too loud, and the measured footsteps outside grow nearer. Every sound is amplified as you strain to understand your surroundings.",
                [
                    "[Hide] Crouch lower, trying to conceal your presence",
                    "[Call Out] Risk speaking again, hoping to break the silence",
                    "[Stay Silent] Keep perfectly still, listening intently"
                ]
            ),
            "[Hide]": (
                "You press yourself against the wall and slide into a shadowy corner behind a crate. Your heart pounds in your ears as the footsteps approach, each step measured and foreboding.",
                [
                    "[Stay Hidden] Remain motionless, blending into the darkness",
                    "[Peek Out] Gently lift your head to see what’s coming",
                    "[Hold Your Breath] Inhale deeply, forcing silence from within"
                ]
            ),
            "[Stay Hidden]": (
                "You hold your position, barely daring to breathe as the echoing steps pass by. The oppressive stillness leaves you suspended between fear and relief.",
                [
                    "[Close Your Eyes] Shut out the darkness, hoping not to see what lurks",
                    "[Try to Move] Risk a slight shift to a safer spot",
                    "[Hold Your Breath Longer] Maintain your frozen state a moment more"
                ]
            ),
            "[Peek Out]": (
                "Carefully, you peek out from behind the crate. In the faint outline of the doorway, a shifting shadow catches your eye—a fleeting glimpse of movement that raises more questions than answers.",
                [
                    "[Stay Hidden] Retreat quickly back behind cover",
                    "[Step Out] Step into the doorway to investigate further",
                    "[Wait] Remain watching, hoping to discern its nature"
                ]
            ),
            "[Hold Your Breath]": (
                "You force the breath from your lungs, trying to remain perfectly silent. The footsteps slow, as if in cautious deliberation, before halting directly in front of you.",
                [
                    "[Exhale Quietly] Let out a slow, measured exhale",
                    "[Wait a Little Longer] Continue to hold your breath, straining to remain undetected",
                    "[Try to Move] Risk a subtle movement in the hope of escape"
                ]
            ),
            "[Call Again]": (
                "You call out once more, louder this time. Your voice trembles as it fills the darkness. A raspy whisper soon responds—a voice so close it sends shivers down your spine.",
                ["[Approach] Step toward the voice with cautious determination"]
            ),
            "[Wait Silently]": (
                "Silence reigns for a heartbeat before the sound of measured footsteps resumes outside. The air feels thick with anticipation as you decide your next move.",
                ["[Approach the doorway cautiously] Move toward the door, ready for whatever lies beyond"]
            ),
            "[Bang on the Wall]": (
                "You bang on the wall, each knock reverberating through the emptiness. Suddenly, a section of the wall shudders and slides aside, revealing a narrow passage lined with cryptic symbols. "
                "A cold gust of wind and a barely audible murmur brush past you.",
                ["[Enter Passage] Step into the newly revealed passage with trepidation"]
            ),
            "[Stay Silent]": (
                "You remain perfectly silent as the footsteps recede, leaving behind an eerie quiet. Yet, a lingering sense of being watched settles over you like a shroud.",
                ["[Approach] Advance slowly toward the doorway, compelled by both fear and curiosity"]
            ),
            "[Try to Move]": (
                "You risk a slight shift in your position, the crate creaking softly beneath you. The sound is ominous in the stillness, and you wonder if it might draw unwanted attention.",
                ["[Examine Crate] Inspect the crate for any clues or a means to steady it"]
            ),
            "[Hold Your Breath Longer]": (
                "Time stretches as you continue to hold your breath. Your vision begins to blur, and a desperate need for air gnaws at you, yet you dare not move.",
                ["[Exhale Quietly] Finally release your breath in a quiet, resigned sigh"]
            ),
            "[Examine Crate]": (
                "You run your hand over the crate, its rough wood and splintered edges offering no secrets—only the persistent odor of something faintly spicy lingers. "
                "It leaves you with a growing unease, as if the crate holds memories of forgotten rituals.",
                ["[Exhale Quietly] Let out a soft exhale and listen for any change in the atmosphere"]
            ),
            "[Step Out]": (
                "You step into the doorway, your body trembling. As you emerge, the shadow coalesces into a tall, gaunt figure, its features obscured by darkness. "
                "Its presence is both inviting and terrifying.",
                ["[Approach] Move closer to the figure, trying to discern its intent"]
            ),
            "[Wait]": (
                "You wait, every sense heightened. In the doorway, the shadow remains still—a silent sentinel that seems to hold secrets beyond comprehension.",
                ["[Approach] Edge toward the shadow, determined to uncover its mystery"]
            ),
            "[Exhale Quietly]": (
                "A long, soft exhale escapes you, breaking the stifling tension. The footsteps outside momentarily cease, leaving only the echo of your breath in the oppressive silence.",
                ["[Approach] Carefully approach the doorway, bracing for what may come"]
            ),
            "[Approach]": (
                "Drawn by the enigmatic whisper, you step toward the voice. As you advance, a burst of light briefly illuminates a spectral figure. "
                "Its outstretched hand seems to beckon you forward, though uncertainty tugs at your mind.",
                [
                    "[Trust] Reach out and take the figure’s hand",
                    "[Fight] Prepare to confront the unknown menace"
                ]
            ),
            "[Approach the doorway cautiously]": (
                "With trepidation, you move toward the door. The light intensifies as you near, and suddenly, the space before you transforms into a surreal tableau:\n\n"
                "A whisper echoes, 'I see you,' as a mysterious figure extends its hand. The decision feels fated—trust the unknown, or resist its pull?",
                [
                    "[Trust] Reach out and accept the offered hand",
                    "[Fight] Muster your courage and prepare to resist"
                ]
            ),
            "[Trust]": (
                "Your hand meets the spectral grasp, and in that instant, a surge of blinding light engulfs you. Images of another life—a self both familiar and foreign—flicker before your eyes as you are pulled into a realm of endless possibility.",
                ["[Follow Path] Follow the alternate version of yourself into the unknown"]
            ),
            "[Fight]": (
                "You steel yourself, ready to confront the apparition. But as you raise your arm, the world shimmers and warps. The figure dissolves into a cascade of fragmented images, leaving you to wonder if resistance was ever truly an option.",
                ["[Follow Path] Step forward into the swirling unknown"]
            ),
            "[Follow Path]": (
                "Your senses are overwhelmed, the world shatters, and then suddenly, it stops..\n"
                "You've escaped. But what was that place? Who was the figure, truly?\n",
                ["[To Be Continued] Continue on your journey"]
            ),
            "[Follow Path new reality]": (
                "Your senses are overwhelmed, the world shatters, and then suddenly, it stops..\n"
                "You've escaped. But what was that place? Who was the figure, truly?\n",
                ["[To Be Continued] Embrace this new beginning"]
            ),
            "[Enter Passage]": (
                "Summoning your courage, you enter the narrow passage. The air grows colder with each step, and ancient symbols seem to pulse with an eerie, hidden life. "
                "The corridor leads you to a threshold between the world you knew and another, more unsettling realm.",
                ["[Follow Path] Step forward into this altered reality"]
            ),
            "[To Be Continued]": (
                "Chapter 2 coming soon!",
                ["[Quit] Exit the game"]
            ),
            "[Quit]": (
                "Thank you for playing. May the shadows guide you...",
                []
            )
        }

        # Look up the branch by the extracted tag.
        if tag in paths:
            new_story, new_choices = paths[tag]
        else:
            new_story = ("An unexpected error has occurred. This path seems uncharted. "
                         "If the darkness continues, perhaps it's time to quit.")
            new_choices = ["[Quit] Exit the game"]

        # Debug: print the tag and resulting story branch
        print("Selected tag:", tag)
        print("New story:", new_story)
        print("New choices:", new_choices)

        # If the branch is [Quit], type the final message then quit the app.
        if tag == "[Quit]":
            self.type_text(new_story, self.story_label, callback=lambda: self.after(2000, self.quit_app))
        else:
            # Otherwise, animate the new story and then the new choices.
            self.type_text(new_story, self.story_label, callback=lambda: self.type_choices(new_choices))

    def set_new_choices(self, new_choices):
        self.menu_options = new_choices
        self.current_selection = 0
        self.update_menu_display()

    def type_text(self, full_text, label, delay=50, callback=None):
        label.config(text="")
        self.typing = True
        print("Typing started - input blocked")
        self.cancel_timers()
        max_animation_time = len(full_text) * delay + 5000
        self.safety_timer = self.after(max_animation_time, self.reset_typing_state)
        total_chars = len(full_text)

        def inner_type(i=0):
            if i <= total_chars:
                label.config(text=full_text[:i])
                self.animation_timer = self.after(delay, inner_type, i+1)
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
        try:
            callback()
        except Exception as e:
            print(f"Error in animation callback: {e}")
            self.reset_typing_state()

    def reset_typing_state(self):
        if self.typing:
            print("Typing ended - input unblocked")
        self.typing = False
        self.animation_timer = None
        self.safety_timer = None

    def type_choices(self, choices, delay=50):
        self.text_label.config(text="")
        self.menu_options = choices
        self.typing = True
        print("Choices typing started - input blocked")
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
                    self.animation_timer = self.after(delay, type_choice, choice_index, char_index+1)
                else:
                    self.text_label.config(text=current_text + "\n\n")
                    self.animation_timer = self.after(delay, type_choice, choice_index+1, 0)
            else:
                self.current_selection = 0
                self.reset_typing_state()
        type_choice()

    def quit_app(self, event=None):
        self.cancel_timers()
        self.destroy()

if __name__ == "__main__":
    ChoiceScreen().mainloop()
