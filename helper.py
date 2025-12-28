from exif import Image as EXIFImage
from PIL import Image
from pathlib import Path
from datetime import datetime
from fractions import Fraction

def read_image(image_path):
    with open(image_path, "rb") as f:
        metadata = EXIFImage(f)
        
    image = Image.open(image_path)
    
    try:
        text = get_caption(metadata)
        if metadata.get("orientation"):
            return fix_orientation(image, metadata.get("orientation")), text
    except:
        pass
    
    try:
        if metadata.get("orientation"):
            return fix_orientation(image, metadata.get("orientation")), None
    except:
        pass
    
    return image, None

def get_caption(metadata) -> str:
    caption = str()
    dt_value = metadata.get("datetime_original")
    if dt_value:
        caption += format_datetime(dt_value) + "\n"
    iso = metadata.get("photographic_sensitivity")
    f_number = metadata.get("f_number") or metadata.get("aperture_value")
    exposure = metadata.get("exposure_time")
    if iso and f_number and exposure:
        caption += f"ISO {iso}, f{f_number}, {format_exposure(exposure)}"
    return caption

def format_datetime(date_str: str) -> str:
    dt = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
    return dt.strftime("%A, %d/%m/%Y %H:%M")


def format_exposure(exposure) -> str:
    if isinstance(exposure, float):
        frac = Fraction(exposure).limit_denominator(1000)
        return f"{frac.numerator}/{frac.denominator}"
    return str(exposure)


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