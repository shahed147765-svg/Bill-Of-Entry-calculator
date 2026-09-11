import tkinter as tk
import threading
import speech_recognition as sr
import pyautogui
import pyperclip
import time

class VoiceTypingTool:
    def __init__(self, root):
        self.root = root
        self.root.title("বাংলা Voice Typing (Nikosh) - Fixed Space")
        self.root.geometry("440x310")
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 250
        self.recognizer.dynamic_energy_threshold = True
        self.is_listening = False

        tk.Label(root, text="Bangla Voice → MS Word (Nikosh)", 
                 font=("Arial", 14, "bold"), fg="#1a5276").pack(pady=8)

        tk.Label(root, text="প্রতি বাক্য/কথার শেষে অটো স্পেস হবে", 
                 font=("Arial", 11), fg="#27ae60").pack(pady=2)

        self.status_label = tk.Label(root, text="Status: বন্ধ আছে", font=("Arial", 12, "bold"), fg="red")
        self.status_label.pack(pady=12)

        self.btn_toggle = tk.Button(root, text="🎙️ কথা বলা শুরু করুন", font=("Arial", 12, "bold"),
                                    bg="#27ae60", fg="white", padx=15, pady=8,
                                    command=self.toggle_listening)
        self.btn_toggle.pack(pady=10)

        tk.Label(root, text="টিপস: একটু থেমে থেমে + স্পষ্ট করে কথা বলুন", 
                 font=("Arial", 9), fg="gray").pack(side="bottom", pady=10)

    def toggle_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.btn_toggle.config(text="⏹️ বন্ধ করুন", bg="#c0392b")
            self.status_label.config(text="Status: শুনছি... কথা বলুন", fg="green")
            threading.Thread(target=self.listen_and_type, daemon=True).start()
        else:
            self.is_listening = False
            self.btn_toggle.config(text="🎙️ কথা বলা শুরু করুন", bg="#27ae60")
            self.status_label.config(text="Status: বন্ধ আছে", fg="red")

    def listen_and_type(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                    text = self.recognizer.recognize_google(audio, language='bn-BD')
                    
                    if text and self.is_listening:
                        clean_text = text.strip()
                        
                        if clean_text:
                            # টেক্সট পেস্ট করা
                            pyperclip.copy(clean_text)
                            pyautogui.hotkey('ctrl', 'v')
                            time.sleep(0.08)
                            
                            # জোর করে স্পেস দেওয়া (এই লাইনটাই মূল ফিক্স)
                            pyautogui.press('space')
                            time.sleep(0.05)
                        
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print("Error:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceTypingTool(root)
    root.mainloop()