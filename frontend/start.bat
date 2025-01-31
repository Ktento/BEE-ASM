@echo off
echo Building Docker image for frontend...
docker build -t frontend .
if %errorlevel% neq 0 (
  echo Failed to build Docker image.
  pause
  exit /b
)

echo Running Docker container for frontend...
docker run -d -it -p 80:80 frontend
if %errorlevel% neq 0 (
  echo Failed to run Docker container.
  pause
  exit /b
)

echo Docker container is running on port 80.
