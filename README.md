# BE Face API

So khớp khuôn mặt (InsightFace + ONNX Runtime). Port mặc định: **8000**.

## Chạy dev (Python)

```powershell
py -3.11 -m venv venv
.\venv\Scripts\pip install -r requirements.txt
.\scripts\prepare_models.bat
.\run.bat
```

Lần đầu nếu chưa có model `buffalo_l`, chạy trong venv:

```powershell
.\venv\Scripts\python -c "from insightface.app import FaceAnalysis; FaceAnalysis(name='buffalo_l').prepare(ctx_id=-1)"
```

Sau đó chạy lại `prepare_models.bat` để copy ONNX vào `models\buffalo_l\`.

## Build exe (một file)

```powershell
.\build.bat
```

Output: **`dist\be-face.exe`** (onefile, gồm model ONNX).

## Chạy exe (sau build)

```powershell
.\dist-run.bat
```

## API

- `GET http://127.0.0.1:8000/health`
- `POST http://127.0.0.1:8000/api/v1/compare` — JSON `{ "image1": "<base64>", "image2": "<base64>" }`
