#Download bullseye-slim image
FROM debian:bullseye-slim
#Installing packages
RUN apt update -y && apt install -y python3 python3-pip ffmpeg cmake libxml2-dev libxmlsec1-dev wget
#Download models under /app and build dlib
WORKDIR /app
RUN mkdir -p stable_diffusion/models
RUN wget https://huggingface.co/Linaqruf/anything-v3.0/resolve/main/Anything-V3.0.ckpt -P stable_diffusion/models
RUN wget https://huggingface.co/gsdf/Counterfeit-V2.0/resolve/main/Counterfeit-V2.0.ckpt -P stable_diffusion/models
RUN wget https://huggingface.co/dreamlike-art/dreamlike-photoreal-2.0/resolve/main/dreamlike-photoreal-2.0.ckpt -P stable_diffusion/models
#Run before COPY as dlib builds are very time consuming
RUN pip3 install dlib
#Copy files to #/app
COPY . /app
#Install Python packages
RUN pip3 install -r req-a1.txt
#Execution of main.py
CMD ["python3","main.py"]