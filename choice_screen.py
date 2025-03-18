import tkinter as tk
from PIL import Image, ImageTk

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

    def quit_app(self):
        self.cancel_timers()
        self.destroy()

    def handle_selection(self):
        selection = self.menu_options[self.current_selection]
        try:
            tag = selection.split(']')[0] + ']'
        except Exception:
            tag = selection

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
                    "[Call Out] Attempt to communicate with the darkness"
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
                "As your fingers brush against the figure's hand, a jolt of icy energy surges through you. The light intensifies, but instead of warmth, it burns with malevolent intent. The figure's features sharpen, revealing a cruel, gaunt face with eyes that gleam with dark amusement. A voice, cold as a crypt, echoes in your mind: 'It's already too late.'",
                ["[Submit] Accept your fate", "[Fight] Struggle against the inevitable"]
            ),
            "[Fight]": (
                "You steel yourself, ready to confront the apparition. But as you raise your arm, the world shimmers and warps. The figure dissolves into a cascade of fragmented images, but a chilling laughter lingers in the air...",
                ["[Resist] Fight against what is coming"]
            ),
            "[Submit]": (
                "A wave of despair washes over you as you relinquish control. The figure's grip tightens, and the world dissolves into a kaleidoscope of terrifying visions. You feel your essence being consumed, your identity fading into nothingness. There is only the figure now, and the endless, silent void.",
                ["[End]"]
            ),
            "[Resist]": (
                "You fight with every fiber of your being, but the power arrayed against you is immense. The fragmented images coalesce once more, forming a horrifying visage of pure malice. With a final, triumphant shriek, the figure unleashes a wave of energy. Blackness consumes you, but even in the void, you sense that this is not the end.",
                ["[End]"]
            ),
            "[End]": (
                "The darkness is absolute. Your journey is over, but your story...your story is not your own anymore.",
                [""]
            )
        }

        story, choices = paths.get(tag, ("Nothing happens. Perhaps you should get Oliver M to code it.", []))
        self.type_text(story, self.story_label, callback=lambda: self.type_choices(choices))

    def type_text(self, full_text, label, delay=50, callback=None):
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

    def type_choices(self, choices, delay=50):
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
                    self.text_label.config(text=current_text + "\n\n")
                    self.animation_timer = self.after(delay, type_choice, choice_index + 1, 0)
            else:
                self.current_selection = 0
                self.reset_typing_state()
        type_choice()

if __name__ == "__main__":
    ChoiceScreen().mainloop()
