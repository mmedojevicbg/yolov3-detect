FROM python:3.7-slim

RUN apt-get update && \
    apt-get upgrade && \
    apt-get -yq install git gcc libglib2.0-0 libsm6 libxrender1 wget curl

RUN pip3 install --upgrade pip && \
    pip3 install --upgrade cython && \
    pip3 install -U numpy --no-cache-dir && \
    pip3 install -U opencv-python --no-cache-dir && \
    pip3 install -U torch --no-cache-dir && \
    pip3 install -U matplotlib --no-cache-dir && \
    pip3 install -U pycocotools --no-cache-dir && \
    pip3 install -U tqdm --no-cache-dir && \
    pip3 install -U tb-nightly --no-cache-dir && \
    pip3 install -U future --no-cache-dir && \
    pip3 install -U torchvision --no-cache-dir && \
    pip3 install -U flask --no-cache-dir && \
    pip3 install -U flask_bootstrap --no-cache-dir && \
    pip3 install -U Flask-BasicAuth --no-cache-dir

WORKDIR /home
RUN wget https://github.com/ultralytics/yolov3/archive/v7.tar.gz && \
    tar -xvzf v7.tar.gz && \
    mv yolov3-7 yolov3

WORKDIR /home/yolov3
RUN chmod a+x ./weights/download_yolov3_weights.sh && \
    ./weights/download_yolov3_weights.sh

WORKDIR /home
#COPY flask /home/flask
VOLUME /home/flask
WORKDIR /home/flask
RUN mkdir -p /home/flask/static/uploads/output

WORKDIR /home/flask
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
