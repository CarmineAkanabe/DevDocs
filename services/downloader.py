import requests
import zipfile
import io
import os
from pathlib import Path
from typing import Optional


class Downloader:
    """Handles downloading documentation from GitHub."""

    @staticmethod
    def download_repo_zip(github_url: str) -> bytes:
        """Download repository as ZIP from GitHub."""
        # Convert GitHub URL to raw download URL
        # Support both https://github.com/user/repo and https://github.com/user/repo.git
        repo_url = github_url.rstrip('.git')
        if not repo_url.startswith('https://github.com/'):
            raise ValueError("Invalid GitHub URL")

        # Try multiple branches
        branches = ['main', 'master', 'develop', 'dev']
        last_error = None

        for branch in branches:
            try:
                download_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
                response = requests.get(download_url, timeout=30)
                if response.status_code == 200:
                    return response.content
            except Exception as e:
                last_error = e
                continue

        # If all branches failed, raise error
        if last_error:
            raise Exception(f"Could not download repository from any branch: {last_error}")
        else:
            raise Exception("Repository not found or no accessible branches")

    @staticmethod
    def extract_markdown_files(zip_bytes: bytes, target_dir: str, subfolder: Optional[str] = None) -> list:
        """Extract markdown files from ZIP."""
        extracted_files = []
        Path(target_dir).mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zip_ref:
            for file_info in zip_ref.filelist:
                # Skip directories and non-markdown files
                if file_info.filename.endswith('/') or not file_info.filename.endswith('.md'):
                    continue

                # Skip hidden files and common non-doc files
                parts = file_info.filename.split('/')
                if any(part.startswith('.') for part in parts):
                    continue

                # If subfolder specified, only extract from that subfolder
                if subfolder:
                    if subfolder not in file_info.filename:
                        continue

                # Extract file
                extracted_data = zip_ref.read(file_info.filename)
                
                # Build local path preserving directory structure
                rel_path = file_info.filename
                if subfolder:
                    # Find subfolder in path and start from there
                    idx = rel_path.find(subfolder)
                    if idx != -1:
                        rel_path = rel_path[idx:]
                else:
                    # Remove repo root folder name
                    rel_path = '/'.join(rel_path.split('/')[1:])

                local_path = os.path.join(target_dir, rel_path.replace('/', os.sep))
                os.makedirs(os.path.dirname(local_path), exist_ok=True)

                with open(local_path, 'wb') as f:
                    f.write(extracted_data)

                extracted_files.append({
                    'local_path': local_path,
                    'relative_path': rel_path
                })

        return extracted_files
