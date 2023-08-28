FROM python:3.10 

RUN python -m pip install --no-cache-dir flask flask-cors numpy tensorflow joblib scikit-learn

WORKDIR /usr/src/app
COPY . .

ENTRYPOINT ["python"]
CMD ["train.py"]