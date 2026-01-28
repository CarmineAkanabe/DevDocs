import customtkinter as ctk
from services.markdown_parser import MarkdownParser
from services.file_manager import FileManager
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import RawTokenFormatter
import re
import os


class ReaderView(ctk.CTkFrame):
    """Document reader view with markdown rendering."""

    def __init__(self, parent, db):
        """Initialize reader view."""
        super().__init__(parent, fg_color="#0d1117")

        self.db = db
        self.parser = MarkdownParser()
        self.file_manager = FileManager()
        self.current_doc_id = None

        # Configure grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Breadcrumb
        self.breadcrumb_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 11),
            text_color="#8b949e"
        )
        self.breadcrumb_label.grid(row=0, column=0, sticky="w", padx=40, pady=(28, 0))

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 32, "bold"),
            text_color="#58a6ff"
        )
        self.title_label.grid(row=1, column=0, sticky="w", padx=40, pady=(12, 28))

        # Content scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=40, pady=(0, 28))
        self.scroll_frame.grid_columnconfigure(0, weight=1)

    def clear(self):
        """Clear reader view."""
        self.breadcrumb_label.configure(text="")
        self.title_label.configure(text="")
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.current_doc_id = None

    def load_manual(self, file_path: str):
        """Load and render the user manual."""
        try:
            self.current_doc_id = None
            content = self.file_manager.read_file(file_path)
            # If parser fails or content isn't markdown-like, render as plain text
            try:
                parsed = self.parser.parse(content)
            except Exception:
                parsed = None

            # Set breadcrumb
            self.breadcrumb_label.configure(text="Help / UserManual", text_color="#666666")

            # Set title
            title = parsed['title'] if parsed and parsed.get('title') else 'User Manual'
            self.title_label.configure(text=title)

            # Clear content
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            # Render markdown or plain text
            if parsed:
                self._render_markdown(content)
            else:
                self._render_plain_text(content)

        except Exception as e:
            error_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"Error loading manual: {str(e)}",
                text_color="#ff4757",
                font=("Segoe UI", 12)
            )
            error_label.pack(pady=20)

    def load_document(self, doc_id: int, file_path: str, relative_path: str):
        """Load and render a document."""
        try:
            self.current_doc_id = doc_id
            content = self.file_manager.read_file(file_path)
            # Try parse; fall back to plain text when parsing fails or content lacks markdown markers
            parsed = None
            try:
                parsed = self.parser.parse(content)
            except Exception:
                parsed = None

            # Set breadcrumb
            breadcrumb = " > ".join(relative_path.replace("\\", "/").split("/"))
            self.breadcrumb_label.configure(text=breadcrumb, text_color="#666666")

            # Set title
            title = parsed['title'] if parsed and parsed.get('title') else os.path.basename(file_path)
            self.title_label.configure(text=title)

            # Clear content
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            # Render markdown or plain text
            if parsed:
                self._render_markdown(content)
            else:
                self._render_plain_text(content)

        except Exception as e:
            error_label = ctk.CTkLabel(
                self.scroll_frame,
                text=f"Error loading document: {str(e)}",
                text_color="#ff4757",
                font=("Segoe UI", 12)
            )
            error_label.pack(pady=20)

    def _render_markdown(self, content: str):
        """Render markdown content as styled widgets."""
        lines = content.split('\n')
        i = 0

        while i < len(lines):
            line = lines[i]

            # Code block
            if line.strip().startswith('```'):
                code_lines = []
                language = line.strip()[3:] or 'text'
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                i += 1  # Skip closing ```

                self._render_code_block('\n'.join(code_lines), language)
                continue

            # Headings
            if line.startswith('# '):
                text = line[2:].strip()
                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=text,
                    font=("Segoe UI", 28, "bold"),
                    text_color="#58a6ff",
                    wraplength=900
                )
                label.pack(anchor="w", pady=(36, 18))
                i += 1
                continue

            if line.startswith('## '):
                text = line[3:].strip()
                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=text,
                    font=("Segoe UI", 24, "bold"),
                    text_color="#79c0ff",
                    wraplength=900
                )
                label.pack(anchor="w", pady=(28, 14))
                i += 1
                continue

            if line.startswith('### '):
                text = line[4:].strip()
                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=text,
                    font=("Segoe UI", 20, "bold"),
                    text_color="#a5d6ff",
                    wraplength=900
                )
                label.pack(anchor="w", pady=(24, 12))
                i += 1
                continue

            # Bullet list
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                bullet_text = line.strip()[2:].strip()
                bullet_label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=f"• {bullet_text}",
                    font=("Segoe UI", 14),
                    text_color="#c9d1d9",
                    wraplength=850,
                    justify="left"
                )
                bullet_label.pack(anchor="w", pady=5, padx=(28, 0))
                i += 1
                continue

            # Paragraph
            if line.strip() and not line.startswith('#') and not line.strip().startswith('```'):
                para_label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=line.strip(),
                    font=("Segoe UI", 14),
                    text_color="#c9d1d9",
                    wraplength=900,
                    justify="left"
                )
                para_label.pack(anchor="w", pady=(0, 14))

            i += 1

    def _render_plain_text(self, content: str):
        """Render a plain text document inside the reader scroll frame."""
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        from tkinter import Text
        frame = ctk.CTkFrame(self.scroll_frame, fg_color="#161b22", corner_radius=10, border_width=1, border_color="#30363d")
        frame.pack(fill="both", expand=True, pady=16)

        text_widget = Text(frame, wrap="word", font=("Consolas", 12), bg="#161b22", fg="#c9d1d9", bd=0)
        text_widget.pack(fill="both", expand=True, padx=16, pady=16)
        text_widget.insert("1.0", content)
        text_widget.config(state="disabled")

    def load_readme(self, file_path: str):
        """Load README or ABOUT file and render (alias for manual)."""
        self.load_manual(file_path)

    def _render_code_block(self, code: str, language: str):
        """Render code block with syntax highlighting using Pygments."""
        # Code block frame
        block_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#161b22", corner_radius=10, border_width=1, border_color="#30363d")
        block_frame.pack(fill="both", expand=False, pady=20, padx=0)

        # Header with language and copy button
        header_frame = ctk.CTkFrame(block_frame, fg_color="#0d1117", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)

        lang_label = ctk.CTkLabel(
            header_frame,
            text=f"📋 {language.upper()}",
            font=("Segoe UI", 11, "bold"),
            text_color="#238636"
        )
        lang_label.pack(anchor="w", padx=16, pady=10)

        # Code content with text widget for better display
        from tkinter import Text
        code_frame = ctk.CTkFrame(block_frame, fg_color="#161b22")
        code_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Create a text widget for code display
        code_text = Text(
            code_frame,
            font=("Consolas", 12),
            bg="#161b22",
            fg="#c9d1d9",
            relief="flat",
            bd=0,
            padx=16,
            pady=16,
            wrap="word",
            height=min(15, code.count('\n') + 2)
        )
        code_text.pack(fill="both", expand=True, padx=0, pady=0)
        code_text.insert("1.0", code)
        code_text.config(state="disabled")

        # Apply syntax highlighting if possible
        try:
            lexer = get_lexer_by_name(language)
        except:
            lexer = guess_lexer(code)

        # Simple color map for keywords (basic syntax highlighting)
        keywords = {
            'def', 'class', 'return', 'import', 'from', 'if', 'else', 'elif',
            'for', 'while', 'try', 'except', 'finally', 'with', 'as', 'pass',
            'break', 'continue', 'yield', 'lambda', 'True', 'False', 'None'
        }

        code_text.tag_config("keyword", foreground="#ff79c6")
        code_text.tag_config("string", foreground="#f1fa8c")
        code_text.tag_config("comment", foreground="#6272a4")
        code_text.tag_config("number", foreground="#bd93f9")

        # Apply highlighting using Pygments tokens
        try:
            tokens = list(lexer.get_tokens(code))
            offset = 0
            for token_type, value in tokens:
                token_str = str(token_type)
                if 'Keyword' in token_str:
                    tag = 'keyword'
                elif 'String' in token_str:
                    tag = 'string'
                elif 'Comment' in token_str:
                    tag = 'comment'
                elif 'Number' in token_str:
                    tag = 'number'
                else:
                    tag = None
                
                if tag and value:
                    # Calculate text position in Tk format (line.column)
                    lines_before = code[:offset].count('\n')
                    col = offset - code[:offset].rfind('\n') - 1
                    start_pos = f"{lines_before + 1}.{col}"
                    end_pos = f"{lines_before + 1}.{col + len(value)}"
                    code_text.tag_add(tag, start_pos, end_pos)
                
                offset += len(value)
        except Exception as e:
            pass  # Syntax highlighting failed, but code still displays
