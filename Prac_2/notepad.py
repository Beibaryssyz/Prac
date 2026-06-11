import os
import webbrowser
from pathlib import Path
from tkinter import (Tk, Menu, filedialog, scrolledtext,
                     constants, messagebox)


# NotePad class — tk-notepad 0.5 (extended with Edit menu)
class NotePad:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.saved = False
        self.root = Tk()  # Initializing root window.

        self.about = None
        self.github_link = None
        self.info = None

        # Setting filename as "Untitled" and creating empty file_path variable.
        self.filename = "Untitled"
        self.file_path = ""

        # --- Menu bar ---
        self.menu_bar = Menu(self.root)

        # File menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New",     command=self.new_file)
        self.file_menu.add_command(label="Open",    command=self.open_file)
        self.file_menu.add_command(label="Save",    command=self.save_existing)
        self.file_menu.add_command(label="Save As", command=self.save_as_textfile)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",    command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut",        command=self.cut_text)
        self.edit_menu.add_command(label="Copy",       command=self.copy_text)
        self.edit_menu.add_command(label="Paste",      command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.root.config(menu=self.menu_bar)

        # text_area using ScrolledText — wrap="word" and undo=True
        self.text_area = scrolledtext.ScrolledText(self.root, wrap="word", undo=True)

        # Ask before closing if there are unsaved changes
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    # ------------------------------------------------------------------ #
    #  Title helper                                                        #
    # ------------------------------------------------------------------ #
    def update_title(self, title):
        self.root.title(f"{title} - Notepad")

    # ------------------------------------------------------------------ #
    #  File operations                                                     #
    # ------------------------------------------------------------------ #
    def open_file(self):
        self.file_path = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=(("Text File", "*.txt"),)
        )
        if not self.file_path:
            return
        with open(self.file_path, "r", encoding="utf-8") as f:
            text = f.read()
        self.text_area.delete("1.0", constants.END)
        self.update_title(os.path.basename(self.file_path))
        self.text_area.insert("1.0", text)
        self.saved = True

    def new_file(self):
        if self._confirm_discard():
            self.root.destroy()
            nt = NotePad(800, 600)
            nt.run()

    def save_existing(self):
        try:
            if self.saved and self.file_path:
                with open(self.file_path, "w", encoding="utf-8") as f:
                    f.truncate(0)
                    f.write(self.text_area.get("1.0", constants.END))
            else:
                self.save_as_textfile()
        except FileNotFoundError:
            pass

    def save_as_textfile(self):
        self.file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=(("Text File", "*.txt"),)
        )
        if not self.file_path:
            return
        try:
            with open(self.file_path, "w+", encoding="utf-8") as f:
                f.write(self.text_area.get("1.0", constants.END))
            self.update_title(os.path.basename(self.file_path))
            self.saved = True
        except FileNotFoundError:
            pass

    def exit_app(self):
        if self._confirm_discard():
            self.root.destroy()

    def _confirm_discard(self):
        """Return True if it is safe to close/replace the current document."""
        if not self.saved or self.text_area.edit_modified():
            answer = messagebox.askyesnocancel(
                "Сохранить изменения?",
                "Файл не сохранён. Сохранить изменения перед закрытием?"
            )
            if answer is True:        # Yes — save then proceed
                self.save_existing()
                return True
            elif answer is False:     # No — discard and proceed
                return True
            else:                     # Cancel — do nothing
                return False
        return True

    # ------------------------------------------------------------------ #
    #  Edit operations                                                     #
    # ------------------------------------------------------------------ #
    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def select_all(self):
        self.text_area.tag_add("sel", "1.0", constants.END)
        self.text_area.mark_set("insert", "1.0")
        self.text_area.see("insert")

    # ------------------------------------------------------------------ #
    #  Run                                                                 #
    # ------------------------------------------------------------------ #
    def run(self):
        icon_path = Path(__file__).parent / "icons" / "notepad_icon.ico"
        if icon_path.exists():
            self.root.iconbitmap(icon_path)

        self.root.geometry(f"{self.width}x{self.height}")
        self.root.title(f"{self.filename} - Notepad")

        self.text_area.pack(expand=True, fill="both")

        self.root.mainloop()


def main():
    notepad = NotePad(800, 600)
    notepad.run()


if __name__ == "__main__":
    main()