import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import subprocess

# Database Setup
conn = sqlite3.connect("patients.db")
cursor = conn.cursor()

# Create Table for Storing Patient Data
cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    therapy TEXT NOT NULL,
                    feedback TEXT)''')
conn.commit()

# Global Variables
patient_data = {}

# Games categorized by therapy type
games = {
    "Cognitive Therapy": [
        ("🐍 Play Cognitive Snake Game", "/home/kali-mnx/Documents/CodeSpace/S-MediTech/Game integrations/snake_game/snake_game.py")
    ],
    "Physical Therapy": [
        ("🏓 Play Table Tennis Therapy", "/home/kali-mnx/Documents/CodeSpace/S-MediTech/Game integrations/TT_ai.py"),
        ("🏃 Start Your Exercise Session", "/home/kali-mnx/Documents/CodeSpace/Python/Project-Expo.py")
    ],
    "Relaxation Therapy": []  # Add relevant relaxation games if available
}

# Function to handle registration
def submit_details():
    global patient_data
    name = name_entry.get().strip()
    age = age_entry.get().strip()
    therapy = therapy_type.get()

    if not name or not age or not therapy:
        messagebox.showerror("Error", "Please fill in all details!")
        return
    
    patient_data = {"name": name, "age": age, "therapy": therapy}

    # Save patient details to database
    cursor.execute("INSERT INTO patients (name, age, therapy, feedback) VALUES (?, ?, ?, ?)", 
                   (name, age, therapy, None))
    conn.commit()
    
    # Hide registration frame & Show game options
    registration_frame.pack_forget()
    display_games(therapy)

# Function to display relevant games
def display_games(therapy):
    for widget in game_selection_frame.winfo_children():
        widget.destroy()
    
    tk.Label(game_selection_frame, text="🎯 Choose Your Activity", font=("Arial", 14, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=5)
    
    if therapy in games:
        for game_name, game_path in games[therapy]:
            tk.Button(game_selection_frame, text=game_name, command=lambda path=game_path: run_game(path),
                      font=("Arial", 12, "bold"), width=35, height=2, bg="#64B5F6", fg="white").pack(pady=5)
    else:
        tk.Label(game_selection_frame, text="No games available for this therapy.", font=("Arial", 12), bg="#E3F2FD").pack()
    
    game_selection_frame.pack(pady=20)

# Function to run the selected game
def run_game(game_path):
    try:
        subprocess.run(["python3", game_path], check=True)
        feedback_frame.pack(pady=20)  # Show feedback after playing
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to run {game_path}:\n{e}")

# Function to collect feedback
def submit_feedback():
    feedback_text = feedback_entry.get("1.0", tk.END).strip()
    if not feedback_text:
        messagebox.showerror("Error", "Please provide your feedback!")
        return

    # Update feedback in database
    cursor.execute("UPDATE patients SET feedback = ? WHERE name = ? AND therapy = ?", 
                   (feedback_text, patient_data["name"], patient_data["therapy"]))
    conn.commit()

    messagebox.showinfo("Thank You!", f"Thank you, {patient_data['name']}! Your feedback is recorded.")
    feedback_frame.pack_forget()
    summary_label.config(text=f"👤 {patient_data['name']}, Age: {patient_data['age']}\n🩺 Therapy: {patient_data['therapy']}\n✅ Feedback: {feedback_text}")
    summary_frame.pack(pady=20)

# Function to exit the app
def exit_app():
    conn.close()
    root.destroy()

# Initialize Tkinter window
root = tk.Tk()
root.title("🩺 Patient Wellness & Game Hub")
root.geometry("600x600")
root.configure(bg="#E3F2FD")

# Registration Form
registration_frame = tk.Frame(root, bg="#E3F2FD")
registration_frame.pack(pady=20)

tk.Label(registration_frame, text="👤 Enter Your Details", font=("Arial", 14, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=5)
tk.Label(registration_frame, text="Full Name:", font=("Arial", 12), bg="#E3F2FD").pack()
name_entry = tk.Entry(registration_frame, font=("Arial", 12), width=30)
name_entry.pack(pady=5)

tk.Label(registration_frame, text="Age:", font=("Arial", 12), bg="#E3F2FD").pack()
age_entry = tk.Entry(registration_frame, font=("Arial", 12), width=30)
age_entry.pack(pady=5)

tk.Label(registration_frame, text="Therapy Type:", font=("Arial", 12), bg="#E3F2FD").pack()
therapy_type = ttk.Combobox(registration_frame, values=list(games.keys()), font=("Arial", 12), width=28)
therapy_type.pack(pady=5)

submit_btn = tk.Button(registration_frame, text="✔ Proceed", command=submit_details, font=("Arial", 12, "bold"), bg="#64B5F6", fg="white", width=20)
submit_btn.pack(pady=10)

# Game Selection Frame
game_selection_frame = tk.Frame(root, bg="#E3F2FD")

# Feedback Section
feedback_frame = tk.Frame(root, bg="#E3F2FD")
tk.Label(feedback_frame, text="💬 How was your experience?", font=("Arial", 14, "bold"), bg="#E3F2FD", fg="#1565C0").pack(pady=5)
feedback_entry = tk.Text(feedback_frame, font=("Arial", 12), width=50, height=4)
feedback_entry.pack(pady=5)
submit_feedback_btn = tk.Button(feedback_frame, text="✔ Submit Feedback", command=submit_feedback, font=("Arial", 12, "bold"), bg="#388E3C", fg="white", width=20)
submit_feedback_btn.pack(pady=5)

# Session Summary
summary_frame = tk.Frame(root, bg="#E3F2FD")
summary_label = tk.Label(summary_frame, text="", font=("Arial", 12), bg="#E3F2FD", fg="#1B5E20")
summary_label.pack()

# Exit Button
btn_exit = tk.Button(root, text="🚪 Exit Safely", command=exit_app, font=("Arial", 12, "bold"), bg="#E53935", fg="white", width=20)
btn_exit.pack(pady=20)

root.mainloop()
