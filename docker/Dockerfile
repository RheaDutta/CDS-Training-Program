FROM ubuntu

RUN \
    apt update && \
    apt install -y python3 python3-pip wget git && \
    ln -s python3 /usr/bin/python && \
    ln -s pip3 /usr/bin/pip

WORKDIR /workspace

RUN wget https://pari.math.u-bordeaux.fr/pub/pari/unix/pari-2.11.0.tar.gz && \
    tar -xvzf pari-2.11.0.tar.gz && cd pari-2.11.0 && \
    ./Configure && make install && \
    pip install cython && \
    pip install cysignals

RUN apt update && apt install -y python3-cypari2

RUN rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
