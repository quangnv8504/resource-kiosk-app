"""Thêm thư mục DLL ONNX Runtime vào search path khi chạy exe (Windows, onefile)."""
import os
import sys

if getattr(sys, "frozen", False):
    os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")
    os.environ.setdefault("OMP_NUM_THREADS", "1")

    base = getattr(sys, "_MEIPASS", "")
    if base:
        for sub in ("onnxruntime/capi", "onnxruntime"):
            dll_dir = os.path.normpath(os.path.join(base, *sub.split("/")))
            if not os.path.isdir(dll_dir):
                continue
            if hasattr(os, "add_dll_directory"):
                os.add_dll_directory(dll_dir)
            os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")
