import customtkinter as ctk


class DocumentView(ctk.CTkFrame):
    """File tree view for documents."""

    def __init__(self, parent, db, on_document_selected):
        """Initialize document view."""
        super().__init__(parent, width=300, fg_color="#0d1117", border_width=2, border_color="#30363d")
        self.grid_propagate(False)

        self.db = db
        self.on_document_selected = on_document_selected
        self.current_topic_id = None
        self.current_document_id = None

        # Configure grid
        self.grid_rowconfigure(1, weight=1)

        # Search entry
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.on_search_change)
        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="🔍 Search documents...",
            height=44,
            font=("Segoe UI", 13),
            textvariable=self.search_var,
            fg_color="#161b22",
            border_color="#30363d",
            border_width=2
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=12, pady=16)

        # Scrollable frame for documents
        self.scroll_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.document_buttons = {}
        self.folder_frames = {}

    def load_topic(self, topic_id: int):
        """Load documents for a topic."""
        self.current_topic_id = topic_id
        self.search_var.set("")
        self.refresh_current_topic()

    def refresh_current_topic(self):
        """Refresh current topic documents."""
        if self.current_topic_id is None:
            return

        # Clear existing buttons and other widgets safely on the main loop
        old_buttons = list(self.document_buttons.values())
        self.document_buttons.clear()

        old_children = list(self.scroll_frame.winfo_children())
        def _clear():
            for btn in old_buttons:
                try:
                    btn.destroy()
                except Exception:
                    pass
            for child in old_children:
                try:
                    child.destroy()
                except Exception:
                    pass

        self.after_idle(_clear)

        # Get documents
        documents = self.db.get_topic_documents(self.current_topic_id)

        # Group by folder structure and render
        self._build_tree(documents, "")

    def _build_tree(self, documents, search_filter=""):
        """Build file tree structure."""
        # Filter documents
        filtered = [d for d in documents if search_filter.lower() in d['relative_path'].lower()]

        if not filtered:
            no_docs = ctk.CTkLabel(
                self.scroll_frame,
                text="📭 No documents found",
                text_color="#8b949e",
                font=("Segoe UI", 12)
            )
            no_docs.pack(pady=20)
            return

        # Build tree structure where each folder is a dict and files are stored in '__files__'
        folder_structure = {}
        for doc in filtered:
            parts = doc['relative_path'].replace('\\', '/').split('/')
            current = folder_structure
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            # Append file to the current folder's file list
            files_list = current.setdefault('__files__', [])
            files_list.append(doc)

        # Render tree into the scroll frame
        self._render_tree(folder_structure, "", 0, parent_frame=self.scroll_frame)

    def _render_tree(self, tree, path_prefix, level, parent_frame=None):
        """Recursively render tree structure into parent_frame."""
        if parent_frame is None:
            parent_frame = self.scroll_frame

        # Render folders (collapsible)
        for key in sorted([k for k in tree.keys() if k != '__files__']):
            folder_path = path_prefix + key + "/"

            container = ctk.CTkFrame(parent_frame, fg_color="transparent")
            container.pack(fill="x", padx=(0, 0))

            folder_btn = ctk.CTkButton(
                container,
                text=f"📁 {key}",
                font=("Segoe UI", 11),
                height=32,
                fg_color="transparent",
                text_color="#8b949e",
                hover_color="#161b22",
                anchor="w",
                command=lambda p=folder_path, f=container, lvl=level: self._toggle_folder(p, f, lvl)
            )
            folder_btn.pack(fill="x", padx=(8 + level * 16, 8), pady=3)

            # Child frame that will hold folder contents
            child_frame = ctk.CTkFrame(container, fg_color="transparent")
            child_frame.pack(fill="x", padx=0, pady=0)
            self.folder_frames[folder_path] = child_frame

            # Render subtree into child_frame
            self._render_tree(tree[key], folder_path, level + 1, parent_frame=child_frame)

        # Render files in this folder
        files = tree.get('__files__', [])
        for doc in files:
            is_read = doc['is_read']
            doc_id = doc['id']
            filename = doc['title'] or doc['relative_path'].split('/')[-1].replace('.md', '').replace('_', ' ').title()

            btn = ctk.CTkButton(
                parent_frame,
                text=f"📄 {filename}" + ("" if is_read else " ●"),
                font=("Segoe UI", 11, "bold" if not is_read else "normal"),
                height=36,
                fg_color="transparent",
                hover_color="#161b22",
                text_color="#58a6ff" if not is_read else "#8b949e",
                anchor="w",
                command=lambda did=doc_id: self.select_document(did)
            )
            btn.pack(fill="x", padx=(8 + (level + 1) * 16, 8), pady=3)
            self.document_buttons[doc_id] = btn

    def _toggle_folder(self, folder_path: str, container: object, level: int):
        """Toggle visibility of a folder's child frame."""
        child_frame = self.folder_frames.get(folder_path)
        if not child_frame:
            return

        if child_frame.winfo_ismapped():
            try:
                child_frame.pack_forget()
            except Exception:
                pass
        else:
            try:
                child_frame.pack(fill="x", padx=0, pady=0)
            except Exception:
                pass

    def select_document(self, doc_id: int):
        """Select a document."""
        self.current_document_id = doc_id
        self.on_document_selected(doc_id)

    def on_search_change(self, *args):
        """Handle search input change."""
        search_text = self.search_var.get()

        # Clear and rebuild tree with filter safely
        for btn in list(self.document_buttons.values()):
            try:
                btn.destroy()
            except Exception:
                pass
        self.document_buttons.clear()

        # Clear all children safely
        for child in list(self.scroll_frame.winfo_children()):
            try:
                child.destroy()
            except Exception:
                pass

        if self.current_topic_id is not None:
            documents = self.db.get_topic_documents(self.current_topic_id)
            self._build_tree(documents, search_text)
