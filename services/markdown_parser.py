import markdown
from markdown.extensions import fenced_code
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import TerminalFormatter
import re


class MarkdownParser:
    """Parses and renders markdown content."""

    def __init__(self):
        """Initialize markdown parser."""
        self.md = markdown.Markdown(extensions=[
            'extra',
            'codehilite',
            'toc'
        ])

    def parse(self, content: str) -> dict:
        """Parse markdown content into structured format."""
        # Extract title (first H1)
        title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Untitled"

        # Extract headings structure
        headings = self._extract_headings(content)

        # Parse markdown
        html = self.md.convert(content)

        return {
            'title': title,
            'headings': headings,
            'html': html,
            'raw': content
        }

    def _extract_headings(self, content: str) -> list:
        """Extract heading structure from markdown."""
        headings = []
        lines = content.split('\n')

        for line in lines:
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                title = line.lstrip('#').strip()
                headings.append({
                    'level': level,
                    'title': title
                })

        return headings

    def extract_code_blocks(self, content: str) -> list:
        """Extract code blocks from markdown."""
        blocks = []
        pattern = r'```(\w+)?\n(.*?)\n```'

        for match in re.finditer(pattern, content, re.DOTALL):
            language = match.group(1) or 'text'
            code = match.group(2)
            blocks.append({
                'language': language,
                'code': code
            })

        return blocks

    def highlight_code(self, code: str, language: str = 'python') -> str:
        """Highlight code using Pygments."""
        try:
            lexer = get_lexer_by_name(language)
        except:
            lexer = guess_lexer(code)

        formatter = TerminalFormatter()
        return highlight(code, lexer, formatter)

    def extract_text(self, content: str) -> str:
        """Extract plain text from markdown."""
        # Remove code blocks
        text = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        # Remove markdown syntax
        text = re.sub(r'[#*`_\[\]()]', '', text)
        return text.strip()
