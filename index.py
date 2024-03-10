<!DOCTYPE html>
<html lang="en">
<head>
  <title>희순이의 생각하는 동화</title>
 
</head>
<body>
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import datetime

class ColorNoteApp:
    def __init__(self, master):
        self.master = master
        self.master.title("ColorNote")

        # Create database connection
        self.conn = sqlite3.connect("notes.db")
        self.cursor = self.conn.cursor()
        self.create_table()

        # Initialize variables
        self.current_note_id = None

        # GUI components
        self.note_text = tk.Text(self.master, height=20, width=50)
        self.note_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self.save_button = tk.Button(self.master, text="Save Note", command=self.save_note)
        self.save_button.grid(row=1, column=0, padx=5, pady=5)

        self.load_button = tk.Button(self.master, text="Load Note", command=self.load_note)
        self.load_button.grid(row=1, column=1, padx=5, pady=5)

        self.delete_button = tk.Button(self.master, text="Delete Note", command=self.delete_note)
        self.delete_button.grid(row=1, column=2, padx=5, pady=5)

        self.notes_list = ttk.Treeview(self.master, columns=("ID", "Content"), selectmode="browse")
        self.notes_list.heading("#0", text="Category")
        self.notes_list.column("#0", width=100)
        self.notes_list.heading("ID", text="ID")
        self.notes_list.column("ID", width=50)
        self.notes_list.heading("Content", text="Content")
        self.notes_list.column("Content", width=300)
        self.notes_list.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.load_notes()

        self.notes_list.bind("<Double-1>", self.note_selected)

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, content TEXT, created_at TEXT)''')
        self.conn.commit()

    def save_note(self):
        note_content = self.note_text.get("1.0", "end-1c")
        if note_content.strip() != "":
            category = "General"
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.current_note_id:
                self.cursor.execute('''UPDATE notes SET category=?, content=?, created_at=? WHERE id=?''',
                                    (category, note_content, created_at, self.current_note_id))
            else:
                self.cursor.execute('''INSERT INTO notes (category, content, created_at) VALUES (?, ?, ?)''',
                                    (category, note_content, created_at))
            self.conn.commit()
            self.load_notes()
            self.current_note_id = None
            messagebox.showinfo("Note Saved", "Note has been saved successfully.")
        else:
            messagebox.showerror("Error", "Note content cannot be empty.")

    def load_notes(self):
        self.notes_list.delete(*self.notes_list.get_children())
        self.cursor.execute('''SELECT id, category, content FROM notes''')
        notes = self.cursor.fetchall()
        for note in notes:
            self.notes_list.insert("", "end", text=note[1], values=(note[0], note[2]))

    def load_note(self):
        selected_item = self.notes_list.selection()
        if selected_item:
            selected_note_id = self.notes_list.item(selected_item)['values'][0]
            self.cursor.execute('''SELECT content FROM notes WHERE id=?''', (selected_note_id,))
            note_content = self.cursor.fetchone()[0]
            self.note_text.delete("1.0", "end")
            self.note_text.insert("1.0", note_content)
            self.current_note_id = selected_note_id
        else:
            messagebox.showinfo("No Note Selected", "Please select a note to load.")

    def delete_note(self):
        selected_item = self.notes_list.selection()
        if selected_item:
            confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this note?")
            if confirmation:
                selected_note_id = self.notes_list.item(selected_item)['values'][0]
                self.cursor.execute('''DELETE FROM notes WHERE id=?''', (selected_note_id,))
                self.conn.commit()
                self.load_notes()
                messagebox.showinfo("Note Deleted", "Note has been deleted successfully.")
                self.note_text.delete("1.0", "end")
                self.current_note_id = None
        else:
            messagebox.showinfo("No Note Selected", "Please select a note to delete.")

    def note_selected(self, event):
        self.load_note()

def main():
    root = tk.Tk()
    app = ColorNoteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

    </body>
</html>