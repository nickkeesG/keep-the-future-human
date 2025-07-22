from pathlib import Path
import yaml


def load_markdown(file_path: Path) -> str:
    """Load content from a markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def save_markdown(file_path: Path, content: str):
    """Save content to a markdown file"""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def concatenate_all_files(config_path: str = "config/settings.yaml") -> str:
    """Concatenate all source markdown files into one document"""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    source_dir = Path(config['directories']['source'])
    concatenated = ""
    
    for filename in config['source_files']:
        file_path = source_dir / filename
        if file_path.exists():
            content = load_markdown(file_path)
            concatenated += f"\n\n# {filename}\n\n{content}\n\n"
        else:
            print(f"Warning: File not found: {file_path}")
    
    return concatenated.strip()