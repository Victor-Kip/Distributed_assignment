FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install flask docker requests
EXPOSE 5000
CMD ["python", "balancer.py"]
