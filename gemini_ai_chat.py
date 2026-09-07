import re
import threading
import tkinter as tk
import customtkinter as ctk
from google import genai


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

GEMINI_API_KEY = "enter_your_api"
MODEL_NAME = "gemini-3.5-flash"

client = genai.Client(
    api_key=GEMINI_API_KEY
)

chat = client.chats.create(
    model=MODEL_NAME
)


# ============================================================
# APP CONFIGURATION
# ============================================================

ctk.set_default_color_theme("blue")


THEMES = {
    "light": {
        "bg": "#FFFFFF",
        "header": "#F7F8FA",
        "input": "#F7F8FA",
        "user_bubble": "#2563EB",
        "bot_bubble": "#F1F3F5",
        "border": "#E2E5EA",
        "text": "#111827",
        "secondary_text": "#6B7280",
        "accent": "#2563EB",
        "status_online": "#059669",
        "new_chat_bg": "#EEF1F5",
        "new_chat_hover": "#E2E6ED",
        "input_wrapper": "#F1F3F5",
        "placeholder": "#9CA3AF",
        "send_bg": "#2563EB",
        "send_hover": "#1D4ED8",
        "avatar_bg": "#DBEAFE",
        "avatar_text": "#2563EB",
        "inline_code_bg": "#F1F5F9",
        "inline_code_text": "#2563EB",
        "codeblock_bg": "#F6F8FA",
        "codeblock_border": "#E2E5EA",
        "codeblock_header": "#EDF0F3",
        "codeblock_label": "#6B7280",
        "codeblock_text": "#1F2328",
        "thinking_dots": "#9CA3AF",
        "toggle_icon": "🌙",
    },
    "dark": {
        "bg": "#0B0F14",
        "header": "#11161D",
        "input": "#11161D",
        "user_bubble": "#2563EB",
        "bot_bubble": "#171D26",
        "border": "#252D38",
        "text": "#F3F4F6",
        "secondary_text": "#9CA3AF",
        "accent": "#60A5FA",
        "status_online": "#34D399",
        "new_chat_bg": "#1D2633",
        "new_chat_hover": "#273342",
        "input_wrapper": "#1A2230",
        "placeholder": "#667085",
        "send_bg": "#2563EB",
        "send_hover": "#1D4ED8",
        "avatar_bg": "#1D3A78",
        "avatar_text": "#93C5FD",
        "inline_code_bg": "#111827",
        "inline_code_text": "#93C5FD",
        "codeblock_bg": "#0D1117",
        "codeblock_border": "#242B35",
        "codeblock_header": "#161B22",
        "codeblock_label": "#8B949E",
        "codeblock_text": "#D1D5DB",
        "thinking_dots": "#6B7280",
        "toggle_icon": "☀",
    },
}


# ============================================================
# MAIN APP
# ============================================================

