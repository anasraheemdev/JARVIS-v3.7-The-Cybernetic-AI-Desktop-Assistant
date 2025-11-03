"""
Code Development Module
Handles VS Code integration, code generation, Git automation, and project templates
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Dict, Optional, List
import json

logger = logging.getLogger(__name__)

# Git automation
try:
    from git import Repo, Git
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False
    logger.warning("GitPython not installed. Git automation will be limited.")

class CodeModule:
    """Handles code development operations"""
    
    def __init__(self, memory_module=None):
        self.memory_module = memory_module
        self.home_dir = Path(os.path.expanduser('~'))
        
        # Common IDE paths (Windows)
        self.vscode_paths = [
            r"C:\Users\{}\AppData\Local\Programs\Microsoft VS Code\Code.exe".format(os.getenv('USERNAME', '')),
            r"C:\Program Files\Microsoft VS Code\Code.exe",
            r"C:\Program Files (x86)\Microsoft VS Code\Code.exe",
        ]
    
    def open_vscode(self, path: Optional[str] = None) -> str:
        """Open VS Code, optionally with a specific file or folder"""
        try:
            # Find VS Code executable
            vscode_exe = None
            for path_option in self.vscode_paths:
                if os.path.exists(path_option):
                    vscode_exe = path_option
                    break
            
            if not vscode_exe:
                # Try to find it via 'code' command
                try:
                    subprocess.run(['code', '--version'], check=True, capture_output=True)
                    vscode_exe = 'code'
                except:
                    return "VS Code not found. Please install VS Code or add it to PATH."
            
            # Open VS Code
            if path:
                target_path = Path(path).expanduser().resolve()
                if target_path.exists():
                    subprocess.Popen([vscode_exe, str(target_path)])
                    return f"Opened VS Code with {target_path}"
                else:
                    # Create file/folder if it doesn't exist
                    if path.endswith('/') or not os.path.splitext(path)[1]:
                        # It's a folder
                        target_path.mkdir(parents=True, exist_ok=True)
                    else:
                        # It's a file
                        target_path.parent.mkdir(parents=True, exist_ok=True)
                        target_path.touch()
                    subprocess.Popen([vscode_exe, str(target_path)])
                    return f"Created and opened {target_path} in VS Code"
            else:
                subprocess.Popen([vscode_exe])
                return "Opened VS Code"
        
        except Exception as e:
            logger.error(f"Error opening VS Code: {e}")
            return f"Error opening VS Code: {e}"
    
    def create_file(self, file_path: str, content: str = "", language: str = "text") -> str:
        """Create a new file with optional content"""
        try:
            target_path = Path(file_path).expanduser().resolve()
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Log action
            if self.memory_module:
                self.memory_module.log_activity('file_created', {
                    'file_path': str(target_path),
                    'language': language
                })
            
            return f"Created file: {target_path}"
        
        except Exception as e:
            logger.error(f"Error creating file: {e}")
            return f"Error creating file: {e}"
    
    def generate_code(self, prompt: str, language: str = "python") -> str:
        """Generate code using Groq AI (requires GroqAgent integration)"""
        # This will be called from groq_agent with a specific prompt
        # Return placeholder for now - actual implementation in groq_agent
        return f"Code generation for {language} requested: {prompt}"
    
    def git_operation(self, params: Dict) -> str:
        """Perform Git operations (commit, push, pull, status)"""
        if not GIT_AVAILABLE:
            return "GitPython not installed. Install with: pip install GitPython"
        
        try:
            operation = params.get('operation', 'status')  # commit, push, pull, status, init
            repo_path = params.get('path', os.getcwd())
            message = params.get('message', '')
            
            repo_path = Path(repo_path).expanduser().resolve()
            
            if operation == 'init':
                if not repo_path.exists():
                    repo_path.mkdir(parents=True, exist_ok=True)
                Repo.init(str(repo_path))
                return f"Initialized Git repository at {repo_path}"
            
            # Check if it's a git repo
            try:
                repo = Repo(str(repo_path))
            except:
                return f"Not a Git repository: {repo_path}"
            
            if operation == 'status':
                status = repo.git.status()
                return f"Git Status:\n{status}"
            
            elif operation == 'commit':
                if not message:
                    return "Error: Commit message required"
                repo.git.add(all=True)
                repo.index.commit(message)
                if self.memory_module:
                    self.memory_module.log_activity('git_commit', {
                        'repo_path': str(repo_path),
                        'message': message
                    })
                return f"Committed changes: {message}"
            
            elif operation == 'push':
                origin = repo.remote('origin')
                if not origin:
                    return "No remote 'origin' configured"
                origin.push()
                return "Pushed changes to remote"
            
            elif operation == 'pull':
                origin = repo.remote('origin')
                if not origin:
                    return "No remote 'origin' configured"
                origin.pull()
                return "Pulled latest changes from remote"
            
            else:
                return f"Unknown Git operation: {operation}"
        
        except Exception as e:
            logger.error(f"Error in Git operation: {e}")
            return f"Git operation failed: {e}"
    
    def create_project_template(self, params: Dict) -> str:
        """Create a project from a template (Flask, React, etc.)"""
        try:
            project_type = params.get('type', 'flask')  # flask, react, node, python
            project_name = params.get('name', 'my-project')
            target_dir = params.get('directory', self.home_dir / 'Desktop' / project_name)
            
            target_dir = Path(target_dir).expanduser().resolve()
            target_dir.mkdir(parents=True, exist_ok=True)
            
            if project_type.lower() == 'flask':
                # Create Flask project structure
                (target_dir / 'app.py').write_text("""from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'

