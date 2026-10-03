FROM python:3.12-slim
WORKDIR /work
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/work/src
CMD ["bash", "-c", "pytest -q && python benchmarks/run_all.py"]
