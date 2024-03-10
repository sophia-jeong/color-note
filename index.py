import tkinter as tk
from tkinter import messagebox
import sqlite3

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
        self.note_text.pack()

        self.save_button = tk.Button(self.master, text="Save Note", command=self.save_note)
        self.save_button.pack()

        self.load_button = tk.Button(self.master, text="Load Note", command=self.load_note)
        self.load_button.pack()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS notes 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)''')
        self.conn.commit()

    def save_note(self):
        note_content = self.note_text.get("1.0", "end-1c")
        if note_content.strip() != "":
            if self.current_note_id:
                self.cursor.execute('''UPDATE notes SET content=? WHERE id=?''', (note_content, self.current_note_id))
            else:
                self.cursor.execute('''INSERT INTO notes (content) VALUES (?)''', (note_content,))
            self.conn.commit()
            self.current_note_id = None
            messagebox.showinfo("Note Saved", "Note has been saved successfully.")
        else:
            messagebox.showerror("Error", "Note content cannot be empty.")

    def load_note(self):
        self.note_text.delete("1.0", "end")
        self.cursor.execute('''SELECT id, content FROM notes''')
        notes = self.cursor.fetchall()
        if notes:
            selected_note_id, selected_note_content = notes[0]
            self.note_text.insert("1.0", selected_note_content)
            self.current_note_id = selected_note_id
        else:
            self.current_note_id = None
            messagebox.showinfo("No Notes", "No saved notes found.")

def main():
    root = tk.Tk()
    app = ColorNoteApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()