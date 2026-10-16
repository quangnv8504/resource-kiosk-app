import base64
import binascii
import io
import re

import cv2
import numpy as np
from PIL import Image

_DATA_URI_PREFIX = re.compile(r"^data:image/[a-zA-Z0-9.+-]+;base64,")
_WHITESPACE = re.compile(r"\s+")

# Chặn ảnh "bom giải nén": file nhỏ nhưng bung ra rất nhiều pixel
MAX_PIXELS = 100_000_000
# Detector đã resize về 640, ảnh lớn hơn mức này chỉ tốn RAM/CPU
MAX_SIDE = 1920

_REDUCED_FLAGS = (
    (8, cv2.IMREAD_REDUCED_COLOR_8),
    (4, cv2.IMREAD_REDUCED_COLOR_4),
    (2, cv2.IMREAD_REDUCED_COLOR_2),
)


def _image_size(data: bytes, field_name: str) -> tuple[int, int]:
    try:
        with Image.open(io.BytesIO(data)) as img:
            return img.size
    except Image.DecompressionBombError as exc:
        raise ValueError(f"{field_name} có độ phân giải quá lớn.") from exc
    except Exception as exc:
        raise ValueError(
            f"Không đọc được {field_name}. Vui lòng gửi ảnh JPG/PNG dạng base64 hợp lệ."
        ) from exc


def base64_to_bgr(value: str, field_name: str = "image") -> np.ndarray:
    if value is None or not isinstance(value, str):
        raise ValueError(f"{field_name} phải là chuỗi base64.")

    text = value.strip()
    if not text:
        raise ValueError(f"Thiếu {field_name} (base64).")

    raw = _WHITESPACE.sub("", _DATA_URI_PREFIX.sub("", text))

    try:
        data = base64.b64decode(raw, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError(f"{field_name} không phải chuỗi base64 hợp lệ.") from exc

    if not data:
        raise ValueError(f"{field_name} rỗng.")

    width, height = _image_size(data, field_name)
    if width * height > MAX_PIXELS:
        raise ValueError(
            f"{field_name} có độ phân giải quá lớn ({width}x{height}). "
            f"Tối đa {MAX_PIXELS // 1_000_000} megapixel."
        )

    flag = cv2.IMREAD_COLOR
    longest = max(width, height)
    for factor, reduced_flag in _REDUCED_FLAGS:
        if longest // factor >= MAX_SIDE:
            flag = reduced_flag
            break

    arr = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(arr, flag)
    if image is None:
        raise ValueError(
            f"Không đọc được {field_name}. Vui lòng gửi ảnh JPG/PNG dạng base64 hợp lệ."
        )

    h, w = image.shape[:2]
    if max(h, w) > MAX_SIDE:
        scale = MAX_SIDE / max(h, w)
        image = cv2.resize(
            image, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_AREA
        )
    return image
