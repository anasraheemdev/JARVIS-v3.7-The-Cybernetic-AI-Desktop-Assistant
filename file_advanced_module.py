"""
Advanced File Management Module
Handles content-based search, duplicate finding, batch operations, image/PDF processing
"""

import os
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional
import shutil
from datetime import datetime

logger = logging.getLogger(__name__)

# Image processing
try:
    from PIL import Image
    IMAGE_AVAILABLE = True
except ImportError:
    IMAGE_AVAILABLE = False
    logger.warning("PIL not installed. Image processing will be limited.")

# PDF processing
try:
    import PyPDF2
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    logger.warning("PyPDF2 not installed. PDF operations will be limited.")

class AdvancedFileModule:
    """Handles advanced file operations"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.home_dir = Path(os.path.expanduser('~'))
    
    def search_file_content(self, params: Dict) -> str:
        """Search for text content in files"""
        try:
            search_text = params.get('text', '').lower()
            directory = params.get('directory', str(self.home_dir))
            file_extensions = params.get('extensions', ['.txt', '.md', '.py', '.js', '.html', '.css'])
            
            if not search_text:
                return "Error: Search text required"
            
            directory = Path(directory).expanduser().resolve()
            if not directory.exists():
                return f"Directory not found: {directory}"
            
            matches = []
            for ext in file_extensions:
                for file_path in directory.rglob(f'*{ext}'):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if search_text in content:
                                matches.append(str(file_path))
                    except:
                        continue
            
            if matches:
                result = f"Found {len(matches)} files containing '{search_text}':\n"
                result += "\n".join(matches[:20])  # Limit to 20 results
                if len(matches) > 20:
                    result += f"\n... and {len(matches) - 20} more"
                return result
            else:
                return f"No files found containing '{search_text}'"
        
        except Exception as e:
            logger.error(f"Error searching file content: {e}")
            return f"Error: {e}"
    
    def find_duplicate_files(self, params: Dict) -> str:
        """Find duplicate files by content hash"""
        try:
            directory = params.get('directory', str(self.home_dir / 'Downloads'))
            directory = Path(directory).expanduser().resolve()
            
            if not directory.exists():
                return f"Directory not found: {directory}"
            
            file_hashes = {}
            duplicates = []
            
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    try:
                        # Calculate MD5 hash
                        hash_md5 = hashlib.md5()
                        with open(file_path, "rb") as f:
                            for chunk in iter(lambda: f.read(4096), b""):
                                hash_md5.update(chunk)
                        file_hash = hash_md5.hexdigest()
                        
                        if file_hash in file_hashes:
                            duplicates.append({
                                'original': str(file_hashes[file_hash]),
                                'duplicate': str(file_path)
                            })
                        else:
                            file_hashes[file_hash] = file_path
                    except:
                        continue
            
            if duplicates:
                result = f"Found {len(duplicates)} duplicate files:\n"
                for dup in duplicates[:10]:  # Limit to 10
                    result += f"\nDuplicate: {dup['duplicate']}\nOriginal: {dup['original']}\n"
                return result
            else:
                return "No duplicate files found"
        
        except Exception as e:
            logger.error(f"Error finding duplicates: {e}")
            return f"Error: {e}"
    
    def batch_rename_files(self, params: Dict) -> str:
        """Batch rename files with pattern"""
        try:
            directory = params.get('directory', str(self.home_dir / 'Desktop'))
            pattern = params.get('pattern', 'file_{}.{}')  # {n} for number, {e} for extension
            prefix = params.get('prefix', 'renamed_')
            
            directory = Path(directory).expanduser().resolve()
            if not directory.exists():
                return f"Directory not found: {directory}"
            
            files = [f for f in directory.iterdir() if f.is_file()]
            renamed_count = 0
            
            for idx, file_path in enumerate(files, 1):
                ext = file_path.suffix
                new_name = pattern.format(idx, ext.lstrip('.'))
                if '{n}' in pattern:
                    new_name = new_name.replace('{n}', str(idx))
                if '{e}' in pattern:
                    new_name = new_name.replace('{e}', ext.lstrip('.'))
                
                new_path = directory / new_name
                if new_path != file_path:
                    file_path.rename(new_path)
                    renamed_count += 1
            
            return f"Renamed {renamed_count} files"
        
        except Exception as e:
            logger.error(f"Error batch renaming: {e}")
            return f"Error: {e}"
    
    def compress_image(self, params: Dict) -> str:
        """Compress an image file"""
        if not IMAGE_AVAILABLE:
            return "Image processing not available. Install Pillow: pip install Pillow"
        
        try:
            image_path = params.get('path', '')
            quality = params.get('quality', 85)  # 0-100
            
            image_path = Path(image_path).expanduser().resolve()
            if not image_path.exists():
                return f"Image not found: {image_path}"
            
            img = Image.open(image_path)
            
            # Save compressed version
            output_path = image_path.parent / f"{image_path.stem}_compressed{image_path.suffix}"
            img.save(output_path, optimize=True, quality=quality)
            
            # Compare sizes
            original_size = image_path.stat().st_size
            compressed_size = output_path.stat().st_size
            savings = round((1 - compressed_size / original_size) * 100, 2)
            
            return f"Compressed image: {output_path}\nSize reduction: {savings}%"
        
        except Exception as e:
            logger.error(f"Error compressing image: {e}")
            return f"Error: {e}"
    
    def merge_pdfs(self, params: Dict) -> str:
        """Merge multiple PDF files"""
        if not PDF_AVAILABLE:
            return "PDF processing not available. Install PyPDF2: pip install PyPDF2"
        
        try:
            pdf_files = params.get('files', [])
            output_path = params.get('output', str(self.home_dir / 'Desktop' / 'merged.pdf'))
            
            if not pdf_files or len(pdf_files) < 2:
                return "Error: At least 2 PDF files required"
            
            output_path = Path(output_path).expanduser().resolve()
            merger = PyPDF2.PdfMerger()
            
            for pdf_file in pdf_files:
                pdf_path = Path(pdf_file).expanduser().resolve()
                if pdf_path.exists():
                    merger.append(str(pdf_path))
                else:
                    return f"PDF not found: {pdf_path}"
            
            merger.write(str(output_path))
            merger.close()
            
            return f"Merged {len(pdf_files)} PDFs into: {output_path}"
        
        except Exception as e:
            logger.error(f"Error merging PDFs: {e}")
            return f"Error: {e}"

