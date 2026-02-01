# DevDocs - Offline Documentation Reader

A desktop application for downloading and reading technical documentation offline from GitHub repositories.

## Project Description

DevDocs is a Python-based desktop application that allows users to download markdown documentation from public GitHub repositories and read them offline. The application features a three-panel interface with a topic sidebar, document tree view, and markdown reader with syntax highlighting.

## Features

- Download markdown documentation from GitHub repositories
- Offline reading after initial download
- Three-panel interface for easy navigation
- Real-time document search
- Syntax highlighting for code blocks
- Track read/unread documents
- SQLite database for persistent storage
- Support for subfolder targeting in repositories

## Technologies Used

| Component | Technology | Version |
|-----------|-----------|---------|
| Programming Language | Python | 3.10+ |
| GUI Framework | customTkinter | 5.2.2 |
| Database | SQLite3 | Built-in |
| Markdown Parser | Markdown | 3.10.1 |
| Syntax Highlighting | Pygments | 2.19.2 |
| HTTP Client | Requests | 2.32.5 |

## Project Structure

```
DevDocs/
├── app.py                      # Application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── database/
│   └── db_manager.py          # Database operations
├── services/
│   ├── downloader.py          # GitHub download functionality
│   ├── markdown_parser.py     # Markdown parsing
│   └── file_manager.py        # File operations
└── ui/
    ├── main_window.py         # Main application window
    ├── topic_view.py          # Topic sidebar
    ├── document_view.py       # Document tree view
    └── reader_view.py         # Markdown reader
```

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- pip package manager
- Internet connection (for initial setup and downloads)

### Installation Steps

1. **Clone or download the project:**
   ```bash
   git clone https://github.com/CarmineAkanabe/DevDocs.git
   cd DevDocs
   ```

2. **Create a virtual environment:**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

## Usage

### Adding Documentation Topics

1. Click the "Add Topic" button in the header
2. Enter the topic name, GitHub repository URL, and optional subfolder path
3. Click "ADD TOPIC" to save

### Downloading Documentation

1. Select a topic from the sidebar
2. Click the "Sync" button in the header
3. Wait for the download to complete

### Reading Documentation

1. Select a topic from the sidebar
2. Browse the document tree in the middle panel
3. Click any document to view it in the reader panel
4. Use the search box to filter documents

## Dependencies

All required packages are listed in `requirements.txt`:

```
certifi==2026.1.4
charset-normalizer==3.4.4
customtkinter==5.2.2
darkdetect==0.8.0
idna==3.11
Markdown==3.10.1
packaging==26.0
Pygments==2.19.2
requests==2.32.5
urllib3==2.6.3
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Carmine Akanabe (Serge)
- GitHub: [@CarmineAkanabe](https://github.com/CarmineAkanabe)
