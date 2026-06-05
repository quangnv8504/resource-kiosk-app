import base64
import binascii
import re

import cv2
import numpy as np

_DATA_URI_PREFIX = re.compile(r"^data:image/[a-zA-Z0-9.+-]+;base64,")


def base64_to_bgr(value: str, field_name: str = "image") -> np.ndarray:
    if value is None or not isinstance(value, str):
        raise ValueError(f"{field_name} phải là chuỗi base64.")

    text = value.strip()
    if not text:
        raise ValueError(f"Thiếu {field_name} (base64).")

    raw = _DATA_URI_PREFIX.sub("", text)

    try:
        data = base64.b64decode(raw, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise ValueError(f"{field_name} không phải chuỗi base64 hợp lệ.") from exc

    if not data:
        raise ValueError(f"{field_name} rỗng.")

    arr = np.frombuffer(data, dtype=np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Không decode được {field_name}. Gửi JPG/PNG base64 hợp lệ.")
    return image
