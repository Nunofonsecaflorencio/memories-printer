from exif import Image as EXIFImage
from PIL import Image
from pathlib import Path

def read_image(image_path):
    with open(image_path, "rb") as f:
        metadata = EXIFImage(f)
        
    image = Image.open(image_path)
    try:
        if metadata.get("orientation"):
            return fix_orientation(image, metadata.get("orientation"))
    except:
        pass
    
    return image

 
def fix_orientation(image: Image, orientation: int) -> Image:
    operations = {
        2: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT),
        3: lambda img: img.rotate(180, expand=True),
        4: lambda img: img.transpose(Image.FLIP_TOP_BOTTOM),
        5: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).rotate(90, expand=True),
        6: lambda img: img.rotate(270, expand=True),
        7: lambda img: img.transpose(Image.FLIP_LEFT_RIGHT).rotate(270, expand=True),
        8: lambda img: img.rotate(90, expand=True),
    }
    return operations.get(orientation, lambda x: x)(image)