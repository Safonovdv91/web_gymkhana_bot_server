# Подготовка графана для логирования

## Устанавливаем настройки

## добавление графана для входа
#### создание единой сети для объединения контейнеровm, так же задается субнет чтобы для локи был отдельный ip-адресс 
Запуск опенсорс клиента grafana(grafana/grafana-oss) - для бесплатной версии
> docker network create -d bridge --subnet=172.28.0.0/16 mynet_grafana
docker run -d -p 3000:3000 --name=grafana --net mynet_grafana -e GF_SECURITY_ADMIN_USER=newuser -e GF_SECURITY_ADMIN_PASSWORD=newpassword grafana/grafana-oss

## Настройки для loki и promtail:

### Скачиваем конфиг файлы в отдельную папку
> mkdir evalute_loki
> cd evalute_loki
>wget https://raw.githubusercontent.com/grafana/loki/v2.9.1/cmd/loki/loki-local-config.yaml -O loki-config.yaml
>wget https://raw.githubusercontent.com/grafana/loki/v2.9.1/clients/cmd/promtail/promtail-docker-config.yaml -O promtail-config.yaml

в файле promtail-config.yml внести изменения
> clients:
>    -url: http://172.28.0.7:3100/lo....

и добавляем для запуска в нашей сети 
> --net mynet_grafana
> --ip 172.28.0.7

Запуск на ip адресе, 7 или можно другой. В рамках докер-композ не будет проблем и без этого, но при отдельном запуске лучше 
прописать прямой адрес

## запускаем docker контейнеры
loki
docker run --name loki -d --net mynet_grafana --ip 172.28.0.7 -v $(pwd):/mnt/config -p 3100:3100 grafana/loki:2.9.1 -config.file=/mnt/config/loki-config.yaml
promtail
docker run --name promtail --net mynet_grafana -d -v $(pwd):/mnt/config -v /var/log:/var/log --link loki grafana/promtail:2.9.1 -config.file=/mnt/config/promtail-config.yaml

## В бразузере настройки

127.0.0.1:3000
user:newuser
password:newpassword

connections
loki
url:  http://172.28.0.7:3100

