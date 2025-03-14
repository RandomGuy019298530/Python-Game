
Scroll down for a Github tutorial and how to use this project.



# 🚀 **GitHub Tutorial for Your Python Game Project**  

🔗 **Project Repository:** [Python Game on GitHub](https://github.com/RandomGuy019298530/Python-Game)  

This guide will show you how to **set up GitHub, download the project, make changes, and upload them back** in the **easiest** way possible.  

## 🛠 **1. Install the Required Tools**  

The easiest way to work with GitHub is to use:  
✅ **[GitHub Desktop](https://desktop.github.com/)** – A user-friendly way to manage your code.  
✅ **[VS Code](https://code.visualstudio.com/)** – A great editor for writing Python code.  

### 🔹 **Step 1: Install GitHub Desktop**  
1. Download **GitHub Desktop** from [this link](https://desktop.github.com/).  
2. Install and open it.  
3. Sign in with your **GitHub account**.  

### 🔹 **Step 2: Install VS Code**  
1. Download **VS Code** from [this link](https://code.visualstudio.com/).  
2. Install and open it.  
3. Go to **Extensions (Ctrl + Shift + X)** and install:  
   - **Python** (for coding)  
   - **GitHub Pull Requests and Issues** (for GitHub integration)  

---

## 📂 **2. Download (Clone) the Project**  

### **Option 1: Using GitHub Desktop (Recommended)**
1. Open **GitHub Desktop**.  
2. Click **"File" → "Clone Repository"**.  
3. Select the URL tab and enter:  
   ```
   https://github.com/RandomGuy019298530/Python-Game.git
   ```
4. Click **"Clone"** to download the project.  
5. Open the project folder in **VS Code** by clicking **"Open in Visual Studio Code"** in GitHub Desktop.  

### **Option 2: Using Git (For Advanced Users)**
If you prefer using Git manually, open a terminal and run:  
```sh
git clone https://github.com/RandomGuy019298530/Python-Game.git
```

---

## ✍️ **3. Making Changes to the Code**  
Once you have the project open in **VS Code**, you can start making changes.

### **Step 1: Open the File You Want to Edit**  
- Use the **Explorer (Ctrl + Shift + E)** in VS Code to navigate and open files.  

### **Step 2: Modify the Code**  
- Make any changes or add new features to the game.

---

## ✅ **4. Save and Upload Your Changes**  

### **Step 1: Save and Check Changes**
After editing, go to **GitHub Desktop** and check the **Changes** tab. It will show all the files you modified.

### **Step 2: Write a Commit Message**
1. In **GitHub Desktop**, under "Summary," write a short message about your changes (e.g., "Fixed menu alignment").  
2. Click **"Commit to main"**.  

### **Step 3: Push (Upload) Your Changes**
Click **"Push origin"** to upload your changes to GitHub.  

---

## 🔄 **5. Updating Your Code (Pulling Changes from GitHub)**  
If someone else has updated the project, you need to **update your local version**.  

1. Open **GitHub Desktop**.  
2. Click **"Fetch Origin"** → **"Pull"** to download the latest updates.  

---

## ⚠️ **6. Handling Merge Conflicts (If Needed)**  
If you see a **merge conflict**, VS Code will show the differences between your code and the updated code.  

1. Manually **fix the conflicting parts** in the file.  
2. Save the file.  
3. Go back to **GitHub Desktop**, write a commit message, and push again.  

---

## 🔥 **7. Summary of Important Steps**  
| Action | How to Do It (Easiest Method) |
|--------|-------------------------------|
| Download Project | Clone it using GitHub Desktop |
| Open in VS Code | Click "Open in VS Code" in GitHub Desktop |
| Edit Code | Modify files in VS Code |
| Save Changes | GitHub Desktop → Write commit message → "Commit to main" |
| Upload Changes | Click "Push origin" in GitHub Desktop |
| Get Latest Updates | Click "Fetch Origin" → "Pull" in GitHub Desktop |

---

## 🎮 **You're Ready to Contribute!**  
Now you can **edit, commit, and upload** your code like a pro. If you run into any issues, let the team know! 🚀







# Guide: Creating a Configurable Text-Based RPG Menu with Tkinter

## Overview
This guide demonstrates how to:
- Use a Canvas widget to display text and images.
- Position text at a configurable vertical height.
- Update the scene by changing text and images as needed.

## Step-by-Step Instructions

1. **Set Up the Tkinter Application**  
   Create a main application window, set its title, dimensions, and background color.

2. **Create a Canvas Widget**  
   Use the Canvas widget to draw text and images at specific (x, y) coordinates. This gives you full control over the placement of each element.

3. **Load and Display Images**  
   Use the Pillow (PIL) library to load images. Convert them to `ImageTk.PhotoImage` objects and display them on the Canvas.

4. **Add Configurable Text**  
   Use `canvas.create_text()` to print text on the Canvas. The y-coordinate (vertical position) can be set with a variable, making it easy to reposition the text.

5. **Update the Scene Dynamically**  
   Create functions that update the text (both content and position) and swap images, allowing you to progress through the game’s storyline.

## Full Example Code

```python
import tkinter as tk
from PIL import Image, ImageTk
import os

class RPGMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text-Based RPG")  # Change the window title here.
        self.geometry("1020x1020")     # Set window dimensions (width x height).
        self.configure(bg="black")     # Set the background color.

        # Create a Canvas for precise positioning.
        self.canvas = tk.Canvas(self, width=1020, height=1020, bg="black", highlightthickness=0)
        self.canvas.pack()

        # Load images (update the file names and sizes as needed).
        self.image1 = self.load_image("pixil-frame-0 (16).png", 400, 400)
        self.image2 = self.load_image("another_image.png", 400, 400)

        # Display the first image at the center of the canvas.
        self.current_image = self.canvas.create_image(510, 510, image=self.image1, anchor=tk.CENTER)

        # Set an initial y-coordinate for the text (adjust this value as desired).
        self.text_y = 200  
        self.text_item = self.canvas.create_text(
            510,             # x-coordinate (center)
            self.text_y,     # y-coordinate (configurable vertical position)
            text="Welcome to the RPG!",  # Initial text content.
            fill="white",    # Text color.
            font=("Courier", 32, "bold"),  # Font, size, and style.
            anchor=tk.CENTER  # Center the text horizontally.
        )

        # Example: Update the scene after 3 seconds to simulate game progression.
        self.after(3000, self.update_scene)

    def load_image(self, filename, width, height):
        """Loads and resizes an image given its filename, width, and height."""
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        if os.path.exists(image_path):
            img = Image.open(image_path).resize((width, height), Image.ANTIALIAS)
            return ImageTk.PhotoImage(img)
        else:
            print(f"Warning: Image file not found: {image_path}")
            return None

    def update_scene(self):
        """Example function to update the text and image on the screen."""
        new_text_y = 300  # Set a new vertical position for the text.
        self.canvas.coords(self.text_item, 510, new_text_y)  # Update text position.
        self.canvas.itemconfig(self.text_item, text="Your journey begins...")  # Update text content.

        # Swap the image to a second image, if available.
        if self.image2:
            self.canvas.itemconfig(self.current_image, image=self.image2)

if __name__ == "__main__":
    app = RPGMenu()
    app.mainloop()
```

## How to Customize

- **Text Position:**  
  Change the `self.text_y` variable or the value in `self.canvas.coords(self.text_item, 510, new_text_y)` to set the desired vertical position for your text.

- **Images:**  
  Modify the filenames in the `load_image()` calls. Adjust the `width` and `height` parameters to suit your design.

- **Text and Font:**  
  Update the `text` parameter in `canvas.create_text()` and the font settings to change the message and appearance.

- **Scene Updates:**  
  Use the `update_scene()` method (or create similar methods) to dynamically change the text and images as the game progresses.
