# Text Editor App.

# Tkinter module and library.

# A module is a single file containing code, while a library is a massive collection of multiple modules and packages grouped together.

# Tkinter is Python's standard, built-in library used for creating Graphical User Interfaces (GUIs)

# Import tkinter for creating GUI apps.
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
# Imports three specific sub-modules from the Tkinter GUI package to create standard popup windows and dialog boxes.
from datetime import datetime
import base64

# For theme .
BG_COLOR = "#1a1a1a" # Deep dark gray background.
TEXT_COLOR = "#00ffff" # Neon cyan / Aqua text.
CURSOR_COLOR = "#ff0055" # Neon red cursor marker.
CUSTOM_FONT = ("Consolas", 13)

# Timer settings.
timer_running = False
seconds_left = 0
lap_history = []

# Function 1 -to count 
def update_counts(event=None):
    content = text.get("1.0", tk.END + "-1c")
    char_count = len(content)
    word_count = len(content.split()) # The split() method in Python breaks a single string into a list of smaller strings (substrings) based on a specified delimiter.
    status_bar.config(text=f"Words: {word_count} | Characters: {char_count}")

# Function 3- to create a new file.
def new_file():
    text.delete("1.0", tk.END) # In Python's Tkinter GUI library, the code text.delete(1.0, tk.END) is used to completely clear all the text content from a Text widget.
    update_counts()

# Function 4 - to open a new file.
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            text.delete("1.0", tk.END)
            text.insert("1.0", file.read())
        update_counts()

# Function 5 - to save the file.
def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get("1.0", tk.END)) # In Python, file.write(text.get(1.0, tk.END)) extracts all the string content from a Tkinter Text widget and saves it directly into an open file
        messagebox.showinfo("Info", "File saved successfully")

# Function 6 - timer .
def countdown():
    global seconds_left, timer_running
    if timer_running and seconds_left > 0:
        mins, secs = divmod(seconds_left, 60)
        status_bar.config(text=f"⏱️ Focus Time: {mins:02d}:{secs:02d} | " + status_bar.cget("text").split(" | ", 1)[-1])
        seconds_left -= 1
        root.after(1000, countdown)
    elif seconds_left == 0 and timer_running:
        timer_running = False
        messagebox.showinfo("SYSTEM ALERT", "🚨 PROTOCOL COMPLETE: Take a break, Falcon-X pilot.")
        update_counts()

def start_timer():
    global timer_running, seconds_left
    if not timer_running:
        if seconds_left == 0:
            user_mins = simpledialog.askinteger("SYSTEM INPUT", "Enter focus time in minutes:", minvalue=1, maxvalue=180)
            if user_mins:
                seconds_left = user_mins * 60
            else:
                return
        timer_running = True
        countdown()

def pause_timer():
    global timer_running
    timer_running = False
    messagebox.showinfo("SYSTEM INFO", "⏸️ Timer Paused.")

# --- RESET FUNCTION ---
def reset_timer():
    global timer_running, seconds_left, lap_history
    timer_running = False
    seconds_left = 0
    lap_history.clear()
    messagebox.showinfo("SYSTEM RESET", "🔄 Timer and Lap History have been reset!")
    update_counts()

# --- MODIFIED LAP LOGIC WITH TIMESTAMP ---
def lap_timer():
    if timer_running or seconds_left > 0:
        mins, secs = divmod(seconds_left, 60)
        current_time = datetime.now().strftime("%I:%M:%S %p")
        lap_info = f"Lap {len(lap_history)+1} -> Remaining: {mins:02d}:{secs:02d} | Taken at: {current_time}"
        lap_history.append(lap_info)
        messagebox.showinfo("LAP RECORDED", f"⏱️ {lap_info}")

# --- LAP HISTORY FUNCTION ---
def show_lap_history():
    if not lap_history:
        messagebox.showinfo("LAP HISTORY", "No laps recorded yet in this session.")
    else:
        history_text = "\n".join(lap_history)
        messagebox.showinfo("📋 FALCON-X LAP HISTORY", history_text)

# Function to handle quantum data lock encryption
def encrypt_text():
    secret_data = text.get("1.0", tk.END + "-1c")
    if not secret_data.strip():
        messagebox.showwarning("SYSTEM ERROR", "Please type something before locking!")
        return
    key = simpledialog.askstring("ENCRYPTION KEY", "Set a 4-digit numeric password to Lock:", show="*")
    if key:
        encoded_bytes = base64.b64encode(secret_data.encode("utf-8"))
        encrypted_string = encoded_bytes.decode("utf-8")
        text.delete("1.0", tk.END)
        text.insert("1.0", f"--- LOCKED BY FALCON-X SYSTEM ---\nKEY-ID: {key}\nDATA: {encrypted_string}")
        messagebox.showinfo("QUANTUM LOCK", "💥 DATA ENCRYPTED SECURELY!")

