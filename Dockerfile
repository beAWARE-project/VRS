FROM python:3.6.4

COPY main/src /usr/src

RUN pip install --upgrade pip
RUN pip install confluent-kafka
RUN pip install netCDF4
RUN pip install xmltodict
RUN pip install requests
RUN pip install matplotlib
RUN pip install scipy
RUN pip install xlrd 
RUN pip install openpyxl
RUN pip install pandas==0.20.3



#COPY src/image_analyzer.py /usr/src/listener/
#COPY src/image_listener.py /usr/src/listener/
#COPY src/timing_test.py /usr/src/listener/
#COPY src/output/timetest_output.json /usr/src/listener/output/
#COPY src/model/label_map.pbtxt /usr/src/listener/model/
#COPY src/model/crisis_index.json /usr/src/listener/model/

WORKDIR /usr/src/

#RUN wget -O frozen_inference_graph.pb http://object-store-app.eu-gb.mybluemix.net/objectStorage?file=frozen_inference_graph.pb
#RUN wget -O vgg_places https://www.dropbox.com/s/53xg37xytrpp8rp/vgg_places?dl=0

#WORKDIR /usr/src/
#WORKDIR /usr/src/listener/

#ENV PYTHONPATH="/usr/local/lib/python3.5/site-packages/tensorflow/models/:/usr/local/lib/python3.5/site-packages/tensorflow/models/slim:${PYTHONPATH}"

CMD python3 VRS_listener.py 
#or  python VRS_listener.py / py VRS_listener.py  / VRS_listener.py