if __name__ == '__main__':
    app.run(debug=True)
""")
                (target_dir / 'requirements.txt').write_text("Flask==3.0.0\n")
                (target_dir / '.gitignore').write_text("venv/\n__pycache__/\n*.pyc\n.env\n")
                (target_dir / 'README.md').write_text(f"# {project_name}\n\nFlask application\n")
                
                # Initialize Git
                if GIT_AVAILABLE:
                    Repo.init(str(target_dir))
                
                return f"Created Flask project '{project_name}' at {target_dir}"
            
            elif project_type.lower() == 'react':
                # Create basic React structure (requires npm/node)
                (target_dir / 'package.json').write_text(json.dumps({
                    "name": project_name,
                    "version": "1.0.0",
                    "scripts": {
                        "start": "react-scripts start"
                    },
                    "dependencies": {
                        "react": "^18.2.0",
                        "react-dom": "^18.2.0",
                        "react-scripts": "5.0.1"
                    }
                }, indent=2))
                (target_dir / 'README.md').write_text(f"# {project_name}\n\nReact application\n")
                return f"Created React project '{project_name}' at {target_dir}. Run 'npm install' to install dependencies."
            
            elif project_type.lower() == 'python':
                # Simple Python project
                (target_dir / 'main.py').write_text(f"# {project_name}\n\nif __name__ == '__main__':\n    print('Hello, World!')\n")
                (target_dir / 'README.md').write_text(f"# {project_name}\n\nPython project\n")
                return f"Created Python project '{project_name}' at {target_dir}"
            
            else:
                return f"Unknown project type: {project_type}. Supported: flask, react, python"
        
        except Exception as e:
            logger.error(f"Error creating project template: {e}")
            return f"Error creating project: {e}"
    
    def run_terminal_command(self, params: Dict) -> str:
        """Run a terminal command (with safety checks)"""
        try:
            command = params.get('command', '')
            confirm = params.get('confirm', True)  # Should ask confirmation for dangerous commands
            
            if not command:
                return "Error: No command provided"
            
            # List of potentially dangerous commands (Windows)
            dangerous_commands = ['format', 'del /f', 'rmdir /s', 'rm -rf', 'sudo', 'mkfs']
            
            if confirm and any(cmd in command.lower() for cmd in dangerous_commands):
                return f"⚠️ WARNING: Potentially dangerous command detected. For safety, this command requires manual confirmation: {command}"
            
            # Run command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,
                cwd=params.get('working_dir', os.getcwd())
            )
            
            output = result.stdout + result.stderr
            
            if self.memory_module:
                self.memory_module.log_activity('command_executed', {
                    'command': command,
                    'success': result.returncode == 0
                })
            
            if result.returncode == 0:
                return f"Command executed successfully:\n{output}"
            else:
                return f"Command failed (exit code {result.returncode}):\n{output}"
        
        except subprocess.TimeoutExpired:
            return "Command timed out after 30 seconds"
        except Exception as e:
            logger.error(f"Error running command: {e}")
            return f"Error running command: {e}"

