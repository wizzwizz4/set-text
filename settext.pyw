from tkinter import Tk, Menu, Frame, Entry, Label
from tkinter.messagebox import askokcancel
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText
from itertools import product

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

        set_focus = lambda e:self.focus_set()
        for widget, event in product(
            (self, self.text_box, self.input_box, self.history_box,
             self.future_box),
            ("<Button-1>", "<Button-2>", "<Button-3>")
        ):
            widget.bind(event, set_focus)
        self.bind("<Key>", self.update)

    def update(self, e):
        if e.char and e.char.isprintable():
            self.user_typed[self.cursor:self.cursor+1] = e.char
            self.cursor += 1
        elif e.keysym == "Return":
            self.user_typed[self.cursor:self.cursor+1] = '\n'
            self.cursor += 1
        elif e.keysym == "BackSpace":
            self.cursor -= 1
            self.user_typed[self.cursor:self.cursor+1] = ()
        elif e.keysym == "Left":
            if self.cursor > 0:
                self.cursor -= 1
        elif e.keysym == "Right":
            if self.cursor < len(self.user_typed):
                self.cursor += 1

        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", "end")
##        self.text_box.insert("end", "{}\n{}\n{}".format(vars(e),
##                                                        self.cursor,
##                                                        self.user_typed))
        self.text_box.insert(
            "end",
            "\n".join(self.text.split('\n')[:self.user_typed[:self.cursor]
                                            .count('\n')])
        )
        self.text_box.configure(state="disabled")

        self.history_box['text'] = self.text[:self.cursor].split('\n')[-1]
        self.input_box['text'] = ("".join(self.user_typed[:self.cursor])
                                  .split('\n')[-1])
        self.future_box['text'] = (self.text[self.cursor:len(self.user_typed)]
                                   .split('\n')[0])

if __name__ == "__main__":
    SetText().mainloop()
