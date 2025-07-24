from pathlib import Path
from typing import List, Dict

def list_images_by_ean(ean: str, base_url: str) -> Dict[str, List[str]]:
    """
    Returns a dict with lists of full image URLs for input and output directories for a given EAN.
    """
    base_dir = Path("static") / ean
    input_dir = base_dir / "input"
    output_dir = base_dir / "output"

    def get_files(directory: Path, subfolder: str) -> List[str]:
        if not directory.exists() or not directory.is_dir():
            return []
        return [
            f"{base_url}static/{ean}/{subfolder}/{f.name}"
            for f in directory.iterdir() if f.is_file()
        ]

    return {
        "input": get_files(input_dir, "input"),
        "output": get_files(output_dir, "output")
    }
