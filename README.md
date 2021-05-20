# Публикуем комиксы в созданную вами группу в социальной сети

Скрипт для публикации комиксов [xkcd](https://xkcd.com/) в созданную вами группу в социальной сети [vk.com](https://vk.com/).

## Установка

- Для работы скрипта у вас должен быть установлен [Python3](https://www.python.org/downloads/) (не ниже версии 3.6.0).
- Скачайте код.
- Рекомендуется использовать [virtualenv/env](https://docs.python.org/3/library/venv.html) для изоляции проекта.
- Установите зависимости для работы скрипта.

```sh
pip install -r requirements.txt
```

## Переменные окружения

Создайте файл `.env`, который содержит данные в формате `ПЕРЕМЕННАЯ=значение`.

Доступны 3 переменные:

- `VK_GROUP_ID` - cоздайте группу на сайте [vk.com](https://vk.com/). Для примера, `id` группы по [ссылке](https://vk.com/club1) равняется `1`.
- `VK_ACCESS_TOKEN` - создайте [standalone приложение](https://vk.com/apps?act=manage), затем воспользуйтесь [запросом](https://oauth.vk.com/authorize?client_id=your_id&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.130) вместо `your_id` укажите значение `client_id`, полученное при создании приложения, разрешите доступ приложению к вашей странице.
- `VK_API_VERSION` - на время написание скрипта использовалась версия `5.130`.

## Запуск

```sh
python main.py
```

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).