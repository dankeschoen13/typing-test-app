import tkinter as tk
from paragraphs import Offline

DEFAULT_DIFFICULTY = 'easy'

def input_blocker(event):
    return "break"

class TypingTest(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Typing Test")
        self.minsize(800, 500)
        self.config(padx=50, pady=50)

        self.UI = dict()
        self.UI['toolbar'] = self.render_top_toolbar()
        self.UI['main'] = self.render_body()
        self.UI['more_options'] = self.render_bottom_toolbar()

        self.diff_select()

    def render_top_toolbar(self):
        toolbar = tk.Frame(self, highlightbackground='white', highlightthickness=1)
        toolbar.pack(side='top', fill='x')

        radiovar = tk.StringVar()
        radiovar.set('easy')

        easy = tk.Radiobutton(
            toolbar,
            text="Easy",
            variable=radiovar,
            value='easy',
            command=self.diff_select
        )
        easy.pack(side='left', padx=5, pady=10)

        medium = tk.Radiobutton(
            toolbar,
            text="Medium",
            variable=radiovar,
            value='medium',
            command = self.diff_select
        )
        medium.pack(side='left', padx=5, pady=10)

        hard = tk.Radiobutton(
            toolbar,
            text="Hard",
            variable=radiovar,
            value='hard',
            command=self.diff_select
        )
        hard.pack(side='left', padx=5, pady=10)

        speed = tk.Label(
            toolbar,
            text="00.0",
            bg='white',
            fg='black'
        )
        speed.pack(side='right', padx=5, pady=10)

        speed_label = tk.Label(
            toolbar,
            text="Words per minute:"
        )
        speed_label.pack(side='right', padx=5, pady=10)

        return {'radiovar': radiovar, 'speed': speed}

    def render_body(self):
        paned = tk.PanedWindow(
            self,
            orient="vertical"
        )
        paned.pack(fill='both', expand=True)

        ttext = tk.Text(
            master=paned,
            wrap='word',
            width=100,
            height=10,
            highlightthickness=0,
        )
        ttext.bind("<Key>", input_blocker)
        ttext.pack(side="top", fill="both")

        user_input = tk.Text(
            master=paned,
            wrap='word',
            width=100,
            height=10,
            highlightthickness=0
        )
        user_input.pack(side="top", fill="both")

        paned.add(ttext)
        paned.add(user_input)

        return {'ttext': ttext, 'user_input': user_input}

    def render_bottom_toolbar(self):
        options = tk.Frame(
            self,
            highlightthickness=1,
            highlightbackground='white'
        )
        options.pack(side="bottom", fill="x")

        start_button = tk.Button(
            options,
            text="Start"
        )
        start_button.pack(side='left', padx=5, pady=10)

        timer = tk.Label(
            options,
            text="Timer:"
        )
        timer.pack(side='right', padx=5, pady=10)

        return timer

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