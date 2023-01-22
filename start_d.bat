:: сбилдить образ
docker build -t app .
:: запустить контейнер
docker run --rm -p 5000:5000 app