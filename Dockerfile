FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install pandas numpy scikit-learn matplotlib pytest pytest-cov

CMD ["bash"]