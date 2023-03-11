#Download bullseye-slim image
FROM debian:bullseye-slim
#Installing packages
RUN apt update -y && apt install -y python3 python3-pip ffmpeg 
#Download models under /app and build dlib
WORKDIR /app
#Run before COPY as dlib builds are very time consuming
# RUN pip3 install dlib
#Copy files to #/app
COPY . /app
#Install Python packages
RUN pip3 install -r requirements.txt
#Execution of main.py
CMD ["python3","main.py"]
