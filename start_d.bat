:: сбилдить образ
docker build -t app .
:: запустить контейнер
docker run --rm -p 5000:5000 -p 5432:5432 -p 5001:5001 app