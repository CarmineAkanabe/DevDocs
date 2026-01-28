# 📖 DevDocs User Manual

**Version 1.0** | **Last Updated: January 2026**

Welcome to the comprehensive user manual for DevDocs - your offline documentation companion. This guide will help you master all features and get the most out of the application.

---

## 📑 Table of Contents

1. [Introduction](#-introduction)
2. [Getting Started](#-getting-started)
3. [Interface Overview](#-interface-overview)
4. [Core Features](#-core-features)
5. [Advanced Usage](#-advanced-usage)
6. [Tips & Tricks](#-tips--tricks)
7. [Troubleshooting](#-troubleshooting)
8. [FAQ](#-faq)

---

## 🎯 Introduction

### What is DevDocs?

DevDocs is a powerful offline documentation reader designed for developers who need quick, reliable access to technical documentation without depending on internet connectivity. Built with Python and featuring a modern GitHub-inspired interface, DevDocs transforms how you interact with documentation.

### Key Benefits

- **🔌 Complete Offline Access** - Download once, read forever
- **⚡ Lightning Fast** - No loading times, no network delays
- **🎨 Beautiful Interface** - Easy on the eyes for long reading sessions
- **📊 Progress Tracking** - Know what you've read and what's left
- **🔍 Instant Search** - Find any document in milliseconds
- **📚 Unlimited Topics** - Add documentation from any GitHub repository

### Who Should Use DevDocs?

- Developers learning new frameworks
- Students studying programming languages
- Teams needing consistent documentation
- Anyone working in areas with limited internet
- Technical writers referencing multiple docs

---

## 🚀 Getting Started

### Launching the Application

1. **Activate Virtual Environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Run DevDocs:**
   ```bash
   python app.py
   ```

3. **Splash Screen:**
   - A beautiful splash screen appears briefly
   - Shows the DevDocs logo and loading progress
   - Automatically transitions to the main interface

### First Launch Experience

When you first open DevDocs, you'll see:

1. **Three Pre-configured Topics:**
   - 📘 **GitHub Docs** - Official GitHub documentation
   - 🐍 **Python Docs** - Python standard library
   - ⚛️ **React Docs** - React framework documentation

2. **Empty Document Tree:**
   - No documents are downloaded yet
   - You'll need to sync each topic to download its documentation

3. **Welcome Message:**
   - The reader panel shows a welcome message
   - Instructions on how to get started

---

## 🖥️ Interface Overview

DevDocs features a clean, three-panel layout optimized for efficient documentation browsing.

### Header Bar

Located at the top of the window, the header contains:

#### Left Side
- **📘 DevDocs** - Application title and branding

#### Right Side
- **✚ Add Topic** - Opens dialog to add new documentation sources
- **📖 Manual** - Opens this user manual
- **ℹ About** - Shows README and project information
- **⟳ Sync** - Downloads/updates documentation for selected topic

### Main Content Area

#### 1. Topic Sidebar (Left Panel - 220px)

**Purpose:** Manage and switch between documentation topics

**Features:**
- **Topic List:**
  - Each topic shown as a button with 📘 icon
  - Click to select and view its documents
  - Selected topic highlighted in green
  
- **Topic Information Panel:**
  - **Documents:** Total count of downloaded documents
  - **Unread:** Number of documents you haven't read yet
  - **Last sync:** Date of last documentation update

**Visual Indicators:**
- **Green highlight** - Currently selected topic
- **Gray background** - Unselected topics
- **Hover effect** - Subtle highlight on mouse over

#### 2. Document Tree (Middle Panel - 300px)

**Purpose:** Browse and search documentation files

**Features:**
- **Search Bar:**
  - 🔍 icon for visual clarity
  - Real-time filtering as you type
  - Case-insensitive search
  - Searches document titles and paths

- **Folder Structure:**
  - 📁 icon for folders
  - Click to expand/collapse
  - Preserves repository structure
  - Nested folders supported

- **Document List:**
  - 📄 icon for documents
  - Click to open and read
  - **Unread documents** shown in blue with ● indicator
  - **Read documents** shown in gray

**Navigation:**
- Folders can be collapsed to reduce clutter
- Search results maintain folder hierarchy
- Clear search to restore full tree view

#### 3. Reader Panel (Right Panel - Flexible Width)

**Purpose:** Display formatted documentation content

**Features:**
- **Breadcrumb Navigation:**
  - Shows document path (e.g., `docs > api > reference.md`)
  - Helps you understand document location
  - Displayed in gray text

- **Document Title:**
  - Large, prominent heading in blue
  - Extracted from first H1 in markdown
  - Falls back to filename if no H1 found

- **Content Area:**
  - Scrollable content with smooth scrolling
  - Formatted markdown rendering
  - Syntax-highlighted code blocks
  - Styled headings, lists, and paragraphs

### Status Bar

Located at the bottom of the window:

#### Left Side
- **Status Messages:**
  - "Ready" - Idle state
  - "Downloading..." - Active download
  - "✓ Downloaded X files" - Success message
  - "✗ Error: ..." - Error messages

#### Center
- **© 2026 DevDocs** - Copyright notice

#### Right Side
- **Author Link** - Click to visit GitHub profile
- **Progress Bar** - Shows during downloads

---

## ⭐ Core Features

### Feature 1: Adding Documentation Topics

**What it does:** Allows you to add documentation from any public GitHub repository.

**How to use:**

1. **Open Add Topic Dialog:**
   - Click **"✚ Add Topic"** button in header
   - Dialog opens centered on screen (600x500px)

2. **Fill in the Form:**
   
   **Topic Name** (Required)
   - Enter a descriptive name for the documentation
   - Examples: "Vue.js", "Django", "TypeScript"
   - This name appears in the sidebar
   
   **GitHub Repository URL** (Required)
   - Must be a public GitHub repository
   - Format: `https://github.com/username/repository`
   - Examples:
     - `https://github.com/vuejs/docs`
     - `https://github.com/django/django`
     - `https://github.com/microsoft/TypeScript`
   
   **Documentation Subfolder** (Optional)
   - Specify if docs are in a subfolder
   - Common values: `docs`, `documentation`, `Doc`, `content`
   - Leave empty to search entire repository
   - Examples:
     - `docs` - for `/docs` folder
     - `src/content` - for nested folders

3. **Submit:**
   - Click **"✓ ADD TOPIC"** button (large green button)
   - Or press **Enter** key
   - Dialog closes automatically on success

4. **Validation:**
   - Empty fields trigger warning message
   - Invalid GitHub URLs are rejected
   - Duplicate topic names are prevented

**Tips:**
- Use descriptive names to easily identify topics
- Check the repository structure on GitHub first
- Most projects use `docs` or `documentation` folders
- Leave subfolder empty if unsure - you can always re-add

---

### Feature 2: Downloading Documentation

**What it does:** Downloads markdown files from GitHub repositories to your local machine.

**How to use:**

1. **Select Topic:**
   - Click any topic in the sidebar
   - Topic highlights in green

2. **Initiate Download:**
   - Click **"⟳ Sync"** button in header
   - Progress bar appears in status bar

3. **Monitor Progress:**
   - Status shows "Downloading..."
   - Progress bar fills from left to right
   - May take 30 seconds to 2 minutes depending on size

4. **Completion:**
   - Status shows "✓ Downloaded X files"
   - Documents appear in middle panel
   - Progress bar disappears after 2 seconds

**What happens during download:**
- DevDocs tries multiple branches (main, master, develop, dev)
- Extracts all `.md` files from the repository
- Preserves folder structure
- Skips hidden files and folders
- Falls back to README.md if no docs found
- Stores files in `docs/topic_name/` directory

**Re-syncing:**
- Click **"⟳ Sync"** again to update documentation
- Old files are replaced with new versions
- Read/unread status is reset
- Useful for getting latest documentation updates

---

### Feature 3: Browsing Documentation

**What it does:** Provides an intuitive tree view for navigating documentation files.

**How to use:**

1. **Expand Folders:**
   - Click any 📁 folder to expand
   - Click again to collapse
   - Nested folders supported

2. **View Documents:**
   - Documents shown with 📄 icon
   - **Unread:** Blue text with ● indicator
   - **Read:** Gray text, no indicator

3. **Open Document:**
   - Click any document name
   - Content loads in right panel
   - Automatically marked as read

**Organization:**
- Folders maintain repository structure
- Documents sorted alphabetically
- Hierarchy preserved from source
- Collapsible for clean view

---

### Feature 4: Searching Documents

**What it does:** Instantly filters documents based on your search query.

**How to use:**

1. **Focus Search Bar:**
   - Click in the 🔍 search box
   - Or use `Ctrl+F` shortcut

2. **Type Query:**
   - Results filter in real-time
   - Case-insensitive matching
   - Searches titles and paths

3. **View Results:**
   - Matching documents remain visible
   - Non-matching documents hidden
   - Folder structure preserved

4. **Clear Search:**
   - Delete all text in search box
   - Or press `Escape` key
   - All documents reappear

**Search Tips:**
- Use partial words (e.g., "intro" finds "introduction")
- Search by folder name to see all docs in that folder
- Combine with folder expansion for precise navigation
- Search is instant - no need to press Enter

---

### Feature 5: Reading Documentation

**What it does:** Renders markdown content with beautiful formatting and syntax highlighting.

**How to use:**

1. **Open Document:**
   - Click any document in tree view
   - Content loads immediately

2. **Navigate Content:**
   - Scroll with mouse wheel or scrollbar
   - Smooth scrolling for comfortable reading

3. **View Formatted Elements:**
   
   **Headings:**
   - H1: Large blue heading (32pt)
   - H2: Medium blue heading (24pt)
   - H3: Smaller blue heading (20pt)
   - Gradient blue colors for visual hierarchy
   
   **Paragraphs:**
   - Clean, readable text in light gray
   - Proper line spacing
   - Wrapped to fit panel width
   
   **Lists:**
   - Bullet points with • character
   - Indented for clarity
   - Proper spacing between items
   
   **Code Blocks:**
   - Dark background (#161b22)
   - Syntax highlighting with Pygments
   - Language label at top (e.g., "📋 PYTHON")
   - Monospace font (Consolas)
   - Scrollable for long code

4. **Track Progress:**
   - Document marked as read automatically
   - ● indicator disappears
   - Text color changes to gray in tree

**Supported Markdown:**
- Headings (H1-H6)
- Paragraphs
- Bullet lists
- Code blocks with language specification
- Inline code (rendered as regular text)

---

### Feature 6: Progress Tracking

**What it does:** Tracks which documents you've read and displays statistics.

**How to use:**

1. **View Topic Statistics:**
   - Select any topic in sidebar
   - Check info panel at bottom of sidebar
   - Shows:
     - Total documents
     - Unread count
     - Last sync date

2. **Identify Unread Documents:**
   - Look for blue text in document tree
   - ● indicator marks unread documents
   - Bold font for emphasis

3. **Mark as Read:**
   - Simply click and open a document
   - Automatically marked as read
   - No manual action needed

4. **Track Learning Progress:**
   - Watch unread count decrease
   - See which topics you've completed
   - Identify areas needing attention

**Benefits:**
- Know exactly what you've covered
- Avoid re-reading familiar content
- Systematic learning approach
- Visual motivation to complete topics

---

### Feature 7: Offline Access

**What it does:** Provides complete offline functionality after initial download.

**How it works:**

1. **Initial Download:**
   - Requires internet connection
   - Downloads all markdown files
   - Stores locally in `docs/` folder
   - Saves metadata in SQLite database

2. **Offline Usage:**
   - No internet required after download
   - All features work offline:
     - Browse documents
     - Search content
     - Read documentation
     - Track progress
     - Switch between topics

3. **Data Storage:**
   - **Files:** `docs/topic_name/` directories
   - **Database:** `devdocs.db` SQLite file
   - **Metadata:** Topics, documents, read status

**Benefits:**
- Work anywhere without internet
- No data usage after download
- Fast, instant access
- No ads or tracking
- Complete privacy

---

## 🎓 Advanced Usage

### Customizing Topics

**Targeting Specific Folders:**

Some repositories have documentation in specific locations:

```
Repository Structure:
├── src/
├── docs/           ← Documentation here
│   ├── api/
│   ├── guides/
│   └── reference/
├── tests/
└── README.md
```

**Solution:** Specify `docs` in the subfolder field when adding the topic.

**Multiple Documentation Folders:**

If a repository has docs in multiple locations, add separate topics:
- "Project - API Docs" → subfolder: `docs/api`
- "Project - Guides" → subfolder: `docs/guides`

### Managing Large Documentation Sets

**For repositories with 100+ documents:**

1. **Use Search Extensively:**
   - Don't scroll through entire tree
   - Search for specific topics
   - Use folder names in search

2. **Collapse Unused Folders:**
   - Keep tree clean and manageable
   - Expand only what you need
   - Reduces visual clutter

3. **Track Progress:**
   - Focus on unread documents
   - Complete one folder at a time
   - Use read status as checklist

### Keyboard Efficiency

**Power User Shortcuts:**

1. **Adding Topics:**
   - Click "✚ Add Topic"
   - Tab through fields
   - Press Enter to submit

2. **Searching:**
   - `Ctrl+F` to focus search
   - Type query
   - `Escape` to clear

3. **Navigation:**
   - Use mouse wheel for smooth scrolling
   - Click folders to expand/collapse
   - Click documents to open

### Organizing Your Workspace

**Best Practices:**

1. **Topic Naming:**
   - Use version numbers: "React v18 Docs"
   - Include framework name: "Vue.js 3.x"
   - Be specific: "Django REST Framework"

2. **Topic Organization:**
   - Group by language (Python, JavaScript, etc.)
   - Group by framework (React, Vue, Angular)
   - Group by purpose (Backend, Frontend, DevOps)

3. **Regular Maintenance:**
   - Sync topics monthly for updates
   - Remove unused topics
   - Re-download if files corrupted

---

## 💡 Tips & Tricks

### Productivity Tips

1. **Download Before Travel:**
   - Sync all needed topics before going offline
   - Perfect for flights, trains, remote areas
   - No internet anxiety

2. **Use as Reference:**
   - Keep DevDocs open while coding
   - Quick lookup without browser
   - No distractions from ads or navigation

3. **Learn Systematically:**
   - Pick a topic
   - Read documents in order
   - Track progress with read status
   - Complete entire topics

4. **Search Effectively:**
   - Use specific terms
   - Try different keywords
   - Search by concept, not exact title

### Interface Tips

1. **Resize Panels:**
   - Drag panel borders to resize
   - Make reader wider for long lines
   - Collapse sidebar when not needed

2. **Window Management:**
   - Maximize for full-screen reading
   - Resize to fit alongside code editor
   - Use multiple monitors

3. **Theme Comfort:**
   - Dark theme reduces eye strain
   - Optimized for long reading sessions
   - GitHub-inspired colors

### Documentation Tips

1. **Check Repository First:**
   - Visit GitHub repo before adding
   - Verify documentation exists
   - Note subfolder location
   - Check if actively maintained

2. **Start with README:**
   - Most repos have README.md
   - Good overview of project
   - Links to detailed docs

3. **Version Awareness:**
   - Documentation reflects current repo state
   - May not match specific versions
   - Check repo branches for version-specific docs

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "No documents found" after sync

**Symptoms:**
- Sync completes successfully
- Document tree shows "📭 No documents found"
- Status shows "Downloaded 0 files"

**Causes:**
- Repository has no markdown files
- Documentation in subfolder not specified
- Documentation in different branch

**Solutions:**

1. **Check Repository Structure:**
   - Visit repository on GitHub
   - Look for `docs/`, `documentation/`, or `Doc/` folders
   - Note the exact folder name

2. **Re-add Topic with Subfolder:**
   - Remove current topic (if possible)
   - Add again with correct subfolder path
   - Example: `docs` or `documentation`

3. **Try Different Branch:**
   - Some repos use `gh-pages` or `docs` branch
   - DevDocs tries main/master/develop/dev automatically
   - May need to check repo settings

4. **Verify Markdown Files:**
   - Ensure repo contains `.md` files
   - Some projects use other formats (HTML, RST)
   - DevDocs only supports markdown

#### Issue 2: Download fails with error

**Symptoms:**
- Status shows "✗ Error: ..."
- Progress bar disappears
- No documents downloaded

**Causes:**
- Invalid GitHub URL
- Private repository
- Network connectivity issues
- Repository doesn't exist

**Solutions:**

1. **Verify URL:**
   - Must start with `https://github.com/`
   - Must be public repository
   - Check for typos

2. **Test URL:**
   - Open URL in browser
   - Verify repository exists
   - Check if public or private

3. **Check Internet:**
   - Ensure internet connection active
   - Try syncing again
   - Check firewall settings

4. **Try Different Repository:**
   - Test with known-good repo
   - Example: `https://github.com/github/docs`
   - Verify DevDocs is working

#### Issue 3: Search not working

**Symptoms:**
- Typing in search box shows no results
- All documents disappear
- Search seems broken

**Causes:**
- No documents match search query
- Topic not synced yet
- Search too specific

**Solutions:**

1. **Clear Search:**
   - Delete all text in search box
   - Or press `Escape` key
   - Verify documents reappear

2. **Try Broader Search:**
   - Use fewer characters
   - Try different keywords
   - Search by folder name

3. **Verify Documents Exist:**
   - Clear search completely
   - Check if documents visible
   - Sync topic if empty

#### Issue 4: Widget refresh errors in console

**Symptoms:**
- Error messages in terminal
- Mentions "invalid command name"
- App still works normally

**Causes:**
- Tkinter widget cleanup timing
- Harmless background process
- Does not affect functionality

**Solutions:**
- **Ignore these errors** - they're harmless
- App handles cleanup safely
- No action needed
- Will be fixed in future update

#### Issue 5: Slow performance with large topics

**Symptoms:**
- App feels sluggish
- Scrolling is slow
- Search takes time

**Causes:**
- Very large documentation sets (1000+ files)
- Many folders expanded simultaneously
- System resource constraints

**Solutions:**

1. **Collapse Unused Folders:**
   - Keep only needed folders expanded
   - Reduces rendering load

2. **Use Search:**
   - Instead of scrolling
   - Faster than visual browsing

3. **Split Large Topics:**
   - Add separate topics for subfolders
   - Example: "Project - API" and "Project - Guides"

4. **Close Other Apps:**
   - Free up system resources
   - Especially on older computers

---

## ❓ FAQ

### General Questions

**Q: Is DevDocs free?**
A: Yes, completely free and open-source under MIT License.

**Q: Does DevDocs work offline?**
A: Yes, after initial download, everything works offline.

**Q: What file formats are supported?**
A: Only Markdown (.md) files are supported.

**Q: Can I use private repositories?**
A: No, only public GitHub repositories are supported.

**Q: Does DevDocs track my usage?**
A: No, absolutely no telemetry or tracking. Completely private.

### Technical Questions

**Q: Where are documents stored?**
A: In the `docs/` folder within the DevDocs directory.

**Q: Where is the database?**
A: `devdocs.db` file in the DevDocs root directory.

**Q: Can I backup my data?**
A: Yes, copy the `docs/` folder and `devdocs.db` file.

**Q: How do I reset DevDocs?**
A: Delete `devdocs.db` and `docs/` folder, then restart.

**Q: Can I edit downloaded documentation?**
A: Files are in `docs/` folder - you can edit them, but changes will be overwritten on next sync.

### Feature Questions

**Q: Can I add non-GitHub documentation?**
A: No, currently only GitHub repositories are supported.

**Q: Can I export documents?**
A: Documents are already in markdown format in `docs/` folder.

**Q: Can I print documentation?**
A: Not directly, but you can open markdown files in any editor and print from there.

**Q: Can I share topics with others?**
A: Yes, share the topic name and GitHub URL. They can add it themselves.

**Q: Can I customize the theme?**
A: Not currently, but may be added in future versions.

---

## 📞 Getting Help

If you need additional assistance:

1. **Check This Manual** - Most questions answered here
2. **Review README.md** - Installation and setup help
3. **Check GitHub Issues** - See if others had same problem
4. **Create New Issue** - Provide detailed information:
   - Operating system
   - Python version
   - Steps to reproduce
   - Error messages
   - Screenshots if applicable

---

## 🎉 Conclusion

Congratulations! You now know how to use all features of DevDocs. Here's a quick recap:

✅ **Add Topics** - From any GitHub repository
✅ **Download Docs** - Sync to get latest documentation
✅ **Browse & Search** - Find documents quickly
✅ **Read Offline** - Beautiful markdown rendering
✅ **Track Progress** - Know what you've read
✅ **Work Anywhere** - Complete offline functionality

**Happy documenting!** 📚

---

<div align="center">

**DevDocs User Manual v1.0**

Built with ❤️ for developers who love documentation

[Back to Top](#-devdocs-user-manual)

</div>
