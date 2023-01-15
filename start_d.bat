:: сбилдить образ
docker build -t app .
:: запустить контейнер
docker run -p 5000:5000 app