@echo off
echo Building Docker image for backend...
docker build -t backend .
if %errorlevel% neq 0 (
  echo Failed to build Docker image.
  pause
  exit /b
)

echo Running Docker container for backend...
docker run -d -it -p 8000:8000 backend
if %errorlevel% neq 0 (
  echo Failed to run Docker container.
  pause
  exit /b
)

echo Docker container is running on port 8000.