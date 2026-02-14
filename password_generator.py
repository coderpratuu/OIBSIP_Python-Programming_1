import tkinter as tk
from tkinter import messagebox
import random
import string

# ================= PASSWORD GENERATION =================
def generate_password():
    try:
        length = int(length_entry.get())

        if length < 4:
            messagebox.showerror("Error", "Password length must be at least 4.")
            return

        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()
        exclude_chars = exclude_entry.get()

        if not (use_letters or use_numbers or use_symbols):
            messagebox.showerror("Error", "Select at least one character type.")
            return

        characters = ""

        if use_letters:
            characters += string.ascii_letters
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation

        # Remove excluded characters
        for char in exclude_chars:
            characters = characters.replace(char, "")

        if not characters:
            messagebox.showerror("Error", "No characters available after exclusions.")
            return

        password = ''.join(random.choice(characters) for _ in range(length))

        # Ensure strong password rule (at least one of each selected type)
        if use_letters and not any(c in string.ascii_letters for c in password):
            password = password[:-1] + random.choice(string.ascii_letters)
        if use_numbers and not any(c in string.digits for c in password):
            password = password[:-1] + random.choice(string.digits)
        if use_symbols and not any(c in string.punctuation for c in password):
            password = password[:-1] + random.choice(string.punctuation)

        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)

        show_strength(password)

    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for length.")

# ================= PASSWORD STRENGTH =================
def show_strength(password):
    strength = 0

    if len(password) >= 8:
        strength += 1
    if any(c in string.ascii_letters for c in password):
        strength += 1
    if any(c in string.digits for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1

    levels = {
        1: ("Very Weak", "#e74c3c"),
        2: ("Weak", "#f39c12"),
        3: ("Good", "#f1c40f"),
        4: ("Strong", "#2ecc71")
    }

    text, color = levels.get(strength, ("Very Weak", "#e74c3c"))
    strength_label.config(text=f"Strength: {text}", fg=color)

# ================= CLIPBOARD =================
def copy_to_clipboard():
    password = result_entry.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

# ================= GUI DESIGN =================
root = tk.Tk()
root.title("Advanced Password Generator")
root.geometry("450x500")
root.configure(bg="#1e272e")

title_label = tk.Label(
    root,
    text="Random Password Generator",
    font=("Helvetica", 18, "bold"),
    bg="#1e272e",
    fg="white"
)
title_label.pack(pady=20)

frame = tk.Frame(root, bg="#485460", padx=20, pady=20)
frame.pack(pady=10)

tk.Label(frame, text="Password Length:", bg="#485460", fg="white").grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(frame)
length_entry.grid(row=0, column=1, pady=5)

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(frame, text="Include Letters", variable=letters_var,
               bg="#485460", fg="white", selectcolor="#485460").grid(row=1, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Include Numbers", variable=numbers_var,
               bg="#485460", fg="white", selectcolor="#485460").grid(row=2, columnspan=2, sticky="w")
tk.Checkbutton(frame, text="Include Symbols", variable=symbols_var,
               bg="#485460", fg="white", selectcolor="#485460").grid(row=3, columnspan=2, sticky="w")

tk.Label(frame, text="Exclude Characters:", bg="#485460", fg="white").grid(row=4, column=0, sticky="w")
exclude_entry = tk.Entry(frame)
exclude_entry.grid(row=4, column=1, pady=5)

tk.Button(root, text="Generate Password",
          command=generate_password,
          bg="#00a8ff", fg="white",
          padx=10, pady=5).pack(pady=10)

result_entry = tk.Entry(root, font=("Helvetica", 14), justify="center")
result_entry.pack(pady=10, fill="x", padx=20)

strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 12, "bold"),
                          bg="#1e272e")
strength_label.pack(pady=5)

tk.Button(root, text="Copy to Clipboard",
          command=copy_to_clipboard,
          bg="#4cd137", fg="white",
          padx=10, pady=5).pack(pady=10)

root.mainloop()
