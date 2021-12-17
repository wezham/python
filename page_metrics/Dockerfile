FROM python:3.8


WORKDIR /page_metrics

COPY ./ ./

RUN pip install -r requirements.txt
RUN cd page_metrics
RUN python setup.py install

CMD ["bash"]