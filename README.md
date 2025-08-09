# Gemini OCR (Streamlit App)

A Streamlit web app that extracts text from receipt images using the Gemini Generative Language API. The app uploads an image, sends it to the API as base64, and displays the extracted OCR text in a structured way.

## Features
- Upload receipt images (PNG, JPG, JPEG)  
- Send images to the Gemini API as base64 inline data  
- Display the uploaded image and extracted text  
- Simple UI with custom CSS styling  
- Docker-ready for easy deployment

## Requirements
- Docker (if using Docker)  
- Python 3.8+ (if running locally without Docker)  
- Internet access to call the Gemini API  
- API key for Google Generative Language API (Gemini)  
- Python packages listed in `requirements.txt`

## Repository Files (example)
- `app.py` — main Streamlit application  
- `Dockerfile` — Docker image build instructions  
- `requirements.txt` — dependency list  
- `README.md` — this file  
- `.gitignore`  

## Installation (Local, without Docker)
1. Clone the repository:
   ```
   git clone <YOUR_REPO_URL>
   cd <YOUR_REPO_FOLDER>
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Provide your API key (options):
   - Set environment variable and update `app.py` to read it:
     ```python
     import os
     API_KEY = os.getenv("GEMINI_API_KEY", "")
     ```
   - Or paste API key into `API_KEY` in `app.py` (not recommended for public repos).

5. Run the app:
   ```
   streamlit run app.py
   ```

6. Open http://localhost:8501 and use the sidebar to upload a receipt image, then click "Jalankan OCR".

## Docker Usage
This repo includes a Dockerfile optimized for a lightweight Python 3.9-slim image, installs system dependencies required by Pillow (libjpeg, zlib), installs Python packages from `requirements.txt`, and runs Streamlit on port 8501.

Example Dockerfile (as included):
```
FROM python:3.9-slim
WORKDIR /app
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.enableCORS=false", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build the Docker image:
```
docker build -t gemini-ocr:latest .
```

Run the container (recommended: pass API key via environment variable and map port):
```
docker run -d \
  -p 8501:8501 \
  -e GEMINI_API_KEY="your_real_api_key_here" \
  --name gemini-ocr \
  gemini-ocr:latest
```

Notes:
- The included `Dockerfile` runs `app.py` directly. If you change `app.py` to read `GEMINI_API_KEY` from the environment (recommended), pass it with `-e GEMINI_API_KEY=...` as shown above.
- If you bind-mount local code for development:
  ```
  docker run -it --rm -p 8501:8501 -v $(pwd):/app -e GEMINI_API_KEY="..." gemini-ocr:latest
  ```

## Environment variable handling (recommended)
Modify `app.py` to read the API key from an environment variable and fall back to existing behavior:
```python
import os
API_KEY = os.getenv("GEMINI_API_KEY", "")
```
This prevents embedding secrets in code or images.

## Example `requirements.txt`
(Ensure this file exists in your repo)
```
streamlit
pillow
requests
```
Add specific versions if desired, e.g. `streamlit==1.25.0`.

## Expected API Payload & Response
Payload example (simplified):
```json
{
  "contents": [
    {
      "parts": [
        {"text": "Extract all visible text..."},
        {
          "inlineData": {
            "mimeType": "image/jpeg",
            "data": "<BASE64_IMAGE_DATA>"
          }
        }
      ]
    }
  ]
}
```

Extracted text location in response:
```py
result['candidates'][0]['content']['parts'][0]['text']
```

## Error Handling
- Network/HTTP errors: handled via `requests.exceptions.RequestException`.
- Other processing errors: caught by a generic exception block and shown in Streamlit.

## Security Best Practices
- Never embed API keys in source code or Docker images pushed to public registries.
- Use environment variables, Docker secrets, or cloud secret managers (e.g., GCP Secret Manager, AWS Secrets Manager).
- Limit the scope and rotate keys regularly.
- Scan images and limit upload size to mitigate abuse.

## Improvements & Next Steps
- Change `app.py` to use `os.getenv("GEMINI_API_KEY")` and update the README accordingly (I can do this for you).
- Implement a parser to convert raw text into structured JSON/CSV (items, qty, price, totals, date).
- Add retry/backoff for API calls and caching for repeated images.
- Add CI/CD pipeline to build Docker image and push to registry.
- Add health checks and production-ready process manager (e.g., Gunicorn) if deploying behind reverse proxy.

## Troubleshooting
- Pillow installation errors in Docker: ensure `libjpeg-dev` and `zlib1g-dev` are installed (already included in Dockerfile).
- Streamlit not accessible: confirm container port mapping `-p 8501:8501` and no host firewall blocking.
- API errors: check your API key, billing status, and network connectivity.
