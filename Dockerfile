FROM python:3.13.1-slim-bookworm

RUN python -m pip install grpcio-tools
RUN python -m pip install grpcio

RUN python -m pip install pymodbus

RUN mkdir -p /opt/bos/device/drivers/modbus
WORKDIR /opt/bos/device/drivers/modbus

COPY . /opt/bos/device/drivers/modbus/

CMD ["python", "server.py"]