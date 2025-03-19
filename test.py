import tkinter as tk
import subprocess
import os
print("Current working directory:", os.getcwd())

def play_audio():
    try:
        # Use ffplay to play the audio without opening a display window and exit automatically after playback.
        subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "type-effect.mp3"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception as e:
        print("Error playing audio:", e)

root = tk.Tk()
root.title("Corridors")
root.geometry("400x200")
root.configure(bg="black")

label = tk.Label(root, text="Welcome to Corridors!", fg="white", bg="black", font=("Courier", 18, "bold"))
label.pack(pady=50)

# Play the sound effect once when the window loads
play_audio()

exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Courier", 14))
exit_button.pack(pady=10)

root.mainloop()
