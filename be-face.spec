# -*- mode: python ; coding: utf-8 -*-
# Onefile: dist\be-face.exe (InsightFace + ONNX Runtime, không TensorFlow)

import os

from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

_project_dir = os.path.abspath(SPECPATH)
_models_src = os.path.join(_project_dir, "models", "buffalo_l")
_model_files = []
if os.path.isdir(_models_src):
    for name in ("det_10g.onnx", "w600k_r50.onnx"):
        path = os.path.join(_models_src, name)
        if os.path.isfile(path):
            _model_files.append(
                (path, os.path.join("insightface", "models", "buffalo_l"))
            )

datas = list(_model_files)
binaries = []
hiddenimports = collect_submodules("insightface") + collect_submodules("flask") + collect_submodules("werkzeug")
hiddenimports += [
    "onnxruntime",
    "onnxruntime.capi",
    "onnxruntime.capi._pybind_state",
    "onnxruntime.capi.onnxruntime_pybind11_state",
]
hiddenimports += [
    "src",
    "src.main",
    "src.api.pace_api",
    "src.services.face_compare",
    "src.exceptions",
    "src.exceptions.handlers",
    "src.exceptions.errors",
    "src.models.response_model",
    "src.utils.image_utils",
    "flask_cors",
    "waitress",
    "cv2",
    "numpy",
    "PIL",
    "onnx",
]

tmp = collect_all("insightface")
datas += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]

try:
    import onnxruntime as _ort

    _ort_capi = os.path.join(os.path.dirname(_ort.__file__), "capi")
    for _name in os.listdir(_ort_capi):
        if _name.endswith((".dll", ".pyd")):
            binaries.append((os.path.join(_ort_capi, _name), "onnxruntime/capi"))
except Exception:
    pass

a = Analysis(
    ["run_server.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["hooks/rth_onnxruntime_dll.py"],
    excludes=[
        "matplotlib",
        "tkinter",
        "tensorflow",
        "tf_keras",
        "keras",
        "deepface",
        "torch",
        "torchvision",
        "tensorboard",
        "pandas",
        "scipy",
        "sklearn",
        "skimage",
        "sympy",
        "gdown",
        "tqdm",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="be-face",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
