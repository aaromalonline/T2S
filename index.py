import tkinter as tk
from tkinter import ttk
import pyttsx3

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to Speech Application")
        self.root.geometry("500x300")
        
        # Initialize the TTS engine
        self.engine = pyttsx3.init()
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create and configure text area
        self.text_label = ttk.Label(self.main_frame, text="Enter text to convert to speech:")
        self.text_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.text_area = tk.Text(self.main_frame, height=8, width=50, wrap=tk.WORD)
        self.text_area.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        # Create controls frame
        self.controls_frame = ttk.Frame(self.main_frame)
        self.controls_frame.grid(row=2, column=0, columnspan=2)
        
        # Speed control
        self.speed_label = ttk.Label(self.controls_frame, text="Speed:")
        self.speed_label.grid(row=0, column=0, padx=(0, 5))
        
        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(
            self.controls_frame,
            from_=0.5,
            to=2.0,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            length=200
        )
        self.speed_scale.grid(row=0, column=1)
        
        # Speak button
        self.speak_button = ttk.Button(
            self.main_frame,
            text="Speak",
            command=self.speak_text
        )
        self.speak_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_label = ttk.Label(
            self.main_frame,
            text="Ready",
            foreground="green"
        )
        self.status_label.grid(row=4, column=0, columnspan=2)
    
    def speak_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            self.status_label.config(text="Speaking...", foreground="blue")
            self.root.update()
            
            # Configure speech rate
            self.engine.setProperty('rate', int(self.engine.getProperty('rate') * self.speed_var.get()))
            
            # Speak the text
            self.engine.say(text)
            self.engine.runAndWait()
            
            # Reset speech rate
            self.engine.setProperty('rate', int(self.engine.getProperty('rate') / self.speed_var.get()))
            
            self.status_label.config(text="Ready", foreground="green")
        else:
            self.status_label.config(text="Please enter some text!", foreground="red")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()