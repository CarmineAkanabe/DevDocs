# DevDocs User Manual

## Overview

**DevDocs** is an offline documentation reader that allows you to download and read technical documentation locally without requiring an internet connection after the initial download.

---

## Getting Started

### Launching the Application

1. Activate your Python virtual environment:
   ```bash
   .venv/Scripts/activate
   ```

2. Run the application:
   ```bash
   python app.py
   ```

The main window will open with a dark theme interface divided into three sections: **Sidebar** (topics), **File Tree** (documents), and **Reader** (content).

---

## Main Interface

### Sidebar (Left Panel)

- **Topics List**: Shows all available documentation topics (Git, Python, SQL, and any custom topics you've added)
- **Topic Selection**: Click any topic to view its documents
- **Topic Information**: Displays document count, unread documents, and last sync date for the selected topic
- **Unread Badge**: A red dot (●) appears next to unread documents

### File Tree (Middle Panel)

- **Search Box**: Type to filter documents by name
- **Folder Structure**: Documents organized in collapsible folders
- **Document List**: Click any document to open and read it
- **Unread Indicators**: Bold text and (●) indicator for unread documents

### Reader (Right Panel)

- **Breadcrumb Navigation**: Shows the document path
- **Document Title**: Large heading at the top
- **Formatted Content**: Styled markdown with headings, paragraphs, lists, and code blocks
- **Syntax Highlighting**: Code examples are displayed with appropriate styling

---

## Managing Documentation Topics

### Viewing Default Topics

DevDocs comes with three default topics pre-configured:

| Topic | Source |
|-------|--------|
| 📘 **Git** | Git version control system documentation |
| 🐍 **Python** | Python programming language documentation |
| 🗄️ **SQL** | SQLite database documentation |

### Adding a Custom Topic

1. Click the **"+ Add Topic"** button in the header
2. Fill in the dialog:
   - **Topic Name**: A descriptive name (e.g., "React", "Docker")
   - **GitHub URL**: The public GitHub repository URL (e.g., `https://github.com/facebook/react`)
   - **Subfolder** (optional): If documentation is in a subfolder, specify it (e.g., `docs/`)
3. Click **"Add Topic"** to confirm

The topic will be added to your sidebar immediately.

---

## Downloading and Syncing Documentation

### Initial Download

1. Select a topic from the sidebar
2. Click the **"⟳ Sync"** button in the header
3. Monitor the progress bar at the bottom
4. Once complete, the status bar will show "Downloaded X files"

### Re-syncing (Updating)

- Select the topic and click **"⟳ Sync"** again to download the latest version
- Existing files will be replaced with the newest versions from the repository

### Status Indicators

- **"Ready"**: No download in progress
- **"Downloading..."**: A download is active (watch the progress bar)
- **"Downloaded X files"**: Successful completion

---

## Reading Documentation

### Opening a Document

1. Select a topic from the sidebar
2. Browse the file tree in the middle panel
3. Click any document (with the 📄 icon) to open it
4. The document will render in the reader panel on the right

### Expanding Folders

- Click any folder (with the 📁 icon) to toggle its visibility
- Subfolder contents will expand/collapse

### Searching Documents

1. Type in the **"Search documents..."** box in the file tree panel
2. Results filter in real-time
3. Clear the search to see all documents again

### Marking as Read

When you click a document to open it:
- The document is automatically marked as **read**
- The (●) indicator disappears
- The text color normalizes from bold to regular

---

## Using the Help Manual

This manual is always accessible via the **"📖 Manual"** button in the header. Click it anytime to reference these instructions while using the app.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Focus search in file tree |
| `Escape` | Clear search or close dialogs |

---

## Troubleshooting

### "No documents found" for a topic

**Problem**: After syncing, the file tree shows "No documents found"

**Solutions**:
- Some repositories store documentation in a subfolder (e.g., `docs/`, `Documentation/`, `Doc/`)
- Delete the topic and re-add it with the correct subfolder path
- Check that the GitHub URL is correct

### Download fails with 404 error

**Problem**: Syncing a topic fails

**Solutions**:
- Verify the GitHub URL is correct
- Ensure the repository is public
- Try a different branch (the app automatically tries `main` and `master`)
- Check your internet connection

### Documents show "Untitled"

**Problem**: Some documents display "Untitled" instead of a proper title

**Solutions**:
- The document may not have an H1 heading (`# Title`)
- The app uses the first H1 heading as the title; add one if missing
- Documents without H1 will use their filename as a fallback

### App crashes or shows errors

**Problem**: Terminal shows exceptions

**Solutions**:
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check that your Python version is 3.10 or higher: `python --version`
- Restart the app and try again

---

## Data Storage

### Where Files Are Stored

- Downloaded documentation is stored in the `docs/` folder in your project directory
- Each topic has its own subfolder:
  - `docs/git/`
  - `docs/python/`
  - `docs/sql/`
  - `docs/custom_topic_name/`

### Database

- `devdocs.db`: SQLite database storing topics, documents, and read status
- This database persists across sessions, so your reading history and custom topics are saved

### Offline Access

- After download, the app works **completely offline**
- No internet connection is needed to read documentation
- Syncing requires internet to fetch the latest files

---

## Tips & Best Practices

### Organizing Topics

- Keep topic names short and descriptive
- Group related documentation (e.g., "Web Development" for React, Vue, etc.)
- Use meaningful names that help you remember the content

### Efficient Reading

- Search before browsing if you know what you're looking for
- Expand folder structures gradually instead of expanding all at once
- Mark read documents as read to track your progress

### Managing Storage

- Downloaded documentation can take significant disk space (100MB+ per topic)
- Use the `docs/` folder for organization
- You can safely delete individual topic folders to free space (they'll re-download on next sync)

---

## Frequently Asked Questions

**Q: Can I edit downloaded documentation?**
A: No, edits are not supported. However, you can delete and re-download to get fresh copies.

**Q: Is authentication required?**
A: No. DevDocs only works with public repositories.

**Q: Can I sync multiple topics at once?**
A: Currently, syncing is one topic at a time. Select the topic and click Sync.

**Q: How large can documentation be?**
A: There's no hard limit, but very large repositories may take time to download.

**Q: Does the app use my internet after downloading?**
A: No. Once downloaded, all reading is completely offline.

---

## Support & Feedback

For issues, suggestions, or contributions, refer to the project repository.

**Version**: 1.0.0  
**Last Updated**: January 2026
