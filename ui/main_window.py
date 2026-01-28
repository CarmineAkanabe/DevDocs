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
        main_frame = ctk.CTkFrame(self, fg_color="#0f0f23")
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
        header = ctk.CTkFrame(self, height=50, fg_color="#0a0a1a", border_width=1, border_color="#2d2d44")
        header.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header.grid_propagate(False)

        # Left section
        left_frame = ctk.CTkFrame(header, fg_color="transparent")
        left_frame.pack(side="left", padx=16, pady=0)

        title_label = ctk.CTkLabel(
            left_frame,
            text="📘 DevDocs",
            font=("Segoe UI", 16, "bold"),
            text_color="#ffffff"
        )
        title_label.pack()

        # Right section
        right_frame = ctk.CTkFrame(header, fg_color="transparent")
        right_frame.pack(side="right", padx=16, pady=0)

        add_topic_btn = ctk.CTkButton(
            right_frame,
            text="+ Add Topic",
            font=("Segoe UI", 11),
            height=32,
            corner_radius=6,
            fg_color="#22aa44",
            hover_color="#1a8833",
            command=self.open_add_topic_dialog
        )
        add_topic_btn.pack(side="left", padx=8)

        manual_btn = ctk.CTkButton(
            right_frame,
            text="📖 Manual",
            font=("Segoe UI", 11),
            height=32,
            corner_radius=6,
            fg_color="transparent",
            border_width=1,
            border_color="#3d3d5c",
            command=self.show_manual
        )
        manual_btn.pack(side="left", padx=8)

        about_btn = ctk.CTkButton(
            right_frame,
            text="About",
            font=("Segoe UI", 11),
            height=32,
            corner_radius=6,
            fg_color="transparent",
            border_width=1,
            border_color="#3d3d5c",
            command=self.show_about
        )
        about_btn.pack(side="left", padx=8)

        sync_btn = ctk.CTkButton(
            right_frame,
            text="⟳ Sync",
            font=("Segoe UI", 11),
            height=32,
            corner_radius=6,
            fg_color="transparent",
            border_width=1,
            border_color="#3d3d5c",
            command=self.sync_current_topic
        )
        sync_btn.pack(side="left", padx=8)

    def _create_status_bar(self):
        """Create status bar."""
        self.status_frame = ctk.CTkFrame(self, height=28, fg_color="#0a0a1a", border_width=1, border_color="#2d2d44")
        self.status_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=0)
        self.status_frame.grid_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready",
            font=("Segoe UI", 11),
            text_color="#666666"
        )
        self.status_label.pack(side="left", padx=12, pady=0)

        # Center copyright (expand to take available space)
        self.copy_label = ctk.CTkLabel(
            self.status_frame,
            text="© 2026 DevDocs",
            font=("Segoe UI", 11, "bold"),
            text_color="#ffffff"
        )
        self.copy_label.pack(side="left", expand=True)

        # GitHub link (author) aligned right, larger and bold, pointer on hover
        self.github_label = ctk.CTkLabel(
            self.status_frame,
            text="CarmineAkanabe",
            font=("Segoe UI", 12, "bold"),
            text_color="#22aa44"
        )
        self.github_label.pack(side="right", padx=(0,12), pady=0)
        try:
            self.github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/CarmineAkanabe"))
            self.github_label.bind("<Enter>", lambda e: self.github_label.configure(cursor="hand2"))
            self.github_label.bind("<Leave>", lambda e: self.github_label.configure(cursor=""))
        except Exception:
            pass

        self.progress_bar = ctk.CTkProgressBar(self.status_frame, width=200)
        self.progress_bar.pack(side="right", padx=12, pady=6)
        self.progress_bar.pack_forget()

    def _init_default_topics(self):
        """Initialize default topics if database is empty."""
        topics = self.db.get_all_topics()
        if len(topics) == 0:
            default_topics = [
                ("JavaScript (MDN)", "https://github.com/mdn/content", "files/en-us"),
                ("Python", "https://github.com/python/cpython", "Doc"),
                ("SQL", "https://github.com/sqlite/sqlite", None)
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
            self.status_label.configure(text=f"Downloading...", text_color="#22aa44")
            self.progress_bar.pack(side="right", padx=12, pady=6)
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

            self.status_label.configure(text=f"Downloaded {len(files)} files", text_color="#2ed573")
            self.topic_view.refresh()
            self.document_view.refresh_current_topic()

        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}", text_color="#ff4757")
            messagebox.showerror("Download Error", str(e))
        finally:
            self.downloading = False
            self.progress_bar.pack_forget()
            self.after(2000, lambda: self.status_label.configure(text="Ready", text_color="#666666"))


class AddTopicDialog(ctk.CTkToplevel):
    """Dialog for adding new topic."""

    def __init__(self, parent, db, file_manager, docs_dir):
        """Initialize dialog."""
        super().__init__(parent)
        self.title("Add Documentation Topic")
        self.geometry("450x280")
        self.resizable(False, False)

        self.db = db
        self.file_manager = file_manager
        self.docs_dir = docs_dir

        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (450 // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (280 // 2)
        self.geometry(f"+{x}+{y}")

        # Make modal
        self.transient(parent)
        self.grab_set()

        self._create_ui()

    def _create_ui(self):
        """Create dialog UI."""
        # Main frame
        main_frame = ctk.CTkFrame(self, fg_color="#0f0f23")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Topic name
        ctk.CTkLabel(main_frame, text="Topic Name", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 4))
        self.name_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="e.g., React",
            height=36,
            font=("Segoe UI", 12)
        )
        self.name_entry.pack(fill="x", pady=(0, 12))

        # GitHub URL
        ctk.CTkLabel(main_frame, text="GitHub URL", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 4))
        self.url_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="https://github.com/user/repo",
            height=36,
            font=("Segoe UI", 12)
        )
        self.url_entry.pack(fill="x", pady=(0, 12))

        # Subfolder (optional)
        ctk.CTkLabel(main_frame, text="Subfolder (optional)", font=("Segoe UI", 12)).pack(anchor="w", pady=(0, 4))
        self.subfolder_entry = ctk.CTkEntry(
            main_frame,
            placeholder_text="docs/ (leave empty if not needed)",
            height=36,
            font=("Segoe UI", 12)
        )
        self.subfolder_entry.pack(fill="x", pady=(0, 24))

        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", pady=(0, 0))

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            font=("Segoe UI", 11),
            fg_color="transparent",
            border_width=1,
            border_color="#3d3d5c",
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=(8, 0))

        add_btn = ctk.CTkButton(
            button_frame,
            text="Add Topic",
            font=("Segoe UI", 11),
            command=self.add_topic
        )
        add_btn.pack(side="right", padx=(0, 8))

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
