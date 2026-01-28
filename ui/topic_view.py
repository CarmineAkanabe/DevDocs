import customtkinter as ctk
from datetime import datetime


class TopicView(ctk.CTkFrame):
    """Sidebar topic selection view."""

    def __init__(self, parent, db, on_topic_selected):
        """Initialize topic view."""
        super().__init__(parent, width=220, fg_color="#0d1117", border_width=2, border_color="#30363d")
        self.grid_propagate(False)

        self.db = db
        self.on_topic_selected = on_topic_selected
        self.current_topic_id = None
        self.topic_buttons = {}

        # Configure grid
        self.grid_rowconfigure(1, weight=1)

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="📚 Topics",
            font=("Segoe UI", 14, "bold"),
            text_color="#58a6ff"
        )
        title_label.grid(row=0, column=0, sticky="ew", padx=16, pady=(20, 16))

        # Scrollable frame for topics
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            label_text=""
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Info section
        self.info_frame = ctk.CTkFrame(self, fg_color="#161b22", corner_radius=8, height=90)
        self.info_frame.grid(row=2, column=0, sticky="ew", padx=12, pady=16)
        self.info_frame.grid_propagate(False)

        separator = ctk.CTkFrame(self.info_frame, height=2, fg_color="#30363d")
        separator.pack(fill="x", pady=(0, 12))

        self.info_label = ctk.CTkLabel(
            self.info_frame,
            text="No topic selected",
            font=("Segoe UI", 10),
            text_color="#8b949e",
            justify="left"
        )
        self.info_label.pack(anchor="w", padx=12, pady=8)

        self.refresh()

    def refresh(self):
        """Refresh topic list."""
        # Store current selection
        current_id = self.current_topic_id
        
        # Clear existing buttons safely using after_idle
        old_buttons = list(self.topic_buttons.values())
        self.topic_buttons.clear()
        
        def _destroy_old():
            for btn in old_buttons:
                try:
                    if btn.winfo_exists():
                        btn.destroy()
                except Exception:
                    pass
        
        self.after_idle(_destroy_old)

        # Get topics
        topics = self.db.get_all_topics()

        # Create buttons
        for topic in topics:
            self.add_topic_button(topic)
            
        # Restore selection
        if current_id:
            self.current_topic_id = current_id
            self.update_selection()
            self.update_info()

    def add_topic_button(self, topic):
        """Add a topic button."""
        topic_id = topic['id']
        topic_name = topic['name']

        btn = ctk.CTkButton(
            self.scroll_frame,
            text=f"📘 {topic_name}",
            font=("Segoe UI", 12),
            height=48,
            corner_radius=10,
            anchor="w",
            fg_color="#161b22",
            hover_color="#21262d",
            border_width=1,
            border_color="#30363d",
            command=lambda: self.select_topic(topic_id)
        )
        btn.pack(fill="x", pady=6, padx=10)
        self.topic_buttons[topic_id] = btn

    def select_topic(self, topic_id: int):
        """Select a topic."""
        self.current_topic_id = topic_id
        self.update_selection()
        self.update_info()
        self.on_topic_selected(topic_id)

    def update_selection(self):
        """Update button colors based on selection."""
        for topic_id, btn in self.topic_buttons.items():
            if topic_id == self.current_topic_id:
                btn.configure(fg_color="#238636", hover_color="#2ea043", text_color="#ffffff", border_color="#238636")
            else:
                btn.configure(fg_color="#161b22", hover_color="#21262d", text_color="#c9d1d9", border_color="#30363d")

    def update_info(self):
        """Update info section."""
        if self.current_topic_id is None:
            self.info_label.configure(text="No topic selected")
            return

        topic = self.db.get_topic(self.current_topic_id)
        doc_count = len(self.db.get_topic_documents(self.current_topic_id))
        unread_count = self.db.get_unread_count(self.current_topic_id)

        updated_at = topic['updated_at'][:10] if topic['updated_at'] else "Never"

        info_text = f"Documents: {doc_count}\nUnread: {unread_count}\nLast sync: {updated_at}"
        self.info_label.configure(text=info_text)
