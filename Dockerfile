FROM python:3.7-slim

WORKDIR /hypertube

COPY . /hypertube

RUN apt-get update

#RUN apt-get install -y git
#RUN git clone https://github.com/arvidn/libtorrent.git libtorrent && \
#cd libtorrent && pwd && python setup.py build && python setup.py install

#RUN cd libtorrent && python setup.py build && python setup.py install
#RUN apt-get install -y python3-libtorrent

RUN apt-get install -y build-essential checkinstall libboost-system-dev libboost-python-dev libboost-chrono-dev \
 libboost-random-dev libssl-dev autoconf automake libtool
RUN cd libtorrent && ./autotool.sh && ./configure --enable-python-binding --with-libiconv && make -j$(nproc) && \
 make install && ldconfig

RUN pip3 install -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver_plus", "0.0.0.0:8000", "--cert-file", "cert.crt"]


