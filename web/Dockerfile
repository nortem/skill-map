FROM python:3.7-slim-buster
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip
RUN python3 -m pip install -r /tmp/requirements.txt
COPY . /tmp
WORKDIR /tmp
CMD ["python3", "skill_map.py"]