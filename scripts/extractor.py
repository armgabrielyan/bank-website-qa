import json
from pathlib import Path
from PIL import Image
import pytesseract

class RawContent:
    def __init__(self, folder_path):
        self.folder_path = Path(folder_path)
        self.metadata_path = self.folder_path / "metadata.json"
        self.webpages_path = self.folder_path / "webpages"
        self.extracted_path = self.folder_path.parent.parent / "extracted" / self.folder_path.name
        self.extracted_path.mkdir(parents=True, exist_ok=True)

    def extract_metadata(self):
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r') as f:
                metadata = json.load(f)
            with open(self.extracted_path / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=4)

    def extract_text_from_images(self):
        if self.webpages_path.exists():
            text = ""
            for image_file in self.webpages_path.glob("*.png"):
                text += self._extract_text_from_image(image_file)
            output_file = self.extracted_path / "data.txt"
            with open(output_file, 'w') as f:
                f.write(text)

    @staticmethod
    def _extract_text_from_image(image_path):
        try:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image)
        except Exception as e:
            return f"Error extracting text from {image_path}: {e}"

    def extract(self):
        self.extract_metadata()
        self.extract_text_from_images()

def process_all_raw_folders(base_path):
    raw_path = Path(base_path) / "data" / "raw"
    for raw_folder in raw_path.iterdir():
        if raw_folder.is_dir():
            print(f"Processing folder: {raw_folder}")
            raw_content = RawContent(raw_folder)
            raw_content.extract()

if __name__ == "__main__":
    base_directory = "./"
    process_all_raw_folders(base_directory)
