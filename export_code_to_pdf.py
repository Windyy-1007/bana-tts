#!/usr/bin/env python3
"""
Code Export Tool - Export all typed code files to PDF
This tool exports all Python, YAML, Jupyter, JSON, HTML, CSS, JS, and Dockerfile content to a PDF file.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
import argparse

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted
    from reportlab.lib.colors import black, blue, red, green
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Error: reportlab is required. Install it with: pip install reportlab")
    sys.exit(1)

class CodeExporter:
    def __init__(self, root_dir, output_file="code_export.pdf"):
        self.root_dir = Path(root_dir)
        self.output_file = output_file
        self.code_extensions = {
            '.py': 'Python',
            '.yml': 'YAML', 
            '.yaml': 'YAML',
            '.ipynb': 'Jupyter Notebook',
            '.json': 'JSON',
            '.html': 'HTML',
            '.css': 'CSS',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React JSX',
            '.tsx': 'React TSX',
            '.md': 'Markdown',
            '.sh': 'Shell Script',
            '.bat': 'Batch Script',
            '.ps1': 'PowerShell',
            '.sql': 'SQL',
            '.xml': 'XML',
            '.toml': 'TOML',
            '.ini': 'INI',
            '.cfg': 'Config',
            '.conf': 'Config'
        }
        
        # Files without extensions that are typically code files
        self.special_files = {
            'Dockerfile': 'Dockerfile',
            'Makefile': 'Makefile',
            'requirements.txt': 'Requirements',
            'setup.py': 'Python Setup',
            'pyproject.toml': 'Python Project',
            '.gitignore': 'Git Ignore',
            '.env': 'Environment'
        }
        
        self.exclude_patterns = {
            '__pycache__',
            '.git',
            '.vscode',
            'node_modules',
            '.pytest_cache',
            '.mypy_cache',
            'dist',
            'build',
            '*.egg-info',
            '.ipynb_checkpoints',
            'logs',
            'checkpts',
            'data',  # Exclude data directories as specified
            'venv',  # Exclude virtual environment
            'env',   # Exclude virtual environment (alternative name)
            '.venv', # Exclude virtual environment (hidden)
            '.env',  # Exclude virtual environment (hidden alternative)
            'site-packages'  # Exclude site-packages if found directly
        }
        
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
    def _setup_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=blue
        )
        
        # File header style
        self.file_header_style = ParagraphStyle(
            'FileHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=10,
            textColor=red,
            keepWithNext=True
        )
        
        # File info style
        self.file_info_style = ParagraphStyle(
            'FileInfo',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceBefore=5,
            spaceAfter=5,
            textColor=green
        )
        
        # Code style with monospace font
        self.code_style = ParagraphStyle(
            'Code',
            parent=self.styles['Code'],
            fontSize=9,
            fontName='Courier',
            leftIndent=20,
            rightIndent=20,
            spaceBefore=5,
            spaceAfter=10,
            backColor=None
        )

    def should_include_file(self, file_path):
        """Check if a file should be included in the export"""
        rel_path = file_path.relative_to(self.root_dir)
        
        # Check if any part of the path contains excluded patterns
        for part in rel_path.parts:
            if part in self.exclude_patterns:
                return False
            if part.startswith('.') and part not in ['.env', '.gitignore']:
                return False
                
        # Check file extension
        suffix = file_path.suffix.lower()
        if suffix in self.code_extensions:
            return True
            
        # Check special files
        if file_path.name in self.special_files:
            return True
            
        return False

    def get_file_type(self, file_path):
        """Get the file type description"""
        suffix = file_path.suffix.lower()
        if suffix in self.code_extensions:
            return self.code_extensions[suffix]
        elif file_path.name in self.special_files:
            return self.special_files[file_path.name]
        return "Text File"

    def read_file_content(self, file_path):
        """Read file content with error handling"""
        try:
            # Handle Jupyter notebooks specially
            if file_path.suffix == '.ipynb':
                return self.extract_notebook_content(file_path)
            
            # Try UTF-8 first, then other encodings
            encodings = ['utf-8', 'utf-16', 'latin1', 'cp1252']
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    return content
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, read as binary and decode with errors='replace'
            with open(file_path, 'rb') as f:
                content = f.read().decode('utf-8', errors='replace')
            return content
            
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def extract_notebook_content(self, file_path):
        """Extract content from Jupyter notebook"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            content_parts = []
            for i, cell in enumerate(notebook.get('cells', [])):
                cell_type = cell.get('cell_type', 'unknown')
                source = cell.get('source', [])
                
                if isinstance(source, list):
                    source_text = ''.join(source)
                else:
                    source_text = source
                
                if source_text.strip():
                    content_parts.append(f"# Cell {i+1} ({cell_type})")
                    content_parts.append(source_text)
                    content_parts.append("")
            
            return '\n'.join(content_parts)
            
        except Exception as e:
            return f"Error reading notebook: {str(e)}"

    def find_code_files(self):
        """Find all code files in the repository"""
        code_files = []
        
        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and self.should_include_file(file_path):
                code_files.append(file_path)
        
        # Sort files by path for consistent ordering
        code_files.sort(key=lambda x: str(x))
        return code_files

    def create_pdf(self):
        """Create the PDF with all code files"""
        print(f"Creating PDF export: {self.output_file}")
        
        # Create document
        doc = SimpleDocTemplate(
            self.output_file,
            pagesize=A4,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Build story (content)
        story = []
        
        # Add title page
        story.append(Paragraph("Code Repository Export", self.title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Add metadata
        metadata = [
            f"Repository: {self.root_dir.name}",
            f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total Files: {len(self.find_code_files())}"
        ]
        
        for meta in metadata:
            story.append(Paragraph(meta, self.file_info_style))
        
        story.append(PageBreak())
        
        # Add table of contents
        story.append(Paragraph("Table of Contents", self.title_style))
        story.append(Spacer(1, 0.2*inch))
        
        code_files = self.find_code_files()
        for file_path in code_files:
            rel_path = file_path.relative_to(self.root_dir)
            file_type = self.get_file_type(file_path)
            toc_entry = f"{rel_path} ({file_type})"
            story.append(Paragraph(toc_entry, self.styles['Normal']))
        
        story.append(PageBreak())
        
        # Add each file
        for i, file_path in enumerate(code_files):
            rel_path = file_path.relative_to(self.root_dir)
            file_type = self.get_file_type(file_path)
            
            print(f"Processing {i+1}/{len(code_files)}: {rel_path}")
            
            # File header
            header_text = f"File: {rel_path}"
            story.append(Paragraph(header_text, self.file_header_style))
            
            # File info
            try:
                file_stats = file_path.stat()
                file_size = file_stats.st_size
                modified_time = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                info_text = f"Type: {file_type} | Size: {file_size} bytes | Modified: {modified_time}"
                story.append(Paragraph(info_text, self.file_info_style))
            except:
                info_text = f"Type: {file_type}"
                story.append(Paragraph(info_text, self.file_info_style))
            
            # File content
            content = self.read_file_content(file_path)
            
            # Split content into chunks to avoid memory issues
            max_chunk_size = 10000  # characters
            if len(content) > max_chunk_size:
                chunks = [content[i:i+max_chunk_size] for i in range(0, len(content), max_chunk_size)]
                for j, chunk in enumerate(chunks):
                    if j > 0:
                        story.append(Paragraph(f"... (continued from chunk {j}) ...", self.file_info_style))
                    story.append(Preformatted(chunk, self.code_style))
            else:
                story.append(Preformatted(content, self.code_style))
            
            # Add page break between files (except for the last file)
            if i < len(code_files) - 1:
                story.append(PageBreak())
        
        # Build PDF
        try:
            doc.build(story)
            print(f"✅ PDF created successfully: {self.output_file}")
        except Exception as e:
            print(f"❌ Error creating PDF: {str(e)}")
            return False
        
        return True

def main():
    parser = argparse.ArgumentParser(description="Export code files to PDF")
    parser.add_argument("--directory", "-d", default=".", help="Directory to scan (default: current directory)")
    parser.add_argument("--output", "-o", default="code_export.pdf", help="Output PDF filename")
    parser.add_argument("--preview", "-p", action="store_true", help="Preview files that would be included")
    
    args = parser.parse_args()
    
    # Convert to absolute path
    root_dir = Path(args.directory).resolve()
    
    if not root_dir.exists():
        print(f"❌ Directory not found: {root_dir}")
        sys.exit(1)
    
    print(f"📁 Scanning directory: {root_dir}")
    
    exporter = CodeExporter(root_dir, args.output)
    
    if args.preview:
        # Preview mode - just list files
        code_files = exporter.find_code_files()
        print(f"\n📋 Found {len(code_files)} code files:")
        print("=" * 60)
        
        total_size = 0
        for file_path in code_files:
            rel_path = file_path.relative_to(root_dir)
            file_type = exporter.get_file_type(file_path)
            try:
                file_size = file_path.stat().st_size
                total_size += file_size
                print(f"  {rel_path} ({file_type}) - {file_size} bytes")
            except:
                print(f"  {rel_path} ({file_type}) - unknown size")
        
        print("=" * 60)
        print(f"📊 Total size: {total_size:,} bytes ({total_size / (1024*1024):.2f} MB)")
        return
    
    # Create PDF
    success = exporter.create_pdf()
    
    if success:
        output_path = Path(args.output).resolve()
        print(f"📄 PDF saved to: {output_path}")
        
        # Show file size
        try:
            file_size = output_path.stat().st_size
            print(f"📊 PDF size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
        except:
            pass
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
