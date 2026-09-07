import customtkinter as ctk
from tkinter import messagebox
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = "<SECRET>"
MODEL_NAME = "gemini-2.5-flash"
genai.configure(api_key=GEMINI_API_KEY)

# Theme setup
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GeminiChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gemini AI Chat")
        self.geometry("800x650")
        self.minsize(700, 550)

        # Gemini model
        try:
            self.model = genai.GenerativeModel(MODEL_NAME)
            self.chat = self.model.start_chat(history=[])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize Gemini:\n{e}")
            self.destroy()
            return

        # ---------------- UI ----------------
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        self.header = ctk.CTkFrame(self, corner_radius=0)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self.header,
            text="Gemini AI Chat",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.header,
            text="Powered by Google Gemini",
            font=ctk.CTkFont(size=12),
            text_color="gray70"
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="w")

        # Chat area
        self.chat_box = ctk.CTkTextbox(
            self,
            wrap="word",
            font=ctk.CTkFont(size=14),
            state="disabled"
        )
        self.chat_box.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")

        # Input area
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.input_box = ctk.CTkTextbox(
            self.input_frame,
            height=70,
            wrap="word",
            font=ctk.CTkFont(size=14)
        )
        self.input_box.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=100,
            height=70,
            command=self.send_message
        )
        self.send_button.grid(row=0, column=1, sticky="e")

        # Enter key behavior
        self.input_box.bind("<Control-Return>", self.send_message)

        self.write_message("Gemini", "Hello! How can I help you today?")

    def write_message(self, sender, message):
        self.chat_box.configure(state="normal")
        self.chat_box.insert("end", f"{sender}:\n{message}\n\n")
        self.chat_box.see("end")
        self.chat_box.configure(state="disabled")

    def send_message(self, event=None):
        user_text = self.input_box.get("1.0", "end").strip()
        if not user_text:
            return "break"

        self.input_box.delete("1.0", "end")
        self.write_message("You", user_text)

        self.send_button.configure(state="disabled", text="Sending...")
        self.update_idletasks()

        try:
            response = self.chat.send_message(user_text)
            reply = response.text
            self.write_message("Gemini", reply)
        except Exception as e:
            self.write_message("Error", str(e))
        finally:
            self.send_button.configure(state="normal", text="Send")

        return "break"

if __name__ == "__main__":
    app = GeminiChatApp()
    app.mainloop()
