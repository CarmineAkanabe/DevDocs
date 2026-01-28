# 📘 DevDocs - Offline Documentation Reader

<div align="center">

![DevDocs Banner](https://img.shields.io/badge/DevDocs-Offline%20Documentation%20Reader-58a6ff?style=for-the-badge&logo=markdown)

**Your personal offline documentation library for developers**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![customTkinter](https://img.shields.io/badge/customTkinter-5.2.2-1f6feb?style=flat-square)](https://github.com/TomSchimansky/CustomTkinter)
[![SQLite](https://img.shields.io/badge/SQLite-Built--in-003B57?style=flat-square&logo=sqlite)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-238636?style=flat-square)](LICENSE)

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Screenshots](#-screenshots)

</div>

---

## 🎯 What is DevDocs?

**DevDocs** is a powerful desktop application that allows developers to download, organize, and read technical documentation completely offline. Built with Python and customTkinter, it provides a beautiful, GitHub-inspired dark interface for browsing markdown documentation from any public GitHub repository.

### Why DevDocs?

- **📚 Centralized Documentation** - Keep all your favorite framework docs in one place
- **🔌 Work Offline** - Download once, access forever without internet
- **⚡ Lightning Fast** - No loading times, no ads, no distractions
- **🎨 Beautiful Interface** - Modern GitHub-inspired dark theme
- **🔍 Smart Search** - Find what you need instantly with real-time filtering
- **📊 Track Progress** - Mark documents as read and track your learning journey

### Perfect For:

- 👨‍💻 **Developers** who need quick offline access to documentation
- 🎓 **Students** learning new frameworks and technologies
- 👥 **Teams** who want consistent documentation across all members
- 🌍 **Remote Workers** in areas with limited internet connectivity
- 📖 **Technical Writers** who need to reference multiple docs

---

## ✨ Features

### 🔌 Offline-First Architecture
Download documentation once and access it forever without internet. Perfect for coding on planes, trains, or anywhere with spotty connectivity.

### 📥 GitHub Integration
Seamlessly download markdown documentation from any public GitHub repository. Supports:
- Multiple branches (main, master, develop, dev)
- Subfolder targeting (e.g., `/docs`, `/documentation`)
- Automatic markdown file extraction
- Fallback to README.md if no docs found

### 📖 Rich Markdown Rendering
Beautiful rendering of markdown content with:
- **Syntax-highlighted code blocks** using Pygments
- **Styled headings** with gradient blue colors
- **Formatted lists** and paragraphs
- **Responsive layout** that adapts to window size

### 💾 Persistent Storage
SQLite database tracks:
- All your documentation topics
- Downloaded documents and their locations
- Read/unread status for each document
- Last sync timestamps

### 🎨 Modern GitHub-Inspired UI
- **Dark theme** optimized for long reading sessions
- **Three-panel layout** for efficient navigation
- **Smooth animations** and hover effects
- **Responsive design** that scales beautifully

### 🔍 Smart Search & Organization
- **Real-time search** filters documents as you type
- **Hierarchical tree view** preserves folder structure
- **Unread indicators** help track your progress
- **Collapsible folders** for clean organization

### ➕ Extensible & Customizable
- **Add unlimited topics** from any GitHub repository
- **Custom subfolder paths** for precise documentation targeting
- **Resizable windows** and panels
- **Keyboard shortcuts** for power users

---

## 🚀 Installation

### System Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+) |
| **Python** | 3.10 or higher |
| **RAM** | 512 MB minimum (1 GB recommended) |
| **Disk Space** | 100 MB for app + space for downloaded docs |
| **Internet** | Required only for downloading documentation |

### Prerequisites

Before installing, ensure you have:

1. **Python 3.10+** installed - [Download from python.org](https://www.python.org/downloads/)
2. **pip** package manager (included with Python)
3. **Git** (optional, for cloning) - [Download from git-scm.com](https://git-scm.com/)

**Verify Python installation:**
```bash
python --version
# Should output: Python 3.10.x or higher
```

---

### 📦 Installation Steps

#### Step 1: Get the Project

**Option A: Clone with Git (Recommended)**
```bash
git clone https://github.com/CarmineAkanabe/DevDocs.git
cd DevDocs
```

**Option B: Download ZIP**
1. Download the ZIP file from [GitHub](https://github.com/CarmineAkanabe/DevDocs)
2. Extract to your desired location
3. Open terminal/command prompt in the extracted folder

#### Step 2: Create Virtual Environment

A virtual environment keeps project dependencies isolated from your system Python.

**Windows (Command Prompt):**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

✅ **Confirmation:** Your prompt should now show `(.venv)` prefix

#### Step 3: Install Dependencies

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install all required packages
pip install -r requirements.txt
```

**What gets installed:**
- `customtkinter` - Modern GUI framework
- `requests` - HTTP library for GitHub downloads
- `markdown` - Markdown parser
- `pygments` - Syntax highlighting for code blocks
- And other supporting libraries

#### Step 4: Run the Application

```bash
python app.py
```

🎉 **Success!** The DevDocs window should open with a beautiful splash screen, followed by the main interface.

---

## 🎯 Quick Start

### First Launch

When you first launch DevDocs, you'll see three pre-configured topics:
- **GitHub Docs** - Official GitHub documentation
- **Python Docs** - Python standard library documentation
- **React Docs** - React framework documentation

### Download Your First Documentation

1. **Select a topic** from the left sidebar (e.g., "Python Docs")
2. **Click the "⟳ Sync" button** in the top-right header
3. **Wait for download** - Progress bar shows download status
4. **Browse documents** - Expand folders in the middle panel
5. **Read documentation** - Click any document to view it

### Add a Custom Topic

1. **Click "✚ Add Topic"** button in the header
2. **Fill in the form:**
   - **Topic Name:** e.g., "Vue.js"
   - **GitHub URL:** e.g., `https://github.com/vuejs/docs`
   - **Subfolder:** e.g., `src` (optional - leave empty for root)
3. **Click "✓ ADD TOPIC"** button (or press Enter)
4. **Sync the new topic** to download its documentation

### Search Documents

1. **Select a topic** from the sidebar
2. **Type in the search bar** (🔍 Search documents...)
3. **Results filter in real-time** as you type
4. **Clear search** to see all documents again

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` | Submit Add Topic form |
| `Escape` | Clear search (when focused) |

---

## 📸 Screenshots

### Main Interface
Beautiful three-panel layout with topic sidebar, document tree, and markdown reader.

### Add Topic Dialog
Large, clear dialog with prominent buttons for adding new documentation sources.

### Markdown Rendering
Syntax-highlighted code blocks, styled headings, and formatted content.

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **GUI Framework** | customTkinter 5.2.2 | Modern, customizable desktop interface |
| **Database** | SQLite3 (built-in) | Local data persistence |
| **Markdown Parser** | Markdown 3.10.1 | Parse and render .md files |
| **Syntax Highlighting** | Pygments 2.19.2 | Colorize code blocks |
| **HTTP Client** | Requests 2.32.5 | Download from GitHub API |
| **Language** | Python 3.10+ | Core application logic |

---

## 📂 Project Structure

```
DevDocs/
├── app.py                      # Application entry point with splash screen
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── UserManual.md              # Comprehensive user guide
├── LICENSE                     # MIT License
│
├── database/
│   ├── __init__.py
│   └── db_manager.py          # SQLite database operations
│
├── services/
│   ├── __init__.py
│   ├── downloader.py          # GitHub repository downloader
│   ├── markdown_parser.py     # Markdown parsing and rendering
│   └── file_manager.py        # File system operations
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # Main application window
│   ├── topic_view.py          # Topic sidebar component
│   ├── document_view.py       # Document tree component
│   └── reader_view.py         # Markdown reader component
│
├── docs/                       # Downloaded documentation (auto-created)
│   ├── github_docs/
│   ├── python_docs/
│   └── react_docs/
│
└── devdocs.db                 # SQLite database (auto-created)
```

---

## 🔧 Troubleshooting

### Common Issues

**Issue: "python: command not found"**
- **Solution:** Install Python from [python.org](https://www.python.org/downloads/)
- On Windows, ensure "Add Python to PATH" is checked during installation
- On macOS/Linux, use `python3` instead of `python`

**Issue: "ModuleNotFoundError: No module named 'customtkinter'"**
- **Solution:** Activate virtual environment and reinstall dependencies:
  ```bash
  .venv\Scripts\activate  # Windows
  source .venv/bin/activate  # macOS/Linux
  pip install -r requirements.txt
  ```

**Issue: "Download failed: 404 error"**
- **Solution:** Verify the GitHub URL is correct and the repository is public
- Check that the subfolder path exists in the repository
- Try with a different branch (main/master/develop)

**Issue: No documents appear after download**
- **Solution:** Check that the repository contains markdown files
- Verify the subfolder path is correct
- Try leaving the subfolder empty to download from root

**Issue: Widget refresh errors in console**
- **Solution:** These are harmless and don't affect functionality
- The app handles widget cleanup safely in the background

---

## 💡 Tips & Best Practices

### Organizing Documentation

- **Use descriptive topic names** - e.g., "React v18 Docs" instead of just "React"
- **Group related topics** - Keep framework docs separate from language docs
- **Regular syncs** - Update documentation periodically to get latest changes

### Optimizing Performance

- **Download selectively** - Only sync topics you actively use
- **Use subfolders** - Target specific documentation folders to reduce download size
- **Clear old topics** - Remove unused topics to save disk space

### Keyboard Efficiency

- **Tab through fields** in the Add Topic dialog
- **Press Enter** to submit forms quickly
- **Use search** to find documents faster than scrolling

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Carmine Akanabe (Serge)**

- GitHub: [@CarmineAkanabe](https://github.com/CarmineAkanabe)
- Project: [DevDocs](https://github.com/CarmineAkanabe/DevDocs)

---

## 🙏 Acknowledgments

- **customTkinter** - For the beautiful modern GUI framework
- **Pygments** - For excellent syntax highlighting
- **GitHub** - For hosting open-source documentation
- **Python Community** - For amazing tools and libraries

---

## 📞 Support

If you encounter any issues or have questions:

1. Check the [UserManual.md](UserManual.md) for detailed usage instructions
2. Review the [Troubleshooting](#-troubleshooting) section above
3. Check existing issues on [GitHub](https://github.com/CarmineAkanabe/DevDocs/issues)
4. Create a new issue with detailed information about your problem

---

<div align="center">

**Built with ❤️ for developers who love documentation**

⭐ Star this repo if you find it useful!

</div>
