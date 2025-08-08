# Code Export Tools

This directory contains tools to export all typed code files from your repository into a PDF or HTML document. The tools will include Python files, YAML configs, Jupyter notebooks, JavaScript, CSS, HTML, and other code files while excluding data directories and binary files.

## Available Tools

### 1. HTML Export (No Dependencies Required) ⭐ **RECOMMENDED**
**File:** `export_code_to_html.py`

This tool creates a beautiful HTML document with syntax highlighting and doesn't require any external dependencies.

```bash
# Preview files that would be included
python export_code_to_html.py --preview

# Export to HTML (default: code_export.html)
python export_code_to_html.py

# Export to custom filename
python export_code_to_html.py --output my_code.html

# Export from different directory
python export_code_to_html.py --directory /path/to/project --output project_code.html
```

**Features:**
- ✅ No external dependencies required
- ✅ Beautiful syntax highlighting using Prism.js
- ✅ Table of contents with file links
- ✅ File metadata (size, modification date)
- ✅ Responsive design
- ✅ Can be printed to PDF from browser

### 2. PDF Export (Requires ReportLab)
**File:** `export_code_to_pdf.py`

This tool creates a professional PDF document directly.

#### Installation
First install the required dependency:

```bash
# Windows
install_dependencies.bat

# Or manually
pip install reportlab
```

#### Usage
```bash
# Preview files that would be included
python export_code_to_pdf.py --preview

# Export to PDF (default: code_export.pdf)
python export_code_to_pdf.py

# Export to custom filename
python export_code_to_pdf.py --output my_code.pdf

# Export from different directory
python export_code_to_pdf.py --directory /path/to/project --output project_code.pdf
```

## What Files Are Included

The tools automatically detect and include:

### Code Files
- **Python:** `.py` files
- **YAML:** `.yml`, `.yaml` files
- **Jupyter Notebooks:** `.ipynb` files
- **Web:** `.html`, `.css`, `.js`, `.ts`, `.jsx`, `.tsx` files
- **Config:** `.json`, `.toml`, `.ini`, `.cfg`, `.conf` files
- **Scripts:** `.sh`, `.bat`, `.ps1` files
- **Data:** `.sql`, `.xml` files
- **Documentation:** `.md` files

### Special Files
- `Dockerfile`
- `Makefile`
- `requirements.txt`
- `setup.py`
- `pyproject.toml`
- `.gitignore`
- `.env`

## What Files Are Excluded

The tools automatically exclude:

- **Data directories:** `data/`, `logs/`, `checkpts/`
- **Cache directories:** `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`
- **Build directories:** `build/`, `dist/`, `*.egg-info/`
- **Version control:** `.git/`
- **IDE files:** `.vscode/`
- **Dependencies:** `node_modules/`
- **Notebook checkpoints:** `.ipynb_checkpoints/`

## Output Features

### HTML Export
- Clean, professional layout
- Syntax highlighting for all supported languages
- Table of contents with clickable links
- File metadata (type, size, last modified)
- Print-friendly CSS (can be printed to PDF)
- Responsive design for different screen sizes

### PDF Export
- Professional PDF layout
- Monospace font for code readability
- Table of contents
- File headers with metadata
- Page breaks between files
- Proper text encoding handling

## Tips

1. **For PDF from HTML:** Open the HTML file in a browser and use "Print to PDF"
2. **Large repositories:** Use `--preview` first to see what will be included
3. **Custom filtering:** Edit the `exclude_patterns` in the script to customize what gets excluded
4. **Memory usage:** For very large codebases, the tools automatically chunk content to prevent memory issues

## Examples

```bash
# Quick preview of your current project
python export_code_to_html.py --preview

# Export current project to HTML
python export_code_to_html.py --output bana_tts_code.html

# Export to PDF (after installing reportlab)
python export_code_to_pdf.py --output bana_tts_code.pdf
```

## File Structure in Export

The exported document will contain:
1. **Title page** with repository metadata
2. **Table of contents** listing all files
3. **File sections** with:
   - File path and type
   - File size and modification date
   - Complete file content with syntax highlighting

## Troubleshooting

### HTML Export Issues
- If the file is very large, some browsers might be slow to load
- For better syntax highlighting, ensure internet connection (uses CDN)

### PDF Export Issues
- Install reportlab: `pip install reportlab`
- For encoding issues, the tool tries multiple encodings automatically
- Large files are automatically chunked to prevent memory issues

### General Issues
- Use `--preview` to check what files will be included
- Check file permissions if you get access errors
- For very large repositories, consider excluding additional directories

## Customization

You can modify the scripts to:
- Change included/excluded file types
- Modify the styling (HTML version)
- Adjust PDF layout and fonts
- Add custom headers or footers
