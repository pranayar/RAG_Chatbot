import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

from rag import RAG


class PhoneShopAI:

    def __init__(self, root):

        self.root = root
        self.root.title("Phone Shop AI")
        self.root.geometry("900x700")

        print("Starting AI...")

        self.bot = RAG()

        title = tk.Label(
            root,
            text="Phone Shop AI",
            font=("Arial", 18, "bold")
        )

        title.pack(pady=10)

        self.chat_box = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            font=("Arial", 11),
            height=25,
            state="disabled"
        )

        self.chat_box.pack(
            fill=tk.BOTH,
            expand=True,
            padx=10,
            pady=5
        )

        self.entry = tk.Entry(
            root,
            font=("Arial", 12)
        )

        self.entry.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        self.entry.bind("<Return>", self.send)

        button_frame = tk.Frame(root)

        button_frame.pack(fill=tk.X)

        send_button = tk.Button(
            button_frame,
            text="Send",
            command=self.send
        )

        send_button.pack(
            side=tk.LEFT,
            padx=10,
            pady=5
        )

        clear_button = tk.Button(
            button_frame,
            text="Clear Chat",
            command=self.clear_chat
        )

        clear_button.pack(
            side=tk.LEFT,
            padx=5
        )

        self.sources = scrolledtext.ScrolledText(
            root,
            height=6,
            font=("Arial", 10),
            state="disabled"
        )

        self.sources.pack(
            fill=tk.X,
            padx=10,
            pady=5
        )

        self.write_bot(
            "Hello! Ask me anything."
        )

    ######################################################

    def write_user(self, text):

        self.chat_box.config(state="normal")

        self.chat_box.insert(
            tk.END,
            f"\nYou:\n{text}\n\n"
        )

        self.chat_box.config(state="disabled")

        self.chat_box.see(tk.END)

    ######################################################

    def write_bot(self, text):

        self.chat_box.config(state="normal")

        self.chat_box.insert(
            tk.END,
            f"Bot:\n{text}\n\n"
        )

        self.chat_box.config(state="disabled")

        self.chat_box.see(tk.END)

    ######################################################

    def stream_token(self, token):
    
        self.root.after(
            0,
            lambda: self.append_token(token)
        )
    
    ######################################################
    
    def append_token(self, token):
    
        self.chat_box.config(state="normal")
    
        self.chat_box.insert(
            tk.END,
            token
        )
    
        self.chat_box.config(state="disabled")
    
        self.chat_box.see(tk.END)

    ######################################################

    def update_sources(self, sources):

        self.sources.config(state="normal")

        self.sources.delete(
            "1.0",
            tk.END
        )

        self.sources.insert(
            tk.END,
            "Sources\n\n"
        )

        if len(sources) == 0:

            self.sources.insert(
                tk.END,
                "No sources"
            )

        else:

            for s in sources:

                self.sources.insert(
                    tk.END,
                    "• " + s + "\n"
                )

        self.sources.config(state="disabled")

    ######################################################

    def send(self, event=None):

        question = self.entry.get().strip()

        if not question:
            return

        self.entry.delete(0, tk.END)

        self.write_user(question)

        # Print Assistant label only
        self.chat_box.config(state="normal")
        self.chat_box.insert(tk.END, "Bot:\n")
        self.chat_box.config(state="disabled")
        self.chat_box.see(tk.END)

        Thread(
            target=self.ask_ai,
            args=(question,),
            daemon=True
        ).start()
        ######################################################

    def ask_ai(self, question):

        answer, sources = self.bot.chat(
            question,
            callback=self.stream_token
        )

        self.root.after(
            0,
            lambda: self.display_answer(sources)
        )
    ######################################################

    def display_answer(self, sources):

        self.chat_box.config(state="normal")
    
        self.chat_box.insert(
            tk.END,
            "\n\n"
        )
    
        self.chat_box.config(state="disabled")
    
        self.chat_box.see(tk.END)
    
        self.update_sources(sources)

    ######################################################

    def clear_chat(self):

        self.bot.clear_history()

        self.chat_box.config(state="normal")

        self.chat_box.delete(
            "1.0",
            tk.END
        )

        self.chat_box.config(state="disabled")

        self.sources.config(state="normal")

        self.sources.delete(
            "1.0",
            tk.END
        )

        self.sources.config(state="disabled")

        self.write_bot(
            "Conversation cleared."
        )


##########################################################

root = tk.Tk()

app = PhoneShopAI(root)

root.mainloop()