import tkinter as tk
from paragraphs import Offline

DEFAULT_DIFFICULTY = 'easy'

def input_blocker(event):
    return "break"

class TypingTest(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Typing Test")
        self.geometry("800x450")
        self.config(padx=50, pady=50)

        self.UI = dict()
        self.UI['toolbar'] = self.render_toolbar()
        self.UI['main'] = self.render_body()

        self.diff_select()

    def render_toolbar(self):
        toolbar = tk.Frame(self, highlightbackground='white', highlightthickness=1)
        toolbar.pack(side="top", fill="x")

        radiovar = tk.StringVar()
        radiovar.set('easy')

        easy = tk.Radiobutton(
            toolbar,
            text="Easy",
            variable=radiovar,
            value='easy',
            command=self.diff_select
        )
        easy.pack(side="left", padx=5, pady=10)

        medium = tk.Radiobutton(
            toolbar,
            text="Medium",
            variable=radiovar,
            value='medium',
            command = self.diff_select
        )
        medium.pack(side="left", padx=5, pady=10)

        hard = tk.Radiobutton(
            toolbar,
            text="Hard",
            variable=radiovar,
            value='hard',
            command=self.diff_select
        )
        hard.pack(side="left", padx=5, pady=10)

        speed = tk.Label(
            toolbar,
            text="00.0",
            bg='white',
            fg='black'
        )
        speed.pack(side="right", padx=5, pady=10)

        speed_label = tk.Label(
            toolbar,
            text="Words per minute:"
        )
        speed_label.pack(side="right", padx=5, pady=10)

        return {'radiovar': radiovar, 'speed': speed}

    def render_body(self):
        ttext = tk.Text(
            master=self,
            wrap='word',
            width=100,
            height=10
        )
        ttext.bind("<Key>", input_blocker)
        ttext.pack()

        user_input = tk.Text(
            master=self,
            wrap='word',
            width=100,
            height=10
        )
        user_input.pack()

        options = tk.Frame(
            self,
            highlightthickness=1,
            highlightbackground='white'
        )
        start_button = tk.Button(
            options,
            text="Start",
        )
        start_button.place(relx=0.5, rely=0.5)

        return {'ttext': ttext, 'user_input': user_input}

    def diff_select(self):
        try:
            difficulty = self.UI['toolbar']['radiovar'].get()
        except AttributeError:
            difficulty = DEFAULT_DIFFICULTY
        ttext_content = Offline().difficulty(f'{difficulty}')
        self.set_ttext_content(ttext_content)

    def set_ttext_content(self, content):
        self.UI['main']['ttext'].delete("1.0", "end")
        self.UI['main']['ttext'].insert('1.0', content)




if __name__ == "__main__":
    app = TypingTest()
    app.mainloop()