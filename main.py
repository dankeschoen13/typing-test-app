import tkinter as tk
from tkinter import font, messagebox
from paragraphs import Offline
import math
import difflib

DEFAULT_DIFFICULTY = 'easy'
TYPING_TEST_DURATION = 60

class Utilities:

    @staticmethod
    def cols_config(widget, total, expand=None, default_weight=0, expand_weight=1):
        expand = expand or []
        for col in range(total):
            weight = expand_weight if col in expand else default_weight
            widget.grid_columnconfigure(col, weight=weight)

def input_blocker(event):
    return "break"

class TypingTest(tk.Tk):

    def __init__(self):
        super().__init__()

        self.BOLD_FONT = font.Font(weight='bold')
        self.utils = Utilities()

        self.title("Typing Test")
        self.minsize(800, 500)
        self.config(padx=50, pady=50)

        self.UI = dict()
        self.UI['toolbar'] = self.render_top_toolbar()
        self.UI['main'] = self.render_body()
        self.UI['timer'] = self.render_bottom_toolbar()
        # UI unpacking
        self.reference_text = self.UI['main']['ttext']
        self.user_input = self.UI['main']['user_input']

        self.duration = TYPING_TEST_DURATION
        self.timer_started = False
        self.diff_select()
        self.words_typed = ""
        self.char_counter = 0

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
            state='disabled',
            highlightthickness=0
        )
        user_input.bind('<KeyRelease>')
        user_input.pack(side="top", fill="both")
        user_input.tag_config("mistake", background="pink", foreground="black")

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
        self.utils.cols_config(options, 5, [1, 3])

        start_button = tk.Button(
            options,
            text="Start",
            command=self.start_test
        )
        start_button.grid(column=0, row=0, padx=5, pady=10)

        timer = tk.Label(
            options,
            text="Duration: 1:00",
            font=self.BOLD_FONT
        )
        timer.grid(column=2, row=0, padx=5, pady=10)

        stop_button = tk.Button(
            options,
            text='Stop',
            command=self.stop_test
        )
        stop_button.grid(column=4, row=0, padx=5, pady=10)

        return timer

    def diff_select(self):
        try:
            difficulty = self.UI['toolbar']['radiovar'].get()
        except AttributeError:
            difficulty = DEFAULT_DIFFICULTY
        ttext_content = Offline().difficulty(f'{difficulty}')
        self.set_ttext_content(ttext_content)

    def set_ttext_content(self, content):
        self.reference_text.delete("1.0", "end")
        self.reference_text.insert('1.0', content)

    def start_test(self):
        self.timer_started = True
        self.after(1000, self.countdown, self.duration)
        self.user_input.config(state='normal')
        self.user_input.delete("1.0", "end")
        # input_field.bind('<KeyRelease>', self.typing)

    def stop_test(self):
        self.timer_started = False

    def countdown(self, duration):
        timer_min = math.floor(duration / 60)
        timer_sec = duration % 60
        if timer_sec < 10:
            timer_sec = f"0{timer_sec}"

        if duration > 0 and self.timer_started:
            self.UI['timer'].config(
                text=f"Timer Started: {timer_min}:{timer_sec}"
            )
            self.after(1000, self.countdown, duration - 1)
        else:
            self.UI['timer'].config(
                text=f"Timer Stopped: {timer_min}:{timer_sec}"
            )
            self.calculate(duration)

    def calculate(self, duration):
        reference_text = self.reference_text.get('1.0', tk.END).strip()
        typed_text = self.user_input.get('1.0', tk.END).strip()

        ref_words = reference_text.split()
        typed_words = typed_text.split()

        ref_words_trimmed = ref_words[:len(typed_words)]

        matcher = difflib.SequenceMatcher(None, ref_words_trimmed, typed_words)
        mistakes = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag in ("replace", "delete", "insert"):
                mistakes += max(i2 - i1, j2 - j1)
                for k in range(j1, j2):
                    start = f"1.0+{self.get_word_start(typed_words, k)}c"
                    end = f"1.0+{self.get_word_end(typed_words, k)}c"
                    self.user_input.tag_add("mistake", start, end)

        factor = TYPING_TEST_DURATION / (TYPING_TEST_DURATION - duration)
        total_chars = len(typed_text.replace(" ", ""))
        raw_wpm = (total_chars / 5) * factor
        wpm = raw_wpm - mistakes
        messagebox.showinfo(
            title='Test Finished',
            message=f'Your score is: {wpm:.2f} words per minute. Mistakes {mistakes}'
        )
        self.UI['toolbar']['speed'].config(text=f"Record: {wpm:.2f} words per minute")
        self.user_input.config(state='disabled')

    @staticmethod
    def get_word_start(words, index):
        """Return character index where a word starts in joined text."""
        return len(
            " ".join(words[:index])
        ) + (1 if index > 0 else 0)

    @staticmethod
    def get_word_end(words, index):
        """Return character index where a word ends in joined text."""
        return len(" ".join(words[:index + 1]))

    # def typing(self, event):
    #     char_counter = 0
    #     self.words_typed = event.keysym
    #     print(self.words_typed)


if __name__ == "__main__":
    app = TypingTest()
    app.mainloop()