# Function to handle quantum data unlock decryption
def decrypt_text():
    content = text.get("1.0", tk.END + "-1c")
    if "--- LOCKED BY FALCON-X SYSTEM ---" not in content:
        messagebox.showwarning("SYSTEM ERROR", "This text is not locked!")
        return
    key_guess = simpledialog.askstring("DECRYPTION KEY", "Enter your secret password to Unlock:", show="*")
    try:
        lines = content.split("\n")
        original_key = lines[1].replace("KEY-ID: ", "")
        if key_guess == original_key:
            encrypted_string = lines[2].replace("DATA: ", "")
            decoded_bytes = base64.b64decode(encrypted_string.encode("utf-8"))
            original_text = decoded_bytes.decode("utf-8")
            text.delete("1.0", tk.END)
            text.insert("1.0", original_text)
            messagebox.showinfo("QUANTUM UNLOCK", "🔓 ACCESS GRANTED!")
        else:
            messagebox.showerror("ACCESS DENIED", "❌ INCORRECT PASSWORD!")
    except Exception:
        messagebox.showerror("ERROR", "Data corrupted!")

# Function to trigger typing ripple effect on active text insertion
def trigger_bubble_effect(event=None):
    if not bubble_effect_enabled.get():
        return
    
    # Using KeyRelease instead of KeyPress captures the character *after* it is inserted into the widget, 
    # ensuring the bubble highlights the exact, current character typed instead of the previous one.
    pos = text.index(tk.INSERT)
    start_pos = f"{pos}-1c"
    
    text.tag_add("ripple", start_pos, pos)
    text.tag_config("ripple", background="#00ffff", foreground="#1a1a1a")
    root.after(100, lambda: text.tag_remove("ripple", "1.0", tk.END))

root = tk.Tk() 
#In Python, root = tk.Tk() initializes the Tkinter toolkit and creates the main application window.
root.title("FALCON-X Editor")
root.geometry("800x600") # For size 
root.config(bg=BG_COLOR)

# creates special Tkinter variables to hold states and link changes with widgets like Checkbuttons.
bubble_effect_enabled = tk.BooleanVar(value=False)

# Cursor = blinking line 
text = tk.Text(
    root, # parent window
    wrap=tk.WORD, # wrap text by words
    font=CUSTOM_FONT,
    bg=BG_COLOR, # Dark background
    fg=TEXT_COLOR, # Neon text color
    insertbackground=CURSOR_COLOR, # If you want to change the text insertion cursor (the blinking line) inside an input widget, you use the insertbackground parameter:
    padx=10, pady=10
)
text.pack(expand=True, fill=tk.BOTH) # The expression text.pack(expand=True, fill=tk.BOTH) in Python's Tkinter library forces a widget (like a Text box) to dynamically expand and completely fill all available horizontal and vertical space inside its parent window or frame.

text.bind("<KeyRelease>", update_counts)
# Capturing bubble calculation on KeyRelease fixes the one-character animation sync offset delay.
text.bind("<KeyRelease>", trigger_bubble_effect, add="+")

# A Label is a widget used to display non-editable text or images on the screen. 
status_bar = tk.Label(
    root, # In Python's Tkinter library, root is the conventional variable name assigned to the main application window. It is created by initializing the Tk class (root = tk.Tk()), which acts as the foundational base and container for your entire Graphical User Interface (GUI).
    text="Words: 0 | Characters: 0",
    font=("Consolas", 10),
    bg="#111111",
    fg="#00ffff",
    anchor=tk.E,
    padx=10, pady=5
)
status_bar.pack(side=tk.BOTTOM, fill=tk.X) # a geometry management command used to position a widget (acting as a status bar) at the very bottom of the application window and stretch it horizontally to span the window's full width.

# MENU 
menu = tk.Menu(root)
root.config(menu=menu) # initialize and display a top-level menu bar at the top of an application window using the Tkinter library.

# NEW , OPEN FILE , SAVE , EXIT. 
# Add file menu to menu bar.
file_menu = tk.Menu(menu, tearoff=0) # In Python, the line file_menu = Menu(menu) creates a dropdown submenu (often labeled "File") for an application's menu bar in a Graphical User Interface.
file_menu.add_command(label="New", command=new_file) # In Python's Tkinter GUI library, menu.add_command() is a method used to add a clickable action item to a drop-down menu.
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator() # In Python GUI development, file_menu.add_separator() is a method used to draw a horizontal line divider inside a dropdown menu.
file_menu.add_command(label="Exit", command=root.quit)
menu.add_cascade(label="File", menu=file_menu) # a method used to bind a dropdown submenu to a parent menu or to the main menu bar.

# Cyber-Mode Dropdown setup
cyber_menu = tk.Menu(menu, tearoff=0) # In Python, tearoff is a configuration property used in the Tkinter library to control how menus behave.
menu.add_cascade(label="Cyber-Mode", menu=cyber_menu)
cyber_menu.add_command(label="▶️ Start Focus Mode", command=start_timer)
cyber_menu.add_command(label="⏸️ Pause Timer", command=pause_timer)
cyber_menu.add_command(label="🔄 Reset Timer", command=reset_timer)
cyber_menu.add_command(label="⏱️ Record Lap", command=lap_timer)
cyber_menu.add_command(label="📋 View Lap History", command=show_lap_history)
cyber_menu.add_separator()
cyber_menu.add_command(label="🔒 Quantum Lock", command=encrypt_text)
cyber_menu.add_command(label="🔓 Quantum Unlock", command=decrypt_text)

# Fly-Mode Dropdown setup
fly_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Fly-Mode", menu=fly_menu)
fly_menu.add_checkbutton(label="🧼 Enable Bubble Effect", variable=bubble_effect_enabled)

root.mainloop() # In Python, root.mainloop() is a method used in the Tkinter library to start the application's event loop