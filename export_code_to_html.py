#!/usr/bin/env python3
"""
Simple Code Export Tool - Export all typed code files to HTML
This is a simpler version that doesn't require external dependencies.
"""

import os
import html
import json
from pathlib import Path
from datetime import datetime
import argparse

class SimpleCodeExporter:
    def __init__(self, root_dir, output_file="code_export.html"):
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

    def get_language_for_highlight(self, file_path):
        """Get language identifier for syntax highlighting"""
        suffix = file_path.suffix.lower()
        name = file_path.name.lower()
        
        mapping = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'javascript',
            '.tsx': 'typescript',
            '.html': 'html',
            '.css': 'css',
            '.json': 'json',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.md': 'markdown',
            '.sh': 'bash',
            '.sql': 'sql',
            '.xml': 'xml'
        }
        
        if suffix in mapping:
            return mapping[suffix]
        elif 'dockerfile' in name:
            return 'dockerfile'
        else:
            return 'text'

    def create_html(self):
        """Create the HTML file with all code files"""
        print(f"Creating HTML export: {self.output_file}")
        
        code_files = self.find_code_files()
        
        # HTML template with embedded CSS
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Code Repository Export - {self.root_dir.name}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        h2 {{
            color: #e74c3c;
            margin-top: 40px;
            padding: 15px;
            background-color: #f8f9fa;
            border-left: 5px solid #e74c3c;
            border-radius: 5px;
        }}
        .file-info {{
            background-color: #d4edda;
            padding: 10px 15px;
            border-radius: 5px;
            margin-bottom: 15px;
            color: #155724;
            font-size: 14px;
        }}
        .toc {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}
        .toc h2 {{
            margin-top: 0;
            color: #495057;
        }}
        .toc ul {{
            list-style-type: none;
            padding-left: 0;
        }}
        .toc li {{
            margin-bottom: 8px;
            padding: 8px;
            background-color: white;
            border-radius: 3px;
            border-left: 3px solid #3498db;
        }}
        .toc a {{
            text-decoration: none;
            color: #2c3e50;
            font-weight: 500;
        }}
        .toc a:hover {{
            color: #3498db;
        }}
        .file-type {{
            background-color: #3498db;
            color: white;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 12px;
            margin-left: 10px;
        }}
        pre {{
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 5px;
            padding: 15px;
            overflow-x: auto;
            font-family: 'Courier New', Courier, monospace;
            font-size: 13px;
            line-height: 1.4;
            margin: 15px 0;
        }}
        code {{
            background-color: #f8f9fa;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', Courier, monospace;
        }}
        .metadata {{
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 30px;
        }}
        .file-separator {{
            border: none;
            height: 2px;
            background: linear-gradient(to right, #3498db, #2c3e50);
            margin: 40px 0;
        }}
        @media print {{
            body {{ margin: 0; padding: 0; }}
            .container {{ box-shadow: none; border-radius: 0; }}
            h2 {{ page-break-before: always; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Code Repository Export</h1>
        
        <div class="metadata">
            <strong>Repository:</strong> {self.root_dir.name}<br>
            <strong>Export Date:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br>
            <strong>Total Files:</strong> {len(code_files)}<br>
            <strong>Root Directory:</strong> {html.escape(str(self.root_dir))}
        </div>
        
        <div class="toc">
            <h2>📋 Table of Contents</h2>
            <ul>
'''
        
        # Add table of contents
        for file_path in code_files:
            rel_path = file_path.relative_to(self.root_dir)
            file_type = self.get_file_type(file_path)
            file_id = str(rel_path).replace('/', '_').replace('\\', '_').replace('.', '_')
            html_content += f'''                <li>
                    <a href="#file_{file_id}">{html.escape(str(rel_path))}</a>
                    <span class="file-type">{file_type}</span>
                </li>
'''
        
        html_content += '''            </ul>
        </div>
'''
        
        # Add each file
        for i, file_path in enumerate(code_files):
            rel_path = file_path.relative_to(self.root_dir)
            file_type = self.get_file_type(file_path)
            file_id = str(rel_path).replace('/', '_').replace('\\', '_').replace('.', '_')
            
            print(f"Processing {i+1}/{len(code_files)}: {rel_path}")
            
            # File header
            html_content += f'''
        <h2 id="file_{file_id}">📄 {html.escape(str(rel_path))}</h2>
        
        <div class="file-info">
'''
            
            # File info
            try:
                file_stats = file_path.stat()
                file_size = file_stats.st_size
                modified_time = datetime.fromtimestamp(file_stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                html_content += f'''            <strong>Type:</strong> {file_type} | 
            <strong>Size:</strong> {file_size:,} bytes | 
            <strong>Modified:</strong> {modified_time}
'''
            except:
                html_content += f"            <strong>Type:</strong> {file_type}"
            
            html_content += '''        </div>
        
'''
            
            # File content
            content = self.read_file_content(file_path)
            language = self.get_language_for_highlight(file_path)
            
            # Escape HTML content
            escaped_content = html.escape(content)
            
            html_content += f'''        <pre><code class="language-{language}">{escaped_content}</code></pre>
'''
            
            # Add separator between files (except for the last file)
            if i < len(code_files) - 1:
                html_content += '''        <hr class="file-separator">
'''
        
        html_content += '''    </div>
    
    <!-- Optional: Add Prism.js for syntax highlighting -->
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism.min.css" rel="stylesheet" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-core.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
</body>
</html>'''
        
        # Write HTML file
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"✅ HTML created successfully: {self.output_file}")
            return True
        except Exception as e:
            print(f"❌ Error creating HTML: {str(e)}")
            return False

def main():
    parser = argparse.ArgumentParser(description="Export code files to HTML")
    parser.add_argument("--directory", "-d", default=".", help="Directory to scan (default: current directory)")
    parser.add_argument("--output", "-o", default="code_export.html", help="Output HTML filename")
    parser.add_argument("--preview", "-p", action="store_true", help="Preview files that would be included")
    
    args = parser.parse_args()
    
    # Convert to absolute path
    root_dir = Path(args.directory).resolve()
    
    if not root_dir.exists():
        print(f"❌ Directory not found: {root_dir}")
        return 1
    
    print(f"📁 Scanning directory: {root_dir}")
    
    exporter = SimpleCodeExporter(root_dir, args.output)
    
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
        return 0
    
    # Create HTML
    success = exporter.create_html()
    
    if success:
        output_path = Path(args.output).resolve()
        print(f"🌐 HTML saved to: {output_path}")
        
        # Show file size
        try:
            file_size = output_path.stat().st_size
            print(f"📊 HTML size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")
        except:
            pass
        
        print("\n💡 Tip: You can:")
        print("  1. Open the HTML file in a web browser")
        print("  2. Use browser's 'Print to PDF' feature to create a PDF")
        print("  3. Or install reportlab and use the PDF version: export_code_to_pdf.py")
        
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())
