# 📘 DevDocs

> **Offline-first documentation reader for developers** — Download, organize, and read technical documentation locally with a beautiful desktop interface.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)
![customTkinter](https://img.shields.io/badge/customTkinter-5.2.2-306998?style=flat-square)
![SQLite](https://img.shields.io/badge/SQLite-Built--in-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production-green?style=flat-square)

---

## ✨ Features

- 🔌 **Offline First** — Download once, read anywhere without internet
- 📥 **GitHub Integration** — Download documentation directly from public repositories
- 📖 **Rich Markdown Rendering** — Styled headings, lists, code blocks, and syntax highlighting
- 💾 **Persistent Storage** — SQLite database tracks topics, documents, and reading status
- 🎨 **Modern UI** — Clean dark-mode interface with green accents built with customTkinter
- ➕ **Extensible** — Add custom documentation topics dynamically
- 🔍 **Search & Organize** — Search documents and track read/unread status
- 📚 **Built-in Help** — Access the user manual directly from the app

---

## 🚀 Installation Guide for Teachers

This section provides complete step-by-step instructions to set up DevDocs on Windows, macOS, and Linux.

### System Requirements

| Component | Requirement |
|-----------|-------------|
| **Operating System** | Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+) |
| **Python** | 3.10 or higher |
| **RAM** | 256 MB minimum (512 MB recommended) |
| **Disk Space** | 100 MB for app + variable for downloaded docs |
| **Internet** | Required for downloading docs; optional for reading |

### Prerequisites

Before installing, ensure you have:

- **Python 3.10+** — [Download from python.org](https://www.python.org/downloads/)
- **pip** (comes with Python automatically)
- **Git** (optional, for cloning) — [Download from git-scm.com](https://git-scm.com/)

**Verify Python is installed:**
```bash
python --version
```

Output should show `Python 3.10.x` or higher.

---

## 💻 Step-by-Step Installation

### Step 1: Get the Project

#### Option A: Clone with Git (Recommended)
```bash
git clone https://github.com/CarmineAkanabe/DevDocs.git
cd DevDocs
```

#### Option B: Manual Download
1. Download as ZIP from GitHub
2. Extract to your desired location
3. Open terminal/command prompt in the folder

### Step 2: Create Virtual Environment

A virtual environment keeps project dependencies isolated from system Python.

#### Windows (Command Prompt):
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### macOS/Linux (Terminal):
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Confirmation**: Your prompt should now show `(.venv)` prefix.

### Step 3: Upgrade pip

Ensure pip is up-to-date:

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

**What gets installed:**
- **customtkinter** — Modern GUI framework
- **requests** — Download from GitHub
- **markdown** — Parse markdown files
- **pygments** — Syntax highlighting

**Verify installation:**
```bash
pip list
```

You should see all packages listed with versions.

### Step 5: Run the Application

```bash
python app.py
```

**Expected**: A window with title "DevDocs - Offline Documentation Reader" opens with three topics in the sidebar: GitHub Docs, Python, and SQL.

---

## 🎯 Quick Start (After Installation)

### First Launch

1. **Download documentation**:
   - Select "Python" from the sidebar
   - Click "⟳ Sync" button
   - Wait for download to complete (may take 1-2 minutes)

2. **Read documentation**:
   - Expand folders in the file tree
   - Click any document to open
   - Content renders in the right panel with syntax highlighting

3. **Access help**:
   - Click "📖 Manual" button in header
   - Browse complete user guide with screenshots

---

## 🔧 Troubleshooting Common Issues

### Issue: "python: command not found"

**Cause**: Python not installed or not in PATH

**Solution**:
- Download Python from [python.org](https://www.python.org/downloads/)
- **Windows**: Check "Add python.exe to PATH" during install
- **macOS**: Use `python3` instead of `python`, or install via Homebrew: `brew install python3`
- **Linux**: `sudo apt-get install python3`

### Issue: "ModuleNotFoundError: No module named 'customtkinter'"

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Activate venv:
.venv\Scripts\activate          # Windows
source .venv/bin/activate      # macOS/Linux

# Reinstall:
pip install -r requirements.txt
```

### Issue: "Permission denied" Error

**Solution**:
- **Windows**: Run Command Prompt as Administrator
- **macOS/Linux**: Use `sudo` if needed: `sudo python3 -m venv .venv`

### Issue: App doesn't start or crashes

**Solution**:
1. Verify Python 3.10+: `python --version`
2. Reinstall dependencies: `pip install --force-reinstall -r requirements.txt`
3. Check for error output in terminal window
4. Try on a fresh virtual environment (delete `.venv` and restart)

### Issue: "Download failed: 404 error"

**Cause**: Repository URL invalid or inaccessible

**Solution**:
- Check internet connection
- Verify GitHub URL is correct (must be public repository)
- Try with a different topic first
- Ensure repository contains markdown files in expected location

### Issue: No documents display after download

**Cause**: Repository subfolder incorrect or no markdown files

**Solution**:
- Check that documentation subfolder is correct (if specified)
- Some repos may not have markdown docs in accessible location
- Try with Python or GitHub Docs topics to verify setup

---

## 📂 Project Structure

```
DevDocs/
├── app.py                      # Application entry point
├── UserManual.md               # Built-in user manual
├── README.md                   # This file
├── requirements.txt            # Python dependencies
├── devdocs.db                  # SQLite database (auto-created)
│
├── database/
│   ├── __init__.py
│   └── db_manager.py           # SQLite operations
│
├── services/
│   ├── __init__.py
│   ├── downloader.py           # GitHub download logic
│   ├── markdown_parser.py      # Markdown parsing
│   └── file_manager.py         # File operations
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # Main window & header
│   ├── topic_view.py           # Topic sidebar
│   ├── document_view.py        # File tree
│   └── reader_view.py          # Markdown renderer
│
├── docs/                       # Downloaded docs (auto-created)
│   ├── github-docs/
│   ├── python/
│   └── sql/
│
└── assets/
    └── fonts/                  # Custom fonts (optional)
```

---

## 🛠️ Technology Stack

| Component | Library | Version | Purpose |
|-----------|---------|---------|---------|
| **GUI** | customTkinter | 5.2.2 | Modern desktop interface |
| **Database** | SQLite3 | Built-in | Local data storage |
| **Markdown** | Markdown | 3.10.1 | Parse .md files |
| **Highlighting** | Pygments | 2.19.2 | Code syntax colors |
| **Downloads** | Requests | 2.32.5 | GitHub API access |

All other dependencies use Python standard library (no additional packages needed beyond what's in requirements.txt).

---

## 📚 Default Documentation Topics

The app includes three pre-configured topics:

| Topic | Repository | Content |
|-------|-----------|---------|
| 📖 **GitHub Docs** | github.com/github/docs | GitHub platform documentation |
| 🐍 **Python** | github.com/python/cpython | Python standard library |
| 🗄️ **SQL** | github.com/sqlite/sqlite | SQLite database documentation |

### Adding Custom Topics

1. Click **"+ Add Topic"** button (green color, top left)
2. Enter topic name and GitHub repository URL
3. (Optional) Specify documentation subfolder (e.g., `docs/`, `Documentation/`)
4. Click **"Add Topic"** to save

**Example**: Add React documentation
- Name: `React`
- URL: `https://github.com/facebook/react`
- Subfolder: `docs`

---

## 💡 Usage Tips

### Download Documentation

1. Select a topic from sidebar
2. Click **"⟳ Sync"** button (arrow icon)
3. Monitor progress bar
4. Status bar shows "Downloaded X files" when complete
5. Documents appear in file tree (may be in expandable folders)

### Search Documents

1. Type in the search box in the file tree
2. Results filter in real-time as you type
3. Clear search box to see all documents again
4. Search is case-insensitive

### Mark as Read

- When you click a document, it's automatically marked as read
- Unread documents show a bullet (•) indicator
- Reading progress persists across sessions in database

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+F` | Focus search (when available) |
| `Escape` | Clear search |

---

## 💾 Data Storage & Privacy

### Local Storage

- **`docs/`** — All downloaded markdown files organized by topic
- **`devdocs.db`** — SQLite database with topics, documents, reading status
- **No cloud sync** — Everything stays on your computer
- **No telemetry** — No data sent anywhere
- **No tracking** — Completely private, offline-first design

### Offline Usage

- After initial download, app works **completely offline**
- All reading uses local files (no internet required)
- Syncing requires internet only to fetch updates
- **Perfect for classroom** — Download docs in advance, use offline in class with no internet needed

### Reset/Clear Data

To start fresh:
```bash
rm devdocs.db              # macOS/Linux
del devdocs.db             # Windows

rm -rf docs/               # macOS/Linux
rmdir /s docs              # Windows
```

Restart the app to reinitialize with defaults.

---

## ✅ Verification Checklist

After installation, verify:

- [ ] Python 3.10+ installed (`python --version`)
- [ ] Virtual environment created (`.venv` folder exists)
- [ ] Virtual environment activated (`(.venv)` in prompt)
- [ ] Dependencies installed (`pip list` shows all packages)
- [ ] App launches without errors (`python app.py`)
- [ ] Topics visible in sidebar (GitHub Docs, Python, SQL)
- [ ] Can download documentation (click "⟳ Sync")
- [ ] Can open and read documents in right panel
- [ ] Manual accessible from "📖 Manual" button
- [ ] Code blocks display with syntax highlighting
- [ ] Search filters documents in real-time

---

## 👥 For All Users

### Getting Started

1. **Install on your machine** — Follow the installation guide above
2. **Download documentation** — Select a topic and click "⟳ Sync" to download
3. **Read offline** — All documentation is available offline after download
4. **Share offline** — Copy the entire `DevDocs` folder to share with others offline

### Benefits of DevDocs

- ✅ Fast, offline access to documentation anytime
- ✅ No internet bandwidth required after initial download
- ✅ Consistent experience across all platforms
- ✅ Learn documentation navigation and organization
- ✅ Add custom topics for your favorite frameworks

### Use Cases

- Personal development and reference
- Team knowledge sharing and onboarding
- Classroom and educational environments
- Remote areas with limited connectivity
- Quick offline API reference during coding

---

## 📞 Getting Help

If problems occur:

1. **Check the terminal output** for error messages
2. **Review troubleshooting section** above
3. **Verify all prerequisites** are installed
4. **Try a clean reinstall** — delete `.venv/` and `devdocs.db`, start from Step 2
5. **Check the UserManual** — click "📖 Manual" inside app

---

## 📦 Dependencies Reference

All packages in `requirements.txt`:

```
certifi==2026.1.4          # SSL certificates
charset-normalizer==3.4.4  # Character encoding
customtkinter==5.2.2       # GUI framework
darkdetect==0.8.0          # Dark mode detection
idna==3.11                 # Domain names
Markdown==3.10.1           # Markdown parser
packaging==26.0            # Version parsing
Pygments==2.19.2           # Syntax highlighting
requests==2.32.5           # HTTP requests
urllib3==2.6.3             # URL handling
```

---

## 📄 License

This project is open source under the MIT License.

---

## 🎯 Support Resources

- **User Manual** — Click "📖 Manual" in the app (2000+ lines of comprehensive help)
- **Issues** — Check troubleshooting section in README
- **Questions** — Refer to project repository or documentation
- **Offline Help** — All help is available offline after app launches

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**Python Version**: 3.10+  
**Platforms**: Windows, macOS, Linux  

**Author**: Carmine Akabane (Serge) — https://github.com/CarmineAkanabe

**Built with ❤️ for educators and developers**
