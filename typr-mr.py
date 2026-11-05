import tkinter as tk
import random
import urllib.request

class TypeTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("30-Second Typing Speed Test")
        
        # 1. the bellow are the codes that allow to fetch from the internet, if it is offline it uses the existing list or words.
        try:
            url = "http://www.mit.edu/~ecprice/wordlist.10000"
            response = urllib.request.urlopen(url)
            all_words = response.read().decode('utf-8').splitlines()
            short_words = [word for word in all_words if len(word) <= 10]
        except:
            short_words = [
                "python", "code", "speed", "test", "fast", "type",
                "apple", "banana", "computer", "keyboard", "mouse", 
                "screen", "window", "door", "table", "chair", 
                "pencil", "paper", "book", "notebook", "school"
            ]
        
        # 2. paragraph generator
        selected_words = random.choices(short_words, k=25)
        self.target_paragraph = " ".join(selected_words)
        
        # timer variables
        self.time_left = 30
        self.timer_running = False
        
        # --- UI Components ---
        tk.Label(root, text="Type as much as you can in 30 seconds:", font=("Arial", 14)).pack(pady=10)
        
        # Text widget that display the target paragraph
        self.text_display = tk.Text(root, font=("Arial", 14), wrap="word", height=4, width=50, bg="#fff9e6", bd=2, relief="solid")
        self.text_display.pack(pady=10)
        self.text_display.insert("1.0", self.target_paragraph)
        self.text_display.config(state="disabled")
        
        # Configure text color tags for highlighting
        self.text_display.tag_config("correct", foreground="gray", background="#d3ffd3")
        self.text_display.tag_config("incorrect", foreground="red", background="#ffcccc")
        # Typed wrongly (bright red with soft red background)
        
        # timmer label
        self.timer_label = tk.Label(root, text=f"Time Left: {self.time_left}s", font=("Arial", 14, "bold"), fg="red")
        self.timer_label.pack(pady=5)
        
        # the place to type on
        self.input_entry = tk.Entry(root, font=("Arial", 14), width=50)
        self.input_entry.pack(pady=10)
        self.input_entry.focus() 
        
        # Bind key events for live highlighting, starting timer, and submitting
        self.input_entry.bind("<KeyRelease>", self.on_key_release)
        self.input_entry.bind("<Return>", self.check_typing)
        
        # Result displayer
        self.result_label = tk.Label(root, text="", font=("Arial", 13))
        self.result_label.pack(pady=10)

    def on_key_release(self, event):
        # the way to start the timmer when the user starts typind
        if not self.timer_running and event.keysym not in ("Return", "BackSpace", "Shift_L", "Shift_R", "Control_L", "Alt_L", "Caps_Lock"):
            if self.time_left > 0:
                self.timer_running = True
                self.update_timer()

        # storage for the user's typed text
        user_text = self.input_entry.get()
        
        # lets the widget to edit and highlight the textes
        self.text_display.config(state="normal")
        self.text_display.tag_remove("correct", "1.0", "end")
        self.text_display.tag_remove("incorrect", "1.0", "end")
        
        # Compare user input character by character
        for i, char in enumerate(user_text):
            if i < len(self.target_paragraph):
                start_idx = f"1.0 + {i} chars"
                end_idx = f"1.0 + {i+1} chars"
                
                if char == self.target_paragraph[i]:
                    self.text_display.tag_add("correct", start_idx, end_idx)
                else:
                    self.text_display.tag_add("incorrect", start_idx, end_idx)
                    
        # no more tyoing part
        self.text_display.config(state="disabled")

    def update_timer(self):
        if self.timer_running:
            if self.time_left > 0:
                self.timer_label.config(text=f"Time Left: {self.time_left}s")
                self.time_left -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_label.config(text=" Time's Up!   !!! I'm sorry for despicable words it's random words from the internet !!!", fg="purple")
                self.time_is_up()

    def time_is_up(self):
        self.timer_running = False
        self.input_entry.config(state="disabled")  # Lock input box
        self.calculate_results()

    def check_typing(self, event):
        if not self.timer_running:
            return
        
        self.timer_running = False
        self.input_entry.config(state="disabled")
        self.calculate_results()

    def calculate_results(self):
        user_text = self.input_entry.get().strip()
        words_typed = len(user_text.split())
        
        time_elapsed_minutes = (30 - self.time_left) / 60
        wpm = int(words_typed / time_elapsed_minutes) if time_elapsed_minutes > 0 else 0
            
        # Error calculation
        errors = 0
        for i, char in enumerate(user_text):
            if i < len(self.target_paragraph):
                if char != self.target_paragraph[i]:
                    errors += 1
            else:
                errors += 1
                
        self.result_label.config(
            text=f"🏁 Test Finished! Speed: {wpm} WPM | Words: {words_typed} | Errors: {errors}", 
            fg="green"
        )

if __name__ == "__main__":
    root = tk.Tk()
    TypeTimer(root)
    root.mainloop()