FROM debian:bullseye-slim
RUN apt update -y && apt install -y python3 python3-pip ffmpeg cmake libxml2-dev libxmlsec1-dev
RUN pip3 install dlib
WORKDIR /app
COPY . /app
RUN pip3 install -r req-a1.txt
CMD ["python3","main.py"]