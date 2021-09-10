# Публикуем комиксы в контакте
Скачиваем случайный комикс и публикуем его у себя в группе в контакте.
### download_random_comic
Скачивает случайный комикс.
### publish_comic_vk
Публикует комикс в вашей группе в контакте.
### Как установить
Для начала вам необходимо создать фан-группу в контакте. После этого создайте 
приложение в контакте, сделать это можно тут: [страница для разработчиков](https://vk.com/dev)
(тип приложения укажите `standalone`). \
В приложении нажмите кнопку редактировать и сохраните свой `client_id`. 

Для получения токена перейдите на [Implicit Flow](https://vk.com/dev/implicit_flow_user),
следуйте инструкциям, права укажите следующие: `photos`, `groups`, `wall` и `offline`.

Для получения id группы в контакте нажмите [здесь](https://regvk.com/id/)

Рядом с кодом создайте файл `.env`, в котором будут храниться ваши личные данные:

```
VK_TOKEN='ваш токен vk'
```
```
VK_GROUP_ID='id группы в контакте'
```
Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть
конфликт с Python2) для установки зависимостей:

```
pip install -r requirements.txt
```
### Как запустить

Запустить и опубликовать случайный комикс:
```
$ python publish_comic_vk.py
```
### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).