class GeminiChatbot(ctk.CTk):

    def __init__(self):

        super().__init__()

        self.title("Gemini AI Chat")
        self.geometry("1000x720")
        self.minsize(750, 550)

        self.theme_name = "light"
        self.colors = THEMES[self.theme_name]

        ctk.set_appearance_mode(self.theme_name)

        self.configure(
            fg_color=self.colors["bg"]
        )

        self.thinking = False
        self.thinking_step = 0
        self.history = []

        self.create_header()
        self.create_chat_area()
        self.create_input_area()

        self.after(
            100,
            lambda: self.add_bot_message(
                "Hello! I'm Gemini. How can I help you today?"
            )
        )

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        self.header = ctk.CTkFrame(
            self,
            height=72,
            corner_radius=0,
            fg_color=self.colors["header"]
        )

        self.header.pack(
            fill="x"
        )

        self.header.pack_propagate(False)

        # Logo
        self.logo_label = ctk.CTkLabel(
            self.header,
            text="✦",
            font=("Segoe UI", 28, "bold"),
            text_color=self.colors["accent"]
        )

        self.logo_label.pack(
            side="left",
            padx=(24, 10)
        )

        # Title section
        title_frame = ctk.CTkFrame(
            self.header,
            fg_color="transparent"
        )

        title_frame.pack(
            side="left"
        )

        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Gemini AI",
            font=("Segoe UI", 19, "bold"),
            text_color=self.colors["text"]
        )

        self.title_label.pack(
            anchor="w"
        )

        self.status_label = ctk.CTkLabel(
            title_frame,
            text="● Online",
            font=("Segoe UI", 11),
            text_color=self.colors["status_online"]
        )

        self.status_label.pack(
            anchor="w"
        )

        # Theme toggle button
        self.theme_toggle_btn = ctk.CTkButton(
            self.header,
            text=self.colors["toggle_icon"],
            width=40,
            height=36,
            corner_radius=10,
            fg_color=self.colors["new_chat_bg"],
            hover_color=self.colors["new_chat_hover"],
            text_color=self.colors["text"],
            font=("Segoe UI", 14, "bold"),
            command=self.toggle_theme
        )

        self.theme_toggle_btn.pack(
            side="right",
            padx=(0, 20)
        )

        # New chat button
        self.new_chat_btn = ctk.CTkButton(
            self.header,
            text="New Chat",
            width=105,
            height=36,
            corner_radius=10,
            fg_color=self.colors["new_chat_bg"],
            hover_color=self.colors["new_chat_hover"],
            text_color=self.colors["text"],
            font=("Segoe UI", 12, "bold"),
            command=self.new_chat
        )

        self.new_chat_btn.pack(
            side="right",
            padx=(0, 10)
        )

    # ========================================================
    # CHAT AREA
    # ========================================================

    def create_chat_area(self):

        self.chat_scroll = ctk.CTkScrollableFrame(
            self,
            fg_color=self.colors["bg"],
            corner_radius=0
        )

        self.chat_scroll.pack(
            fill="both",
            expand=True
        )

    # ========================================================
    # INPUT AREA
    # ========================================================

    def create_input_area(self):

        self.input_container = ctk.CTkFrame(
            self,
            height=82,
            fg_color=self.colors["input"],
            corner_radius=0
        )

        self.input_container.pack(
            fill="x"
        )

        self.input_container.pack_propagate(False)

        # Input wrapper
        self.input_wrapper = ctk.CTkFrame(
            self.input_container,
            height=48,
            corner_radius=14,
            fg_color=self.colors["input_wrapper"],
            border_width=1,
            border_color=self.colors["border"]
        )

        self.input_wrapper.pack(
            fill="x",
            expand=True,
            padx=(20, 10),
            pady=16,
            side="left"
        )

        self.message_entry = ctk.CTkEntry(
            self.input_wrapper,
            height=44,
            corner_radius=14,
            border_width=0,
            fg_color="transparent",
            placeholder_text="Message Gemini...",
            placeholder_text_color=self.colors["placeholder"],
            text_color=self.colors["text"],
            font=("Segoe UI", 14)
        )

        self.message_entry.pack(
            fill="both",
            expand=True,
            padx=10
        )

        self.message_entry.bind(
            "<Return>",
            self.send_message
        )

        # Send button
        self.send_button = ctk.CTkButton(
            self.input_container,
            text="➤",
            width=52,
            height=48,
            corner_radius=14,
            font=("Segoe UI", 19, "bold"),
            fg_color=self.colors["send_bg"],
            hover_color=self.colors["send_hover"],
            command=self.send_message
        )

        self.send_button.pack(
            side="right",
            padx=(0, 20),
            pady=16
        )

    # ========================================================
    # USER MESSAGE
    # ========================================================

    def add_user_message(self, message, record=True):

        row = ctk.CTkFrame(
            self.chat_scroll,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=(8, 8)
        )

        bubble = ctk.CTkFrame(
            row,
            fg_color=self.colors["user_bubble"],
            corner_radius=16
        )

        bubble.pack(
            side="right",
            padx=(150, 0)
        )

        label = ctk.CTkLabel(
            bubble,
            text=message,
            font=("Segoe UI", 14),
            text_color="white",
            justify="left",
            anchor="w",
            wraplength=550
        )

        label.pack(
            padx=16,
            pady=11
        )

        if record:
            self.history.append(("user", message))

        self.scroll_bottom()

    # ========================================================
    # BOT MESSAGE
    # ========================================================

    def add_bot_message(self, message, record=True):

        row = ctk.CTkFrame(
            self.chat_scroll,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            padx=25,
            pady=(8, 12)
        )

        # Avatar
        avatar = ctk.CTkLabel(
            row,
            text="✦",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=self.colors["avatar_bg"],
            text_color=self.colors["avatar_text"],
            font=("Segoe UI", 18, "bold")
        )

        avatar.pack(
            side="left",
            anchor="n",
            padx=(0, 10)
        )

        # Message content
        content = ctk.CTkFrame(
            row,
            fg_color="transparent"
        )

        content.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 100)
        )

        name = ctk.CTkLabel(
            content,
            text="Gemini",
            font=("Segoe UI", 11, "bold"),
            text_color=self.colors["accent"]
        )

        name.pack(
            anchor="w",
            pady=(0, 4)
        )

        self.render_markdown(
            content,
            message
        )

        if record:
            self.history.append(("bot", message))

        self.scroll_bottom()

    # ========================================================
    # MARKDOWN RENDERER
    # ========================================================

    def render_markdown(self, parent, message):

        lines = message.splitlines()

        in_code = False
        code_lines = []

        for line in lines:

            # ------------------------------------------------
            # Code block
            # ------------------------------------------------

            if line.strip().startswith("```"):

                if not in_code:

                    in_code = True
                    code_lines = []

                else:

                    in_code = False

                    self.create_code_block(
                        parent,
                        "\n".join(code_lines)
                    )

                continue

            if in_code:

                code_lines.append(line)

                continue

            # ------------------------------------------------
            # Empty line
            # ------------------------------------------------

            if not line.strip():

                spacer = ctk.CTkFrame(
                    parent,
                    height=7,
                    fg_color="transparent"
                )

                spacer.pack(
                    fill="x"
                )

                continue

            # ------------------------------------------------
            # Headings
            # ------------------------------------------------

            if line.startswith("### "):

                self.create_text_line(
                    parent,
                    line[4:],
                    font=("Segoe UI", 15, "bold")
                )

                continue

            if line.startswith("## "):

                self.create_text_line(
                    parent,
                    line[3:],
                    font=("Segoe UI", 17, "bold")
                )

                continue

            if line.startswith("# "):

                self.create_text_line(
                    parent,
                    line[2:],
                    font=("Segoe UI", 20, "bold")
                )

                continue

            # ------------------------------------------------
            # Horizontal rule
            # ------------------------------------------------

            if re.match(r"^\s*([-*_])\1{2,}\s*$", line):

                rule = ctk.CTkFrame(
                    parent,
                    height=1,
                    fg_color=self.colors["border"]
                )

                rule.pack(
                    fill="x",
                    pady=8
                )

                continue

            # ------------------------------------------------
            # Bullet
            # ------------------------------------------------

            bullet = re.match(
                r"^\s*[-*]\s+(.*)",
                line
            )

            if bullet:

                self.create_rich_line(
                    parent,
                    "• " + bullet.group(1)
                )

                continue

            # ------------------------------------------------
            # Numbered list
            # ------------------------------------------------

            numbered = re.match(
                r"^\s*(\d+)\.\s+(.*)",
                line
            )

            if numbered:

                self.create_rich_line(
                    parent,
                    f"{numbered.group(1)}. "
                    f"{numbered.group(2)}"
                )

                continue

            # ------------------------------------------------
            # Normal text
            # ------------------------------------------------

            self.create_rich_line(
                parent,
                line
            )

    # ========================================================
    # SIMPLE TEXT LINE
    # ========================================================

    def create_text_line(
        self,
        parent,
        text,
        font=("Segoe UI", 14, "bold"),
        color=None
    ):

        if color is None:
            color = self.colors["text"]

        label = ctk.CTkLabel(
            parent,
            text=text,
            font=font,
            text_color=color,
            justify="left",
            anchor="w"
        )

        label.pack(
            fill="x",
            pady=(5, 5)
        )

    # ========================================================
    # RICH TEXT LINE
    # ========================================================

    def create_rich_line(
        self,
        parent,
        text
    ):

        box = tk.Text(
            parent,
            wrap="word",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=("Segoe UI", 14),
            bd=0,
            highlightthickness=0,
            padx=0,
            pady=0,
            spacing3=2,
            cursor="arrow",
            height=1
        )

        box.tag_configure(
            "bold",
            font=("Segoe UI", 14, "bold")
        )

        box.tag_configure(
            "italic",
            font=("Segoe UI", 14, "italic")
        )

        box.tag_configure(
            "code",
            font=("Consolas", 13),
            background=self.colors["inline_code_bg"],
            foreground=self.colors["inline_code_text"]
        )

        # Split Markdown
        parts = re.split(
            r"(\*\*.*?\*\*|__.*?__|\*.*?\*|_.*?_|`.*?`)",
            text
        )

        for part in parts:

            if not part:
                continue

            # Bold
            if part.startswith("**") and part.endswith("**"):

                box.insert("end", part[2:-2], "bold")

            # Bold using __
            elif part.startswith("__") and part.endswith("__"):

                box.insert("end", part[2:-2], "bold")

            # Italic
            elif part.startswith("*") and part.endswith("*"):

                box.insert("end", part[1:-1], "italic")

            # Italic using _
            elif part.startswith("_") and part.endswith("_"):

                box.insert("end", part[1:-1], "italic")

            # Inline code
            elif part.startswith("`") and part.endswith("`"):

                box.insert("end", part[1:-1], "code")

            else:

                box.insert("end", part)

        box.configure(state="disabled")

        box.pack(
            fill="x",
            pady=1
        )

        box.update_idletasks()

        line_count = box.count("1.0", "end", "displaylines")

        if isinstance(line_count, tuple):
            line_count = line_count[0]

        box.configure(height=max(int(line_count), 1))

    # ========================================================
    # CODE BLOCK
    # ========================================================

    def create_code_block(
        self,
        parent,
        code
    ):

        container = ctk.CTkFrame(
            parent,
            fg_color=self.colors["codeblock_bg"],
            corner_radius=10,
            border_width=1,
            border_color=self.colors["codeblock_border"]
        )

        container.pack(
            fill="x",
            pady=(6, 10)
        )

        # Code header
        header = ctk.CTkFrame(
            container,
            height=30,
            fg_color=self.colors["codeblock_header"],
            corner_radius=0
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        code_label = ctk.CTkLabel(
            header,
            text="Code",
            font=("Segoe UI", 10),
            text_color=self.colors["codeblock_label"]
        )

        code_label.pack(
            side="left",
            padx=10
        )

        # Code text
        code_text = ctk.CTkLabel(
            container,
            text=code,
            font=("Consolas", 12),
            text_color=self.colors["codeblock_text"],
            justify="left",
            anchor="nw",
            wraplength=700
        )

        code_text.pack(
            fill="x",
            padx=14,
            pady=12
        )

    # ========================================================
    # THINKING ANIMATION
    # ========================================================

    def show_thinking(self):

        self.thinking = True
        self.thinking_step = 0

        self.thinking_row = ctk.CTkFrame(
            self.chat_scroll,
            fg_color="transparent"
        )

        self.thinking_row.pack(
            fill="x",
            padx=25,
            pady=8
        )

        avatar = ctk.CTkLabel(
            self.thinking_row,
            text="✦",
            width=36,
            height=36,
            corner_radius=18,
            fg_color=self.colors["avatar_bg"],
            text_color=self.colors["avatar_text"],
            font=("Segoe UI", 18, "bold")
        )

        avatar.pack(
            side="left",
            padx=(0, 10)
        )

        bubble = ctk.CTkFrame(
            self.thinking_row,
            fg_color=self.colors["bot_bubble"],
            corner_radius=14
        )

        bubble.pack(
            side="left"
        )

        self.thinking_label = ctk.CTkLabel(
            bubble,
            text="●  ●  ●",
            font=("Segoe UI", 11, "bold"),
            text_color=self.colors["thinking_dots"]
        )

        self.thinking_label.pack(
            padx=14,
            pady=10
        )

        self.animate_thinking()

        self.scroll_bottom()

    def animate_thinking(self):

        if not self.thinking:
            return

        states = [
            "●  ○  ○",
            "○  ●  ○",
            "○  ○  ●",
            "○  ●  ○"
        ]

        self.thinking_label.configure(
            text=states[
                self.thinking_step % len(states)
            ]
        )

        self.thinking_step += 1

        self.after(
            300,
            self.animate_thinking
        )

    def hide_thinking(self):

        self.thinking = False

        if hasattr(self, "thinking_row"):

            self.thinking_row.destroy()

    # ========================================================
    # SEND MESSAGE
    # ========================================================

    def send_message(self, event=None):

        message = self.message_entry.get().strip()

        if not message:
            return

        self.message_entry.delete(
            0,
            "end"
        )

        self.add_user_message(
            message
        )

        self.send_button.configure(
            state="disabled"
        )

        self.message_entry.configure(
            state="disabled"
        )

        self.show_thinking()

        thread = threading.Thread(
            target=self.get_response,
            args=(message,),
            daemon=True
        )

        thread.start()

    # ========================================================
    # GEMINI RESPONSE
    # ========================================================

    def get_response(self, message):

        try:

            response = chat.send_message(
                message
            )

            reply = response.text

            self.after(
                0,
                self.show_response,
                reply
            )

        except Exception as error:

            self.after(
                0,
                self.show_response,
                f"Sorry, something went wrong.\n\n{error}"
            )

    # ========================================================
    # SHOW RESPONSE
    # ========================================================

    def show_response(self, response):

        self.hide_thinking()

        self.add_bot_message(
            response
        )

        self.send_button.configure(
            state="normal"
        )

        self.message_entry.configure(
            state="normal"
        )

        self.message_entry.focus()

    # ========================================================
    # NEW CHAT
    # ========================================================

    def new_chat(self):

        global chat

        chat = client.chats.create(
            model=MODEL_NAME
        )

        self.history = []

        for widget in self.chat_scroll.winfo_children():

            widget.destroy()

        self.add_bot_message(
            "New conversation started. How can I help?"
        )

    # ========================================================
    # THEME TOGGLE
    # ========================================================

    def toggle_theme(self):

        self.theme_name = (
            "dark" if self.theme_name == "light" else "light"
        )

        self.colors = THEMES[self.theme_name]

        ctk.set_appearance_mode(self.theme_name)

        self.configure(
            fg_color=self.colors["bg"]
        )

        self.header.configure(
            fg_color=self.colors["header"]
        )

        self.logo_label.configure(
            text_color=self.colors["accent"]
        )

        self.title_label.configure(
            text_color=self.colors["text"]
        )

        self.status_label.configure(
            text_color=self.colors["status_online"]
        )

        self.theme_toggle_btn.configure(
            text=self.colors["toggle_icon"],
            fg_color=self.colors["new_chat_bg"],
            hover_color=self.colors["new_chat_hover"],
            text_color=self.colors["text"]
        )

        self.new_chat_btn.configure(
            fg_color=self.colors["new_chat_bg"],
            hover_color=self.colors["new_chat_hover"],
            text_color=self.colors["text"]
        )

        self.chat_scroll.configure(
            fg_color=self.colors["bg"]
        )

        self.input_container.configure(
            fg_color=self.colors["input"]
        )

        self.input_wrapper.configure(
            fg_color=self.colors["input_wrapper"],
            border_color=self.colors["border"]
        )

        self.message_entry.configure(
            text_color=self.colors["text"],
            placeholder_text_color=self.colors["placeholder"]
        )

        self.send_button.configure(
            fg_color=self.colors["send_bg"],
            hover_color=self.colors["send_hover"]
        )

        history = self.history
        self.history = []

        for widget in self.chat_scroll.winfo_children():

            widget.destroy()

        for role, message in history:

            if role == "user":
                self.add_user_message(message)
            else:
                self.add_bot_message(message)

    # ========================================================
    # SCROLL TO BOTTOM
    # ========================================================

    def scroll_bottom(self):

        self.after(
            50,
            lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0)
        )


# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":

    app = GeminiChatbot()

    app.mainloop()
