import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime

# File paths
JOURNAL_FILE = "journal_entries.json"
PROMPTS_FILE = "prompts.json"

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

# Load prompts
def load_prompts():
    try:
        with open(PROMPTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        with open(PROMPTS_FILE, "w") as file:
            json.dump(DEFAULT_PROMPTS, file)
        return DEFAULT_PROMPTS

# Save prompts
def save_prompts(prompts):
    with open(PROMPTS_FILE, "w") as file:
        json.dump(prompts, file, indent=4)

# Load journal
def load_journal():
    try:
        with open(JOURNAL_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save journal
def save_journal(journal):
    with open(JOURNAL_FILE, "w") as file:
        json.dump(journal, file, indent=4)

# Get a random prompt
def get_random_prompt():
    prompts = load_prompts()
    return random.choice(prompts)

# Initialize Streamlit app state
if "journal" not in st.session_state:
    st.session_state.journal = load_journal()

if "random_prompt" not in st.session_state:
    st.session_state.random_prompt = get_random_prompt()

# Streamlit layout
st.title("Journaling App")

# Display random prompt
st.subheader("Today's Prompt")
st.write(st.session_state.random_prompt)

# Journal entry input
entry = st.text_area("What's on your mind today?")
tags = st.text_input("Tags (comma-separated)")
mood = st.slider("How are you feeling today?", 1, 5)

# Save entry button
if st.button("Save Entry"):
    date = datetime.now().strftime("%Y-%m-%d")
    if date not in st.session_state.journal:
        st.session_state.journal[date] = {
            "prompt": st.session_state.random_prompt,
            "entry": entry,
            "tags": [tag.strip() for tag in tags.split(",")],
            "mood": mood
        }
        save_journal(st.session_state.journal)
        st.success("Your entry has been saved!")
        st.session_state.random_prompt = get_random_prompt()  # Update the prompt
    else:
        st.warning("You already have an entry for today!")

# Display journal entries
st.subheader("Your Journal Entries")
for date, content in st.session_state.journal.items():
    st.write(f"### {date}")
    st.write(f"- **Prompt**: {content['prompt']}")
    st.write(f"- **Entry**: {content['entry']}")
    st.write(f"- **Tags**: {', '.join(content['tags'])}")
    st.write(f"- **Mood**: {content['mood']}")

# Analyze data
if st.button("Analyze Data"):
    journal_df = pd.DataFrame.from_dict(st.session_state.journal, orient="index")
    journal_df["mood"] = pd.to_numeric(journal_df["mood"], errors="coerce")

    st.subheader("Mood Trends Over Time")
    st.line_chart(journal_df["mood"])

    st.subheader("Most Common Tags")
    all_tags = [tag for tags in journal_df["tags"] for tag in tags]
    tag_counts = pd.Series(all_tags).value_counts()
    st.bar_chart(tag_counts)

# Add prompt management
st.subheader("Manage Prompts")
new_prompt = st.text_input("Add a new prompt")
if st.button("Add Prompt"):
    prompts = load_prompts()
    prompts.append(new_prompt)
    save_prompts(prompts)
    st.success("New prompt added!")
