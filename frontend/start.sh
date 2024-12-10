docker build -t frontend .
docker run -d -it -p 80:80 frontend
