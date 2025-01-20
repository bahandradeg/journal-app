import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import random

# File paths
# Ensure these files exist or will be created in /Users/barbaraguimaraes/Documents/
JOURNAL_FILE = "/Users/barbaraguimaraes/Documents/journal_entries.json"
PROMPTS_FILE = "/Users/barbaraguimaraes/Documents/prompts.json"

# Default prompts
DEFAULT_PROMPTS = [
    "What made you smile today?",
    "What challenges did you face, and how did you overcome them?",
    "What are you grateful for today?",
    "Describe your mood and why you feel that way.",
    "What is something you learned recently?",
    "How did you take care of yourself today?",
    "What is a small victory you achieved today?",
    "What’s something you’re looking forward to?"
]

# Initialize prompts file
def load_prompts():
    try:
        with open(PROMPTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open(PROMPTS_FILE, "w") as file:
            json.dump(DEFAULT_PROMPTS, file)
        return DEFAULT_PROMPTS

def save_prompts(prompts):
    with open(PROMPTS_FILE, "w") as file:
        json.dump(prompts, file, indent=4)

# Load and save journal entries
def load_journal():
    try:
        with open(JOURNAL_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_journal(journal):
    with open(JOURNAL_FILE, "w") as file:
        json.dump(journal, file, indent=4)

def get_random_prompt():
    prompts = load_prompts()
    return random.choice(prompts)

# Core journal operations
journal = load_journal()

# GUI Functions
def add_entry():
    date = datetime.now().strftime("%Y-%m-%d")
    prompt = prompt_label.cget("text")
    entry = entry_text.get("1.0", tk.END).strip()
    tags = tags_entry.get().split(",")
    mood = mood_var.get()

    if not entry or not mood:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    journal[date] = {
        "prompt": prompt,
        "entry": entry,
        "tags": [tag.strip() for tag in tags],
        "mood": int(mood)
    }
    save_journal(journal)
    messagebox.showinfo("Success", "Journal entry saved!")
    entry_text.delete("1.0", tk.END)
    tags_entry.delete(0, tk.END)
    mood_var.set("")
    update_prompt()  # Get a new random prompt after saving

def view_entry():
    date = date_entry.get()
    if date in journal:
        entry = journal[date]
        messagebox.showinfo(
            f"Entry for {date}",
            f"Prompt: {entry['prompt']}\n"
            f"Entry: {entry['entry']}\n"
            f"Tags: {', '.join(entry['tags'])}\n"
            f"Mood: {entry['mood']}"
        )
    else:
        messagebox.showerror("Error", "No entry found for this date!")

def analyze_data():
    if not journal:
        messagebox.showerror("Error", "No data available for analysis!")
        return

    # Convert journal to DataFrame
    data = pd.DataFrame.from_dict(journal, orient="index")
    data.index.name = "Date"
    data["mood"] = pd.to_numeric(data["mood"], errors="coerce")

    # Mood Trends
    plt.figure()
    data["mood"].plot(title="Mood Trends Over Time", ylabel="Mood (1-5)", marker="o")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Most Common Tags
    all_tags = [tag for tags in data["tags"] for tag in tags]
    tag_counts = pd.Series(all_tags).value_counts()

    plt.figure()
    tag_counts.plot(kind="bar", title="Most Common Tags", ylabel="Frequency")
    plt.tight_layout()
    plt.show()

def update_prompt():
    prompt_label.config(text=get_random_prompt())

def manage_prompts():
    def add_custom_prompt():
        new_prompt = prompt_entry.get().strip()
        if new_prompt:
            prompts = load_prompts()
            prompts.append(new_prompt)
            save_prompts(prompts)
            messagebox.showinfo("Success", "Prompt added!")
            prompt_entry.delete(0, tk.END)
            update_prompt_list()
        else:
            messagebox.showerror("Error", "Prompt cannot be empty!")

    def update_prompt_list():
        prompt_list.delete(0, tk.END)
        prompts = load_prompts()
        for p in prompts:
            prompt_list.insert(tk.END, p)

    # Manage Prompts Window
    manage_window = tk.Toplevel(app)
    manage_window.title("Manage Prompts")

    tk.Label(manage_window, text="Existing Prompts:").pack(pady=5)
    prompt_list = tk.Listbox(manage_window, width=50, height=10)
    prompt_list.pack(pady=5)
    update_prompt_list()

    tk.Label(manage_window, text="Add New Prompt:").pack(pady=5)
    prompt_entry = tk.Entry(manage_window, width=40)
    prompt_entry.pack(pady=5)
    tk.Button(manage_window, text="Add Prompt", command=add_custom_prompt).pack(pady=10)

# GUI Setup
app = tk.Tk()
app.title("Journaling App")

# Add Entry Section
tk.Label(app, text="Daily Journal", font=("Arial", 16)).grid(row=0, column=0, columnspan=3, pady=10)

prompt_label = tk.Label(app, text=get_random_prompt(), wraplength=300, justify="left")
prompt_label.grid(row=1, column=0, columnspan=3, pady=5)

tk.Label(app, text="Your Entry:").grid(row=2, column=0, sticky="w")
entry_text = tk.Text(app, width=40, height=5)
entry_text.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

tk.Label(app, text="Tags (comma-separated):").grid(row=4, column=0, sticky="w")
tags_entry = tk.Entry(app, width=30)
tags_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Label(app, text="Mood (1-5):").grid(row=5, column=0, sticky="w")
mood_var = tk.StringVar()
mood_entry = ttk.Combobox(app, textvariable=mood_var, values=[1, 2, 3, 4, 5], width=5)
mood_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Button(app, text="Save Entry", command=add_entry).grid(row=6, column=0, columnspan=3, pady=10)

# View Entry Section
tk.Label(app, text="View Entry").grid(row=7, column=0, columnspan=3, pady=10)

tk.Label(app, text="Enter Date (YYYY-MM-DD):").grid(row=8, column=0, sticky="w")
date_entry = tk.Entry(app, width=20)
date_entry.grid(row=8, column=1, padx=10, pady=5)

tk.Button(app, text="View", command=view_entry).grid(row=9, column=0, columnspan=3, pady=5)

# Analyze Data Section
tk.Button(app, text="Analyze Data", command=analyze_data).grid(row=10, column=0, columnspan=3, pady=10)

# Manage Prompts Section
tk.Button(app, text="Manage Prompts", command=manage_prompts).grid(row=11, column=0, columnspan=3, pady=10)

app.mainloop()
