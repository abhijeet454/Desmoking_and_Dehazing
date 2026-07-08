# ClearVision AI - Enterprise Desmoking & Dehazing Service

ClearVision AI is a production-grade machine learning platform for image desmoking and dehazing. Originally based on a PyTorch research notebook, it has been refactored into a scalable, full-stack application following Clean Architecture principles.

## Features

- **Advanced ML Model**: Uses a custom U-Net architecture trained on the NH-HAZE dataset for superior dehazing performance.
- **FastAPI Backend**: Robust, asynchronous Python API for handling inference requests.
- **Next.js Frontend**: Modern, responsive React application with drag-and-drop support and before/after comparison UI.
- **Comprehensive Testing**: Includes `pytest` suites for API reliability.
- **Clean Codebase**: Strictly separated concerns (ML Core, API, Web).

## Quick Start

### 1. Backend (FastAPI + PyTorch)

Ensure you have Python 3.10+ installed.

```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn src.api.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`. Swagger documentation is auto-generated at `/docs`.

### 2. Frontend (Next.js)

Ensure you have Node.js 18+ installed.

```bash
cd src/web

# Install dependencies
npm install

# Run the development server
npm run dev
```
The Web UI will be available at `http://localhost:3000`.

### 3. Model Training (Optional)

To retrain the PyTorch model from scratch:

```bash
python src/ml/train.py --data_dir /path/to/dataset --batch_size 4 --num_epochs 50
```

## Testing

Run the test suite using `pytest`:

```bash
pytest src/api/test_main.py -v
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design decisions and module boundaries.
