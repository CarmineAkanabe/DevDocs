import customtkinter as ctk
from services.markdown_parser import MarkdownParser
from services.file_manager import FileManager
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import RawTokenFormatter
import re


class ReaderView(ctk.CTkFrame):
    """Document reader view with markdown rendering."""

    def __init__(self, parent, db):
        """Initialize reader view."""
        super().__init__(parent, fg_color="#0f0f23")

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
            text_color="#666666"
        )
        self.breadcrumb_label.grid(row=0, column=0, sticky="w", padx=32, pady=(24, 0))

        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 28, "bold"),
            text_color="#ffffff"
        )
        self.title_label.grid(row=1, column=0, sticky="w", padx=32, pady=(8, 24))

        # Content scrollable frame
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=2, column=0, sticky="nsew", padx=32, pady=(0, 24))
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
            parsed = self.parser.parse(content)

            # Set breadcrumb
            self.breadcrumb_label.configure(text="Help / UserManual", text_color="#666666")

            # Set title
            title = parsed['title']
            self.title_label.configure(text=title)

            # Clear content
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            # Render markdown
            self._render_markdown(content)

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
            parsed = self.parser.parse(content)

            # Set breadcrumb
            breadcrumb = " > ".join(relative_path.replace("\\", "/").split("/"))
            self.breadcrumb_label.configure(text=breadcrumb, text_color="#666666")

            # Set title
            title = parsed['title']
            self.title_label.configure(text=title)

            # Clear content
            for widget in self.scroll_frame.winfo_children():
                widget.destroy()

            # Render markdown
            self._render_markdown(content)

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
                    font=("Segoe UI", 26, "bold"),
                    text_color="#ffffff",
                    wraplength=800
                )
                label.pack(anchor="w", pady=(32, 16))
                i += 1
                continue

            if line.startswith('## '):
                text = line[3:].strip()
                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=text,
                    font=("Segoe UI", 22, "bold"),
                    text_color="#e0e0e0",
                    wraplength=800
                )
                label.pack(anchor="w", pady=(24, 12))
                i += 1
                continue

            if line.startswith('### '):
                text = line[4:].strip()
                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=text,
                    font=("Segoe UI", 18, "bold"),
                    text_color="#cccccc",
                    wraplength=800
                )
                label.pack(anchor="w", pady=(20, 10))
                i += 1
                continue

            # Bullet list
            if line.strip().startswith('- ') or line.strip().startswith('* '):
                bullet_text = line.strip()[2:].strip()
                bullet_label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=f"\u2022 {bullet_text}",
                    font=("Segoe UI", 14),
                    text_color="#b0b0b0",
                    wraplength=750,
                    justify="left"
                )
                bullet_label.pack(anchor="w", pady=4, padx=(24, 0))
                i += 1
                continue

            # Paragraph
            if line.strip() and not line.startswith('#') and not line.strip().startswith('```'):
                para_label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=line.strip(),
                    font=("Segoe UI", 14),
                    text_color="#b0b0b0",
                    wraplength=800,
                    justify="left"
                )
                para_label.pack(anchor="w", pady=(0, 12))

            i += 1

    def _render_code_block(self, code: str, language: str):
        """Render code block with syntax highlighting using Pygments."""
        # Code block frame
        block_frame = ctk.CTkFrame(self.scroll_frame, fg_color="#1a1a2e", corner_radius=8, border_width=1, border_color="#2d2d44")
        block_frame.pack(fill="both", expand=False, pady=16, padx=0)

        # Header with language and copy button
        header_frame = ctk.CTkFrame(block_frame, fg_color="#0a0a1a", corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)

        lang_label = ctk.CTkLabel(
            header_frame,
            text=f"📋 {language.upper()}",
            font=("Segoe UI", 10, "bold"),
            text_color="#22aa44"
        )
        lang_label.pack(anchor="w", padx=12, pady=8)

        # Code content with text widget for better display
        from tkinter import Text
        code_frame = ctk.CTkFrame(block_frame, fg_color="#1a1a2e")
        code_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Create a text widget for code display
        code_text = Text(
            code_frame,
            font=("Consolas", 12),
            bg="#1a1a2e",
            fg="#e0e0e0",
            relief="flat",
            bd=0,
            padx=12,
            pady=12,
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
