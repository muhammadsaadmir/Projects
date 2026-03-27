import os
import math
import time
import json
import queue
import sqlite3
import threading
import datetime
import webbrowser
import subprocess
import tkinter as tk
from tkinter import scrolledtext

import psutil
import pyttsx3
import speech_recognition as sr

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from google import genai
except ImportError:
    genai = None


class EvaApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("EVA")
        self.root.geometry("1500x940")
        self.root.minsize(1280, 820)
        self.root.configure(bg="#02060d")

        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("EVA_GEMINI_MODEL", "gemini-3-flash-preview").strip()

        self.client = None
        if genai is not None and self.gemini_api_key:
            try:
                self.client = genai.Client(api_key=self.gemini_api_key)
            except Exception:
                self.client = None

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 178)
        self._pick_voice()

        self.recognizer = sr.Recognizer()

        self.mode = "boot"
        self.ai_badge = "GEMINI ONLINE" if self.client else "LOCAL MODE"
        self.phase = 0.0
        self.rot1 = 0.0
        self.rot2 = 0.0
        self.rot3 = 0.0
        self.sweep = 0.0

        self.continuous_mode = False
        self.stop_continuous_flag = False
        self.speaking_lock = threading.Lock()

        self.db = sqlite3.connect("eva_memory.db", check_same_thread=False)
        self._setup_db()

        self.build_ui()
        self.root.after(120, self.boot_system)

    # ----------------------------
    # basic helpers
    # ----------------------------
    def ui(self, fn, *args, **kwargs):
        self.root.after(0, lambda: fn(*args, **kwargs))

    def _pick_voice(self):
        try:
            voices = self.engine.getProperty("voices")
            if not voices:
                return
            preferred = None
            for voice in voices:
                name = getattr(voice, "name", "").lower()
                if any(v in name for v in ["ava", "victoria", "samantha", "karen", "moira"]):
                    preferred = voice.id
                    break
            self.engine.setProperty("voice", preferred or voices[0].id)
        except Exception:
            pass

    # ----------------------------
    # memory
    # ----------------------------
    def _setup_db(self):
        cur = self.db.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS facts (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
            """
        )
        self.db.commit()

    def save_memory(self, role: str, content: str):
        cur = self.db.cursor()
        cur.execute(
            "INSERT INTO memory (role, content, created_at) VALUES (?, ?, ?)",
            (role, content, datetime.datetime.now().isoformat())
        )
        self.db.commit()

    def get_recent_memory(self, limit: int = 12):
        cur = self.db.cursor()
        cur.execute("SELECT role, content FROM memory ORDER BY id DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        rows.reverse()
        return rows

    def remember_fact(self, key: str, value: str):
        cur = self.db.cursor()
        cur.execute("INSERT OR REPLACE INTO facts (key, value) VALUES (?, ?)", (key, value))
        self.db.commit()

    def recall_fact(self, key: str):
        cur = self.db.cursor()
        cur.execute("SELECT value FROM facts WHERE key = ?", (key,))
        row = cur.fetchone()
        return row[0] if row else None

    # ----------------------------
    # UI
    # ----------------------------
    def build_ui(self):
        top = tk.Frame(self.root, bg="#02060d", height=88)
        top.pack(fill="x", padx=18, pady=(10, 5))
        top.pack_propagate(False)

        self.title_label = tk.Label(
            top,
            text="EVA",
            font=("Arial", 28, "bold"),
            fg="white",
            bg="#02060d",
        )
        self.title_label.pack()

        subtitle = "Enhanced Virtual Assistant • Gemini edition • standalone"
        subtitle += " • ONLINE" if self.client else " • LOCAL"
        self.subtitle_label = tk.Label(
            top,
            text=subtitle,
            font=("Consolas", 11),
            fg="white",
            bg="#02060d",
        )
        self.subtitle_label.pack()

        info = tk.Frame(self.root, bg="#02060d", height=58)
        info.pack(fill="x", padx=18, pady=(0, 8))
        info.pack_propagate(False)

        self.status_label = tk.Label(
            info,
            text="STATUS : BOOTING",
            font=("Consolas", 12, "bold"),
            fg="white",
            bg="#08121c",
            width=24,
            height=2,
            relief="solid",
            bd=1,
        )
        self.status_label.pack(side="left")

        self.clock_label = tk.Label(
            info,
            text="TIME",
            font=("Consolas", 12, "bold"),
            fg="white",
            bg="#08121c",
            width=34,
            height=2,
            relief="solid",
            bd=1,
        )
        self.clock_label.pack(side="right")

        middle = tk.Frame(self.root, bg="#02060d")
        middle.pack(fill="both", expand=True, padx=18, pady=8)

        self.canvas = tk.Canvas(middle, bg="#03070f", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        bottom = tk.Frame(self.root, bg="#02060d", height=200)
        bottom.pack(fill="x", padx=18, pady=(5, 12))
        bottom.pack_propagate(False)

        chat_frame = tk.Frame(bottom, bg="#08121c", relief="solid", bd=1)
        chat_frame.pack(side="left", fill="both", expand=True, padx=(0, 12))

        self.chat = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            height=9,
            bg="#09131f",
            fg="white",
            insertbackground="white",
            font=("Consolas", 11),
            relief="flat",
            padx=10,
            pady=10,
        )
        self.chat.pack(fill="both", expand=True)
        self.chat.config(state="disabled")

        controls = tk.Frame(bottom, bg="#02060d")
        controls.pack(side="right", fill="y")

        self.entry = tk.Entry(
            controls,
            width=44,
            font=("Arial", 12),
            bg="#09131f",
            fg="white",
            insertbackground="white",
            relief="solid",
            bd=1,
        )
        self.entry.grid(row=0, column=0, columnspan=4, pady=(0, 8), padx=4, ipady=10)
        self.entry.bind("<Return>", self.process_text)

        tk.Button(controls, text="SEND", width=10, command=self.process_text).grid(row=1, column=0, padx=4)
        tk.Button(controls, text="VOICE", width=10, command=self.start_voice_once).grid(row=1, column=1, padx=4)
        tk.Button(controls, text="CONT", width=10, command=self.start_continuous_conversation).grid(row=1, column=2, padx=4)
        tk.Button(controls, text="STOP", width=10, command=self.stop_continuous_conversation).grid(row=1, column=3, padx=4)

    # ----------------------------
    # system
    # ----------------------------
    def boot_system(self):
        self.write("SYSTEM", "EVA LOADED")
        self.write("SYSTEM", f"RUNNING FILE: {os.path.abspath(__file__)}")

        if self.client:
            self.ai_badge = "GEMINI ONLINE"
        else:
            self.ai_badge = "LOCAL MODE"
            self.write("SYSTEM", "Gemini key not found. EVA will use local mode.")

        self.set_mode("idle")
        self.update_clock()
        self.animate()

    def set_mode(self, mode: str):
        self.mode = mode
        self.status_label.config(text=f"STATUS : {mode.upper()}")

    def update_clock(self):
        now = datetime.datetime.now().strftime("%A | %d %B %Y | %I:%M:%S %p")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    # ----------------------------
    # chat
    # ----------------------------
    def write(self, speaker: str, text: str):
        self.chat.config(state="normal")
        self.chat.insert(tk.END, f"{speaker}: {text}\n\n")
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def update_last_eva_message(self, text: str):
        self.chat.config(state="normal")
        content = self.chat.get("1.0", tk.END).rstrip("\n")
        blocks = content.split("\n\n") if content else []
        if blocks and blocks[-1].startswith("EVA:"):
            blocks[-1] = f"EVA: {text}"
            self.chat.delete("1.0", tk.END)
            self.chat.insert(tk.END, "\n\n".join(blocks) + "\n\n")
        else:
            self.chat.insert(tk.END, f"EVA: {text}\n\n")
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    # ----------------------------
    # speech
    # ----------------------------
    def speak(self, text: str):
        def _run():
            with self.speaking_lock:
                self.ui(self.set_mode, "speaking")
                self.engine.say(text)
                self.engine.runAndWait()
                if self.continuous_mode:
                    self.ui(self.set_mode, "continuous")
                else:
                    self.ui(self.set_mode, "idle")
        threading.Thread(target=_run, daemon=True).start()

    def reply(self, text: str):
        self.write("EVA", text)
        self.save_memory("assistant", text)
        self.speak(text)

    # ----------------------------
    # local fallback
    # ----------------------------
    def local_fallback_reply(self, user_text: str) -> str:
        text = user_text.lower().strip()

        if text in {"hello", "hi", "hey"}:
            return "Hello."
        if "how are you" in text:
            return "All systems are operating normally."
        if "who are you" in text:
            return "I am EVA, your futuristic assistant."
        if "what can you do" in text:
            return "I can talk with you, open apps, search the web, remember details, and use camera vision."
        if text in {"time", "what time is it"}:
            return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
        if text in {"date", "what is the date", "what day is it"}:
            return f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}."
        if "joke" in text:
            return "Why do programmers prefer dark mode? Because light attracts bugs."
        return "Gemini is unavailable right now, so I am using local mode."

    # ----------------------------
    # voice input
    # ----------------------------
    def start_voice_once(self):
        threading.Thread(target=self.listen_once, daemon=True).start()

    def listen_once(self):
        self.ui(self.set_mode, "listening")
        self.ui(self.write, "SYSTEM", "Listening...")

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)

            text = self.recognizer.recognize_google(audio)
            self.ui(self.write, "YOU (VOICE)", text)
            self.save_memory("user", text)
            self.handle(text)

        except sr.WaitTimeoutError:
            self.ui(self.write, "SYSTEM", "No voice detected.")
            self.ui(self.set_mode, "idle")
        except sr.UnknownValueError:
            self.ui(self.write, "SYSTEM", "Could not understand audio.")
            self.ui(self.set_mode, "idle")
        except Exception as e:
            self.ui(self.write, "SYSTEM", f"Voice error: {e}")
            self.ui(self.set_mode, "idle")

    def start_continuous_conversation(self):
        if self.continuous_mode:
            return
        self.continuous_mode = True
        self.stop_continuous_flag = False
        self.write("SYSTEM", "Continuous conversation enabled.")
        threading.Thread(target=self.continuous_loop, daemon=True).start()

    def stop_continuous_conversation(self):
        self.continuous_mode = False
        self.stop_continuous_flag = True
        self.set_mode("idle")
        self.write("SYSTEM", "Continuous conversation stopped.")

    def continuous_loop(self):
        self.ui(self.set_mode, "continuous")
        while self.continuous_mode and not self.stop_continuous_flag:
            try:
                with sr.Microphone() as source:
                    self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)

                text = self.recognizer.recognize_google(audio).strip()
                if not text:
                    continue

                self.ui(self.write, "YOU (VOICE)", text)
                self.save_memory("user", text)

                if text.lower() in {"stop listening", "stop conversation", "goodbye"}:
                    self.reply("Continuous conversation disabled.")
                    self.continuous_mode = False
                    self.stop_continuous_flag = True
                    self.ui(self.set_mode, "idle")
                    return

                self.handle(text)
                time.sleep(0.2)

            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                self.ui(self.write, "SYSTEM", f"Continuous mode error: {e}")
                self.continuous_mode = False
                self.ui(self.set_mode, "idle")
                return

    # ----------------------------
    # Mac controls
    # ----------------------------
    def mac_volume_up(self):
        os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) + 10)'")

    def mac_volume_down(self):
        os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) - 10)'")

    def mac_mute(self):
        os.system("osascript -e 'set volume with output muted'")

    def mac_unmute(self):
        os.system("osascript -e 'set volume without output muted'")

    def mac_lock_screen(self):
        os.system("/System/Library/CoreServices/Menu\\ Extras/User.menu/Contents/Resources/CGSession -suspend")

    def mac_sleep_display(self):
        os.system("pmset displaysleepnow")

    # ----------------------------
    # input handling
    # ----------------------------
    def process_text(self, event=None):
        text = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if not text:
            return
        self.write("YOU", text)
        self.save_memory("user", text)
        self.handle(text)

    def handle(self, text: str):
        lower = text.lower().strip()

        if lower in {"hello", "hi", "hey"}:
            self.reply("Hello.")
            return

        if "who are you" in lower:
            name = self.recall_fact("user_name")
            if name:
                self.reply(f"I am EVA, and you are {name}.")
            else:
                self.reply("I am EVA, your futuristic assistant.")
            return

        if "my name is" in lower:
            name = text.lower().replace("my name is", "").strip().title()
            if name:
                self.remember_fact("user_name", name)
                self.reply(f"Nice to meet you, {name}.")
            else:
                self.reply("Tell me your name again.")
            return

        if "what is my name" in lower:
            name = self.recall_fact("user_name")
            if name:
                self.reply(f"Your name is {name}.")
            else:
                self.reply("You have not told me your name yet.")
            return

        if "what can you do" in lower:
            self.reply("I can talk with you, open apps, search the web, control your Mac, remember details, and use camera vision.")
            return

        if "what do you remember" in lower:
            self.reply(self.summarize_memory())
            return

        if lower in {"time", "what time is it"}:
            self.reply(f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}.")
            return

        if lower in {"date", "what is the date", "what day is it"}:
            self.reply(f"Today is {datetime.datetime.now().strftime('%A, %d %B %Y')}.")
            return

        if "joke" in lower:
            self.reply("Why do programmers prefer dark mode? Because light attracts bugs.")
            return

        if "open chrome" in lower:
            self.open_app("Google Chrome", "Opening Chrome.")
            return

        if "open vscode" in lower or "open visual studio code" in lower:
            self.open_app("Visual Studio Code", "Opening VS Code.")
            return

        if "open spotify" in lower:
            self.open_app("Spotify", "Opening Spotify.")
            return

        if lower.startswith("quit "):
            app_name = text[5:].strip()
            if app_name:
                os.system(f'''osascript -e 'tell application "{app_name}" to quit' ''')
                self.reply(f"Quitting {app_name}.")
            else:
                self.reply("Tell me which app to quit.")
            return

        if "volume up" in lower:
            self.mac_volume_up()
            self.reply("Volume increased.")
            return

        if "volume down" in lower:
            self.mac_volume_down()
            self.reply("Volume decreased.")
            return

        if "mute volume" in lower or lower == "mute":
            self.mac_mute()
            self.reply("Volume muted.")
            return

        if "unmute volume" in lower or lower == "unmute":
            self.mac_unmute()
            self.reply("Volume unmuted.")
            return

        if "lock screen" in lower:
            self.mac_lock_screen()
            self.reply("Locking screen.")
            return

        if "sleep display" in lower:
            self.mac_sleep_display()
            self.reply("Putting display to sleep.")
            return

        if "open google" in lower:
            webbrowser.open("https://www.google.com")
            self.reply("Opening Google.")
            return

        if "open youtube" in lower:
            webbrowser.open("https://www.youtube.com")
            self.reply("Opening YouTube.")
            return

        if lower.startswith("search "):
            query = text[7:].strip()
            if query:
                webbrowser.open(f"https://www.google.com/search?q={query}")
                self.reply(f"Searching the web for {query}.")
            else:
                self.reply("Please give me something to search for.")
            return

        if "camera" in lower or "vision" in lower:
            threading.Thread(target=self.open_camera_preview, daemon=True).start()
            self.reply("Opening camera vision.")
            return

        threading.Thread(target=self.ask_gemini, args=(text,), daemon=True).start()

    def open_app(self, app_name: str, success_text: str):
        try:
            if os.name == "posix":
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen([app_name])
            self.reply(success_text)
        except Exception as e:
            self.reply(f"I couldn't open {app_name}. {e}")

    def open_camera_preview(self):
        if cv2 is None:
            self.ui(self.write, "SYSTEM", "OpenCV is not installed.")
            return

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.ui(self.write, "SYSTEM", "Could not open camera.")
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cv2.imshow("EVA Vision", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

    # ----------------------------
    # Gemini
    # ----------------------------
    def summarize_memory(self):
        rows = self.get_recent_memory(8)
        if not rows:
            return "I do not remember anything yet."
        summary = []
        for role, content in rows[-4:]:
            who = "You" if role == "user" else "I"
            summary.append(f"{who} said: {content}")
        return "Recent memory: " + " | ".join(summary)

    def extract_gemini_text(self, response) -> str:
        text = getattr(response, "text", None)
        if text:
            return text.strip()

        try:
            candidates = getattr(response, "candidates", [])
            parts = []
            for candidate in candidates:
                content = getattr(candidate, "content", None)
                if not content:
                    continue
                for part in getattr(content, "parts", []):
                    ptext = getattr(part, "text", None)
                    if ptext:
                        parts.append(ptext)
            return "\n".join(parts).strip()
        except Exception:
            return ""

    def ask_gemini(self, user_text: str):
        if not self.client:
            self.ai_badge = "LOCAL MODE"
            self.reply(self.local_fallback_reply(user_text))
            return

        self.ui(self.set_mode, "thinking")
        self.ui(self.write, "SYSTEM", "Thinking...")
        self.ui(self.write, "EVA", "")

        try:
            memory_rows = self.get_recent_memory(10)
            memory_text = "\n".join([f"{role}: {content}" for role, content in memory_rows])

            prompt = (
                "You are EVA, a futuristic desktop AI assistant.\n"
                "Be concise, helpful, natural, and strong at spoken replies.\n\n"
                f"Relevant memory:\n{memory_text}\n\n"
                f"Current user message:\n{user_text}"
            )

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )

            final_text = self.extract_gemini_text(response)
            if not final_text:
                final_text = self.local_fallback_reply(user_text)

            self.ai_badge = "GEMINI ONLINE"
            self.save_memory("assistant", final_text)
            self.ui(self.update_last_eva_message, final_text)
            self.speak(final_text)

        except Exception:
            fallback = self.local_fallback_reply(user_text)
            self.ai_badge = "LOCAL MODE"
            self.ui(self.update_last_eva_message, fallback)
            self.save_memory("assistant", fallback)
            self.speak(fallback)

        if self.continuous_mode:
            self.ui(self.set_mode, "continuous")
        else:
            self.ui(self.set_mode, "idle")

    # ----------------------------
    # animation
    # ----------------------------
    def animate(self):
        self.canvas.delete("all")

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        cx = w // 2
        cy = h // 2 - 10

        self.rot1 = (self.rot1 + 1.0) % 360
        self.rot2 = (self.rot2 - 1.6) % 360
        self.rot3 = (self.rot3 + 2.3) % 360
        self.sweep = (self.sweep + 3.0) % 360
        self.phase += 0.07

        main = "#18bfff"
        white = "#d7f8ff"
        gold = "#58d6ff"

        outer_r = min(w, h) * 0.28
        mid_r = outer_r * 0.78
        inner_r = outer_r * 0.56
        core_r = outer_r * 0.18

        # grid
        for x in range(0, w, 42):
            self.canvas.create_line(x, 0, x, h, fill="#0b1a28", width=1)
        for y in range(0, h, 42):
            self.canvas.create_line(0, y, w, y, fill="#0b1a28", width=1)

        # side text
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent

        self.canvas.create_text(120, 70, text=f"CPU {cpu:.0f}%", fill="white", font=("Consolas", 12))
        self.canvas.create_text(120, 102, text=f"RAM {ram:.0f}%", fill="white", font=("Consolas", 12))
        self.canvas.create_text(120, 134, text=f"MODE {self.mode.upper()}", fill="white", font=("Consolas", 12))

        if self.mode == "thinking":
            self.canvas.create_text(w - 130, 40, text="THINKING...", fill="white", font=("Consolas", 13, "bold"))

        badge_color = "#55e4ff" if self.ai_badge == "GEMINI ONLINE" else "#ffd76a"
        self.canvas.create_rectangle(w - 260, 62, w - 40, 100, outline=badge_color, width=2)
        self.canvas.create_text(w - 150, 81, text=self.ai_badge, fill="white", font=("Consolas", 12, "bold"))

        # left panel
        self.canvas.create_rectangle(70, 170, 330, 610, outline=main, width=2)
        self.canvas.create_text(200, 200, text="SCAN METRICS", fill="white", font=("Consolas", 14, "bold"))
        self.canvas.create_text(
            200, 290,
            text=(
                f"CORE TEMP : 37.2 C\n"
                f"VOICE LINK: ACTIVE\n"
                f"HUD RENDER: STABLE\n"
                f"AI STATUS : {self.ai_badge}\n"
                f"SECURITY  : CLEAR\n"
                f"LATENCY   : 042 ms"
            ),
            fill="white",
            font=("Consolas", 11),
            justify="left"
        )
        for i in range(11):
            y = 430 + i * 16
            x2 = 290 - i * 7
            self.canvas.create_line(110, y, x2, y, fill=main, width=2)

        # right panel
        self.canvas.create_rectangle(w - 330, 170, w - 70, 610, outline=main, width=2)
        self.canvas.create_text(w - 200, 200, text="SIGNAL TELEMETRY", fill="white", font=("Consolas", 14, "bold"))
        self.canvas.create_text(
            w - 200, 290,
            text=(
                f"AUDIO LVL : 78\n"
                f"SIGNAL    : CLEAN\n"
                f"MODEL     : {self.model_name[:18]}\n"
                f"MEMORY    : READY\n"
                f"CAMERA    : {'READY' if cv2 else 'OFF'}\n"
                f"SYNC      : LOCKED"
            ),
            fill="white",
            font=("Consolas", 11),
            justify="left"
        )
        for i in range(11):
            y = 430 + i * 16
            x1 = w - 290 + i * 7
            self.canvas.create_line(x1, y, w - 110, y, fill=main, width=2)

        # reactor rings
        self.canvas.create_oval(cx - outer_r - 34, cy - outer_r - 34, cx + outer_r + 34, cy + outer_r + 34, outline="#0f2c3b", width=2)
        self.canvas.create_oval(cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r, outline=main, width=3)
        self.canvas.create_oval(cx - mid_r, cy - mid_r, cx + mid_r, cy + mid_r, outline=white, width=2)
        self.canvas.create_oval(cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r, outline=main, width=2)

        self.canvas.create_arc(cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r, start=self.rot1, extent=120, style="arc", outline=main, width=9)
        self.canvas.create_arc(cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r, start=180 - self.rot1, extent=34, style="arc", outline=main, width=9)
        self.canvas.create_arc(cx - mid_r, cy - mid_r, cx + mid_r, cy + mid_r, start=90 + self.rot2, extent=86, style="arc", outline=white, width=6)
        self.canvas.create_arc(cx - mid_r, cy - mid_r, cx + mid_r, cy + mid_r, start=248 - self.rot2, extent=44, style="arc", outline=gold, width=4)
        self.canvas.create_arc(cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r, start=38 + self.rot3, extent=126, style="arc", outline=white, width=4)
        self.canvas.create_arc(cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r, start=220 - self.rot3, extent=52, style="arc", outline=main, width=4)

        # sweep
        sweep_r = outer_r * 0.84
        self.canvas.create_arc(
            cx - sweep_r, cy - sweep_r, cx + sweep_r, cy + sweep_r,
            start=self.sweep, extent=18, style="pieslice", outline="", fill="#103d52"
        )

        # ticks
        for i in range(100):
            angle = math.radians(i * 3.6)
            r1 = mid_r * 0.92
            r2 = mid_r * (1.02 if i % 5 else 1.11)
            x1 = cx + math.cos(angle) * r1
            y1 = cy + math.sin(angle) * r1
            x2 = cx + math.cos(angle) * r2
            y2 = cy + math.sin(angle) * r2
            self.canvas.create_line(x1, y1, x2, y2, fill=main if i % 5 else white, width=1 if i % 5 else 2)

        # orbit dots
        for i in range(12):
            angle = math.radians((self.rot1 * 2) + i * 30)
            orbit_r = outer_r * 0.72
            x = cx + math.cos(angle) * orbit_r
            y = cy + math.sin(angle) * orbit_r
            self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=gold, outline="")

        # central wireframe head inspired mesh
        head_w = inner_r * 0.82
        head_h = inner_r * 1.00
        self.canvas.create_oval(cx - head_w * 0.42, cy - head_h * 0.62, cx + head_w * 0.42, cy + head_h * 0.50, outline=main, width=2)
        self.canvas.create_line(cx, cy - head_h * 0.62, cx, cy + head_h * 0.50, fill=main, width=1)
        for f in [-0.30, -0.15, 0.0, 0.15, 0.30]:
            self.canvas.create_oval(
                cx - head_w * (0.42 - abs(f) * 0.25),
                cy - head_h * (0.62 - abs(f) * 0.12),
                cx + head_w * (0.42 - abs(f) * 0.25),
                cy + head_h * (0.50 - abs(f) * 0.08),
                outline="#0e7aa8",
                width=1
            )
        for frac in [-0.30, -0.15, 0, 0.15, 0.30]:
            x = cx + head_w * frac
            self.canvas.create_line(x, cy - head_h * 0.58, x, cy + head_h * 0.42, fill="#0e7aa8", width=1)
        self.canvas.create_line(cx - head_w * 0.18, cy - head_h * 0.10, cx + head_w * 0.18, cy - head_h * 0.10, fill=main, width=1)
        self.canvas.create_line(cx - head_w * 0.10, cy + head_h * 0.12, cx + head_w * 0.10, cy + head_h * 0.12, fill=main, width=1)
        self.canvas.create_line(cx - head_w * 0.18, cy + head_h * 0.44, cx + head_w * 0.18, cy + head_h * 0.44, fill=main, width=1)

        # core glow
        pulse = 1.0 + 0.08 * math.sin(self.phase * 4)
        glow = core_r * 2.0 * pulse
        self.canvas.create_oval(cx - glow, cy - glow, cx + glow, cy + glow, fill="#0d3240", outline="")
        self.canvas.create_oval(cx - core_r * pulse, cy - core_r * pulse, cx + core_r * pulse, cy + core_r * pulse, fill="#07111a", outline="#9afcff", width=2)
        pulse2 = 1.0 + 0.12 * math.sin(self.phase * 6)
        glow2 = core_r * 2.5 * pulse2
        self.canvas.create_oval(cx - glow2, cy - glow2, cx + glow2, cy + glow2, outline="#1c5a70", width=2)

        # waveform
        wave_y = cy + outer_r * 0.74
        wave_w = outer_r * 1.35
        left_x = cx - wave_w / 2
        segments = 42
        step = wave_w / segments

        for i in range(segments):
            x1 = left_x + i * step
            x2 = x1 + step

            if self.mode == "speaking":
                amp = 10 + 20 * abs(math.sin(self.phase * 7 + i * 0.35))
            elif self.mode == "listening":
                amp = 6 + 12 * abs(math.sin(self.phase * 4 + i * 0.28))
            elif self.mode == "thinking":
                amp = 4 + 8 * abs(math.sin(self.phase * 5 + i * 0.22))
            elif self.mode == "continuous":
                amp = 5 + 9 * abs(math.sin(self.phase * 3 + i * 0.20))
            else:
                amp = 2 + 3 * abs(math.sin(self.phase * 2 + i * 0.18))

            y1 = wave_y + math.sin(self.phase * 4 + i * 0.3) * amp
            y2 = wave_y + math.sin(self.phase * 4 + i * 0.3 + 0.7) * amp
            self.canvas.create_line(x1, y1, x2, y2, fill=main, width=2, smooth=True)

        self.root.after(40, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = EvaApp(root)
    root.mainloop()