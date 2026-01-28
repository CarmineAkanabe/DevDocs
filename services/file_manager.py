import os
from pathlib import Path


class FileManager:
    """Manages file operations for documentation."""

    @staticmethod
    def ensure_docs_directory(docs_dir: str = "docs"):
        """Ensure docs directory exists."""
        Path(docs_dir).mkdir(parents=True, exist_ok=True)
        return docs_dir

    @staticmethod
    def get_topic_directory(docs_dir: str, topic_name: str) -> str:
        """Get or create topic-specific directory."""
        topic_dir = os.path.join(docs_dir, topic_name.lower().replace(' ', '_'))
        Path(topic_dir).mkdir(parents=True, exist_ok=True)
        return topic_dir

    @staticmethod
    def read_file(file_path: str) -> str:
        """Read file content."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    @staticmethod
    def write_file(file_path: str, content: str):
        """Write content to file."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def list_markdown_files(directory: str) -> list:
        """List all markdown files in directory recursively."""
        md_files = []
        for root, dirs, files in os.walk(directory):
            # Skip hidden directories
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for file in files:
                if file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, directory)
                    md_files.append({
                        'path': full_path,
                        'relative_path': rel_path,
                        'filename': file
                    })
        return sorted(md_files, key=lambda x: x['relative_path'])

    @staticmethod
    def delete_directory(dir_path: str):
        """Delete directory and all contents."""
        import shutil
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(file_path)

    @staticmethod
    def build_file_tree(directory: str) -> dict:
        """Build a tree structure of files and folders."""
        tree = {'folders': {}, 'files': []}

        for item in os.listdir(directory):
            if item.startswith('.'):
                continue

            full_path = os.path.join(directory, item)

            if os.path.isdir(full_path):
                tree['folders'][item] = FileManager.build_file_tree(full_path)
            elif item.endswith('.md'):
                tree['files'].append(item)

        return tree
