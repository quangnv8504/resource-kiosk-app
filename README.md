# BE Face API

So khớp khuôn mặt (InsightFace + ONNX Runtime). Port mặc định: **8001**.

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

## Docker (production)

Build image **một lần** trên máy có source + model, đẩy lên registry; các máy khác chỉ `pull` và chạy (không cần source, Python hay model).

### 1. Build (máy build)

Cần có `models\buffalo_l\det_10g.onnx` và `w600k_r50.onnx` (xem phần "Chạy dev" để tải model).

```powershell
.\scripts\docker-build.bat 1.0.0
```

Tạo image `be-face-v1:1.0.0` và `be-face-v1:latest` (linux/amd64, đã gồm model).

### 2. Đẩy lên registry (máy build)

Đăng nhập registry trước, rồi push:

```powershell
# Docker Hub
docker login
.\scripts\docker-push.bat <username>/be-face-v1 1.0.0

# GitHub Container Registry
docker login ghcr.io
.\scripts\docker-push.bat ghcr.io/<org>/be-face-v1 1.0.0

# Registry riêng của công ty
docker login registry.company.com
.\scripts\docker-push.bat registry.company.com/<team>/be-face-v1 1.0.0
```

### 3. Chạy trên máy khác

Chỉ cần Docker và file `docker-compose.prod.yml`. Tạo file `.env` cạnh nó:

```env
BE_FACE_IMAGE=<username>/be-face-v1:1.0.0
CORS_ORIGINS=https://fe.example.com
HOST_PORT=8001
```

```bash
docker login                     # nếu registry/repo là private
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

Hoặc không dùng compose:

```bash
docker run -d --name be-face-v1 --restart unless-stopped -p 8001:8001 \
  -e CORS_ORIGINS="https://fe.example.com" <username>/be-face-v1:1.0.0
```

Cập nhật bản mới: build + push tag mới, trên máy chạy đổi `BE_FACE_IMAGE` rồi `pull` + `up -d`.

### Chạy thử Docker trên máy dev

```powershell
docker compose up -d --build
```

### Biến môi trường

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `PORT` | `8001` | Port server bên trong container |
| `CORS_ORIGINS` | `*` | Danh sách domain FE, cách nhau bởi dấu phẩy |
| `MAX_CONTENT_LENGTH_MB` | `10` | Giới hạn kích thước body request (MB) |
| `BE_FACE_IMAGE` | `be-face-v1:latest` | Image dùng trong `docker-compose.prod.yml` |
| `HOST_PORT` | `8001` | Port mở ra máy host trong `docker-compose.prod.yml` |

## API

- `GET http://127.0.0.1:8001/health`
- `POST http://127.0.0.1:8001/api/v1/compare` — JSON `{ "image1": "<base64>", "image2": "<base64>" }`
