import random
import tkinter as tk
from tkinter import messagebox, filedialog

# Character pools
letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
numbers = list("0123456789")
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

def generate_password(nr_letters, nr_symbols, nr_numbers):
    letters_selected = random.choices(letters, k=nr_letters)
    symbols_selected = random.choices(symbols, k=nr_symbols)
    numbers_selected = random.choices(numbers, k=nr_numbers)

    easy_pwd = ''.join(letters_selected + symbols_selected + numbers_selected)

    charlist = list(easy_pwd)
    random.shuffle(charlist)
    hard_pwd = ''.join(charlist)

    return easy_pwd, hard_pwd

# GUI Application
class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyPassword Generator by Rudraksha")

        self.password_history = []  # Store generated passwords here

        # Input fields
        tk.Label(root, text="Letters:").grid(row=0, column=0, sticky="e")
        tk.Label(root, text="Symbols:").grid(row=1, column=0, sticky="e")
        tk.Label(root, text="Numbers:").grid(row=2, column=0, sticky="e")

        self.letters_var = tk.StringVar(value="4")
        self.symbols_var = tk.StringVar(value="2")
        self.numbers_var = tk.StringVar(value="2")

        tk.Entry(root, textvariable=self.letters_var, width=5).grid(row=0, column=1)
        tk.Entry(root, textvariable=self.symbols_var, width=5).grid(row=1, column=1)
        tk.Entry(root, textvariable=self.numbers_var, width=5).grid(row=2, column=1)

        # Difficulty selection
        self.difficulty_var = tk.StringVar(value="easy")
        tk.Radiobutton(root, text="Easy", variable=self.difficulty_var, value="easy").grid(row=3, column=0)
        tk.Radiobutton(root, text="Hard", variable=self.difficulty_var, value="hard").grid(row=3, column=1)

        # Buttons
        tk.Button(root, text="Generate Password", command=self.generate).grid(row=4, column=0, columnspan=2, pady=5)
        tk.Button(root, text="Show History", command=self.show_history).grid(row=7, column=0, columnspan=2, pady=5)

        # Password display
        self.password_display = tk.Entry(root, width=40, font=("Arial", 14))
        self.password_display.grid(row=5, column=0, columnspan=2, pady=5)

        # Copy button
        tk.Button(root, text="Copy to Clipboard", command=self.copy_password).grid(row=6, column=0, columnspan=2)

    def generate(self):
        try:
            nr_letters = int(self.letters_var.get())
            nr_symbols = int(self.symbols_var.get())
            nr_numbers = int(self.numbers_var.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid integer numbers!")
            return

        easy_pwd, hard_pwd = generate_password(nr_letters, nr_symbols, nr_numbers)
        if self.difficulty_var.get() == "hard":
            pwd = hard_pwd
        else:
            pwd = easy_pwd

        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, pwd)

        # Save to history
        self.password_history.append(pwd)

    def copy_password(self):
        pwd = self.password_display.get()
        if pwd:
            self.root.clipboard_clear()
            self.root.clipboard_append(pwd)
            messagebox.showinfo("Copied!", "Password copied to clipboard.")
        else:
            messagebox.showwarning("No Password", "Generate a password first.")

    def show_history(self):
        if not self.password_history:
            messagebox.showinfo("History Empty", "No passwords generated yet!")
            return

        history_window = tk.Toplevel(self.root)
        history_window.title("Password History")

        tk.Label(history_window, text="Generated Passwords:", font=("Arial", 12, "bold")).pack(pady=5)

        # Scrollable text box to show history
        history_text = tk.Text(history_window, width=50, height=10, wrap='word')
        history_text.pack(padx=10, pady=10)

        # Insert all passwords with index
        for i, pwd in enumerate(self.password_history, start=1):
            history_text.insert(tk.END, f"{i}: {pwd}\n")

        history_text.config(state='disabled')  # read-only

        # Save to file button
        save_btn = tk.Button(history_window, text="Save to File", command=lambda: self.save_history_to_file(history_window))
        save_btn.pack(side="left", padx=10, pady=5)

        # Close button
        close_btn = tk.Button(history_window, text="Close", command=history_window.destroy)
        close_btn.pack(side="right", padx=10, pady=5)

    def save_history_to_file(self, parent_window):
        # Ask user where to save
        file_path = filedialog.asksaveasfilename(
            parent=parent_window,
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return  # User cancelled

        try:
            with open(file_path, "w") as f:
                for i, pwd in enumerate(self.password_history, start=1):
                    f.write(f"{i}: {pwd}\n")
            messagebox.showinfo("Saved", f"Passwords saved to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
