from tkinter import Tk, Menu, Frame, Entry, Label
from tkinter.messagebox import askokcancel
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText

class SetText(Tk):
    def __init__(self):
        super().__init__()
        self.title("SetText")

        self.menu = Menu(self)
        self.config(menu=self.menu)
        
        self.file_menu = Menu(self.menu)
        self.menu.add_cascade(label="File", underline=0, menu=self.file_menu)
        self.file_menu.add_command(label="Open", underline=0,
                                   command=self.show_open)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1,
                                   command=self.show_quit)

        self.frame = None

    def show_open(self):
        filename = askopenfilename(filetypes=(("Text files", ".txt,.text"),
                                              ("All files", "*.*")))
        if not filename:
            return
        self.title("SetText - {}".format(filename))
        
        text = self.open(filename)
        if self.frame:
            self.frame.destroy()
        self.frame = JustType(text)
        self.frame.pack()

    def show_quit(self):
        if askokcancel("Exit?", "Are you sure you want to exit?"):
            self.destroy()

    @staticmethod
    def open(filename):
        with open(filename, 'r') as f:
            return f.read()
        
class JustType(Frame):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.user_typed = []
        self.cursor = 0

        self.text_box = ScrolledText(self)
        self.text_box.configure(state="disabled")
        self.text_box.grid(row=0, columnspan=2)

        self.input_box = Label(self)
        self.input_box.grid(row=2, column=0, sticky='e')

        self.history_box = Label(self)
        self.history_box.grid(row=1, column=0, sticky='e')

        self.future_box = Label(self)
        self.future_box.grid(row=1, column=1, sticky='w')

        self.bind("<Key>", self.update)

    def update(self, e):
        if len(e.keysym) == 1:
            self.user_typed[cursor:cursor+1] = e.keysym        
        
        typed = self.input_box.get()
        self.user_typed[:cursor] = typed

        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
        self.text_box.insert("end", "{}\n{}\n{}".format(e.keysym,
                                                        typed,
                                                        self.user_typed))
        self.text_box.configure(state="disabled")

        self.history_box['text'] = self.text[:len(typed)].split('\n')[-1]
        self.future_box['text'] = (self.text[len(typed):len(self.user_typed)]
                                   .split('\n')[0])

if __name__ == "__main__":
    SetText().mainloop()
