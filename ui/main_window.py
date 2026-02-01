import customtkinter as ctk
from tkinter import messagebox
import webbrowser
from datetime import datetime
from database.db_manager import DatabaseManager
from services.downloader import Downloader
from services.file_manager import FileManager
import threading
from typing import Optional


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self):
        """Initialize main window."""
        super().__init__()

        # Window configuration
        self.title("DevDocs - Offline Documentation Reader")
        self.geometry("1400x900")
        self.minsize(1200, 800)

        # Set appearance and theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize database
        self.db = DatabaseManager("devdocs.db")
        self.file_manager = FileManager()
        self.docs_dir = self.file_manager.ensure_docs_directory("docs")

        # State
        self.current_topic_id = None
        self.current_document_id = None
        self.downloading = False

        # Create UI
        self._create_ui()

        # Initialize with default topics if needed
        self._init_default_topics()

    def _create_ui(self):
        """Create UI layout."""
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Header
        self._create_header()

        # Main content area
        main_frame = ctk.CTkFrame(self, fg_color="#010409")
        main_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=0)
        main_frame.grid_columnconfigure(2, weight=1)

        # Sidebar
        from ui.topic_view import TopicView
        self.topic_view = TopicView(main_frame, self.db, self.on_topic_selected)
        self.topic_view.grid(row=0, column=0, sticky="nsew")

        # File tree
        from ui.document_view import DocumentView
        self.document_view = DocumentView(main_frame, self.db, self.on_document_selected)
        self.document_view.grid(row=0, column=1, sticky="nsew")

        # Reader
        from ui.reader_view import ReaderView
        self.reader_view = ReaderView(main_frame, self.db)
        self.reader_view.grid(row=0, column=2, sticky="nsew")

        # Status bar
        self._create_status_bar()

    def _create_header(self):
        """Create header bar."""
        header = ctk.CTkFrame(self, height=60, fg_color="#0d1117", border_width=2, border_color="#30363d")
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        # Left section
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=0)

        title_label = ctk.CTkLabel(
            left_frame,
            text="📘 DevDocs",
            font=("Segoe UI", 18, "bold"),
            text_color="#58a6ff"
        )
        title_label.pack()

        # Right section
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=0)

        add_topic_btn = ctk.CTkButton(
            right_frame,
            text="✚ Add Topic",
            font=("Segoe UI", 12, "bold"),
            height=36,
            corner_radius=8,
            fg_color="#238636",
            hover_color="#2ea043",
            command=self.open_add_topic_dialog
        )
        add_topic_btn.pack(side="left", padx=6)

        manual_btn = ctk.CTkButton(
            right_frame,
            text="📖 Manual",
            font=("Segoe UI", 12),
            height=36,
            corner_radius=8,
            fg_color="#21262d",
            hover_color="#30363d",
            border_width=1,
            border_color="#30363d",
            command=self.show_manual
        )
        manual_btn.pack(side="left", padx=6)

        about_btn = ctk.CTkButton(
            right_frame,
            text="ℹ About",
            font=("Segoe UI", 12),
            height=36,
            corner_radius=8,
            fg_color="#21262d",
            hover_color="#30363d",
            border_width=1,
            border_color="#30363d",
            command=self.show_about
        )
        about_btn.pack(side="left", padx=6)

        sync_btn = ctk.CTkButton(
            right_frame,
            text="⟳ Sync",
            font=("Segoe UI", 12, "bold"),
            height=36,
            corner_radius=8,
            fg_color="#1f6feb",
            hover_color="#388bfd",
            command=self.sync_current_topic
        )
        sync_btn.pack(side="left", padx=6)

    def _create_status_bar(self):
        """Create status bar."""
        self.status_frame = ctk.CTkFrame(self, height=32, fg_color="#0d1117", border_width=2, border_color="#30363d")
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.status_frame.grid_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=("Segoe UI", 11),
            text_color="#8b949e"
        )
        self.status_label.pack(side="left", padx=16, pady=0)

        # Center copyright (expand to take available space)
        self.copy_label = ctk.CTkLabel(
            self.status_frame,
            text="© 2026 DevDocs",
            font=("Segoe UI", 11, "bold"),
            text_color="#c9d1d9"
        )
        self.copy_label.pack(side="left", expand=True)

        # GitHub link (author) aligned right, larger and bold, pointer on hover
        self.github_label = ctk.CTkLabel(
            self.status_frame,
            text="CarmineAkanabe",
            font=("Segoe UI", 12, "bold"),
            text_color="#58a6ff"
        )
        self.github_label.pack(side="right", padx=(0,16), pady=0)
        try:
            self.github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/CarmineAkanabe"))
            self.github_label.bind("<Enter>", lambda e: self.github_label.configure(cursor="hand2"))
            self.github_label.bind("<Leave>", lambda e: self.github_label.configure(cursor=""))
        except Exception:
            pass

        self.progress_bar = ctk.CTkProgressBar(self.status_frame, width=200, progress_color="#238636")
        self.progress_bar.pack(side="right", padx=16, pady=6)
        self.progress_bar.pack_forget()

    def _init_default_topics(self):
        """Initialize default topics if database is empty."""
        topics = self.db.get_all_topics()
        if len(topics) == 0:
            default_topics = [
                ("Laravel Docs", "https://github.com/laravel/docs", None),
                ("Python Docs", "https://github.com/python/cpython", "Doc"),
                ("Vue.js Docs", "https://github.com/vuejs/docs", "src")
            ]

            for name, url, subfolder in default_topics:
                topic_dir = self.file_manager.get_topic_directory(self.docs_dir, name)
                self.db.add_topic(name, url, topic_dir, subfolder)

            self.topic_view.refresh()

    def on_topic_selected(self, topic_id: int):
        """Handle topic selection."""
        self.current_topic_id = topic_id
        self.current_document_id = None
        self.document_view.load_topic(topic_id)
        self.reader_view.clear()

    def on_document_selected(self, doc_id: int):
        """Handle document selection."""
        self.current_document_id = doc_id
        doc = self.db.get_document(doc_id)
        if doc:
            self.reader_view.load_document(doc_id, doc['file_path'], doc['relative_path'])
            self.db.mark_as_read(doc_id, 1)
            self.document_view.refresh_current_topic()

    def show_manual(self):
        """Display the user manual."""
        import os
        manual_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "UserManual.md")
        if os.path.exists(manual_path):
            self.reader_view.load_manual(manual_path)
        else:
            messagebox.showerror("Error", "UserManual.md not found")

    def show_about(self):
        """Display the README/About file."""
        import os
        readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'README.md')
        readme_path = os.path.normpath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "README.md"))
        if os.path.exists(readme_path):
            # reuse manual loader which expects a file path
            self.reader_view.load_manual(readme_path)
        else:
            messagebox.showerror("Error", "README.md not found")

    def open_add_topic_dialog(self):
        """Open dialog to add new topic."""
        dialog = AddTopicDialog(self, self.db, self.file_manager, self.docs_dir)
        self.wait_window(dialog)
        self.topic_view.refresh()

    def sync_current_topic(self):
        """Sync/download current topic."""
        if self.current_topic_id is None:
            messagebox.showinfo("Info", "Please select a topic first")
            return

        if self.downloading:
            messagebox.showinfo("Info", "Download already in progress")
            return

        # Run in thread to avoid blocking UI
        thread = threading.Thread(target=self._sync_topic_thread)
        thread.daemon = True
        thread.start()

    def _sync_topic_thread(self):
        """Background thread for syncing."""
        try:
            self.downloading = True
            self.status_label.configure(text=f"Downloading...", text_color="#238636")
            self.progress_bar.pack(side="right", padx=16, pady=6)
            self.progress_bar.set(0)

            if self.current_topic_id is None:
                return

            topic = self.db.get_topic(self.current_topic_id)
            if not topic:
                return

            # Download
            zip_bytes = Downloader.download_repo_zip(topic['github_url'])

            # Clear old documents
            self.db.clear_documents_for_topic(self.current_topic_id)

            # Extract
            files = Downloader.extract_markdown_files(zip_bytes, topic['local_path'], topic['subfolder'])

            # Register documents
            for file_info in files:
                title = file_info['relative_path'].split('/')[-1].replace('.md', '').replace('_', ' ').title()
                self.db.add_document(
                    self.current_topic_id,
                    title,
                    file_info['relative_path'].split('/')[-1],
                    file_info['local_path'],
                    file_info['relative_path']
                )

            self.db.update_topic_timestamp(self.current_topic_id)
            self.progress_bar.set(1)

            self.status_label.configure(text=f"✓ Downloaded {len(files)} files", text_color="#238636")
            self.topic_view.refresh()
            self.document_view.refresh_current_topic()

        except Exception as e:
            error_msg = str(e)
            self.status_label.configure(text=f"✗ Error: {error_msg}", text_color="#f85149")
            
            # Check if it's a 404 error
            if "404" in error_msg or "not found" in error_msg.lower() or "Could not download" in error_msg:
                messagebox.showerror(
                    "404 - Repository Not Found",
                    f"Failed to download documentation:\n\n{error_msg}\n\n"
                    "Possible causes:\n"
                    "• Repository URL is incorrect\n"
                    "• Repository doesn't exist or was moved\n"
                    "• Repository is private\n"
                    "• Branch doesn't exist (tried: main, master, develop, dev)\n\n"
                    "Please verify the GitHub URL and try again."
                )
            else:
                messagebox.showerror("Download Error", f"An error occurred:\n\n{error_msg}")
        finally:
            self.downloading = False
            self.progress_bar.pack_forget()
            self.after(2000, lambda: self.status_label.configure(text="Ready", text_color="#8b949e"))


class AddTopicDialog(ctk.CTkToplevel):
    """Dialog for adding new topic."""

    def __init__(self, parent, db, file_manager, docs_dir):
        """Initialize dialog."""
        super().__init__(parent)
        self.title("Add Documentation Topic")
        self.geometry("600x500")
        self.resizable(True, True)

        self.db = db
        self.file_manager = file_manager
        self.docs_dir = docs_dir

        # Set dark theme
        self.configure(fg_color="#0d1117")

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (600 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (500 // 2)
        self.geometry(f"+{x}+{y}")

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._create_ui()
        
        # Bind Enter key to submit
        self.bind('<Return>', lambda e: self.add_topic())

    def _create_ui(self):
        """Create dialog UI."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="#0d1117", border_width=2, border_color="#30363d", corner_radius=12)
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="✚ Add New Topic",
            font=("Segoe UI", 20, "bold"),
            text_color="#58a6ff"
        )
        title_label.pack(pady=(20, 30))

        # Topic name
        ctk.CTkLabel(main_frame, text="Topic Name", font=("Segoe UI", 13, "bold"), text_color="#c9d1d9").pack(anchor="w", padx=20, pady=(0, 8))
        self.name_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="e.g., React, Vue, Django",
            height=45,
            font=("Segoe UI", 13),
            fg_color="#161b22",
            border_color="#30363d",
            border_width=2
        )
        self.name_entry.pack(fill="x", padx=20, pady=(0, 20))

        # GitHub URL
        ctk.CTkLabel(main_frame, text="GitHub Repository URL", font=("Segoe UI", 13, "bold"), text_color="#c9d1d9").pack(anchor="w", padx=20, pady=(0, 8))
        self.url_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="https://github.com/username/repository",
            height=45,
            font=("Segoe UI", 13),
            fg_color="#161b22",
            border_color="#30363d",
            border_width=2
        )
        self.url_entry.pack(fill="x", padx=20, pady=(0, 20))

        # Subfolder (optional)
        ctk.CTkLabel(main_frame, text="Documentation Subfolder (Optional)", font=("Segoe UI", 13, "bold"), text_color="#c9d1d9").pack(anchor="w", padx=20, pady=(0, 8))
        self.subfolder_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="docs (leave empty for root)",
            height=45,
            font=("Segoe UI", 13),
            fg_color="#161b22",
            border_color="#30363d",
            border_width=2
        )
        self.subfolder_entry.pack(fill="x", padx=20, pady=(0, 30))

        # Buttons frame - NO pack_propagate(False) to allow natural sizing
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(20, 20))

        # Add button (left side, more prominent)
        add_btn = ctk.CTkButton(
            button_frame,
            text="✓ ADD TOPIC",
            font=("Segoe UI", 16, "bold"),
            height=60,
            width=250,
            corner_radius=12,
            fg_color="#238636",
            hover_color="#2ea043",
            command=self.add_topic
        )
        add_btn.pack(side="left", padx=(0, 15))

        # Cancel button (right side)
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="CANCEL",
            font=("Segoe UI", 16),
            height=60,
            width=180,
            corner_radius=12,
            fg_color="#21262d",
            hover_color="#30363d",
            border_width=2,
            border_color="#30363d",
            command=self.destroy
        )
        cancel_btn.pack(side="left")

    def add_topic(self):
        """Add the topic."""
        name = self.name_entry.get().strip()
        url = self.url_entry.get().strip()
        subfolder = self.subfolder_entry.get().strip() or None

        if not name or not url:
            messagebox.showwarning("Validation", "Please fill in topic name and GitHub URL")
            return

        if not url.startswith("https://github.com/"):
            messagebox.showerror("Validation", "GitHub URL must start with https://github.com/")
            return

        try:
            topic_dir = self.file_manager.get_topic_directory(self.docs_dir, name)
            self.db.add_topic(name, url, topic_dir, subfolder)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add topic: {str(e)}")
