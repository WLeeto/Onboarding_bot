# Onboarding bot

### Общая логика:
* <a href="https://miro.com/app/board/uXjVMdrCxL4=/?share_link_id=416191956347">Миро с логикой</a>
* <a href="https://docs.google.com/spreadsheets/d/1vUxmU82UEEuKlfqwD5p6xwzTZ5_UYug43UMbXmBPawE/edit#gid=1849404296">Фаил с описаниями функций где беспределят все кто хочет</a>


### Реализация поиска:
Бот использует систему поиска по редакционному расстоянию (Расстояние Левенштейна, библиотека FuzzyWuzzy)
Чуствительность поска можно настроить в функции recognize_question (~/func/all_funk) переменная sensitivity
(0 <= sensitivity <= 100). При sensitivity == 100 ,будут фильтроваться только запросы совпадающие на 100%
(регистр не учитывается)

### Наполнение БД:
Обучение бота происходит через наполнение БД вопросов. Если бот не может найти вопроса в БД
(соответствующего на расстояние sensitivity) - он предлагает переслать ответ оператору. После ответа оператору 
предлагается добавить связку вопрос-ответ в БД 

### Команды:
--- Старое ---
* /addanswer - добавляет ответ в БД
* /allanswers - выводит список всех ответов
* /addquestion - добавляет вопрос в БД и привязывает его к ответу
* /allquestions - выводит список всех вопросов
* /_resetdb - сбрасывает БД и удаляет все данные (только админ)
* /_filldb - заполнить БД тестовыми данными (только админ)
* Если боту прислать видео - он отдаст ID этого видео в TG

--- Новое ---
* /сontacts
* /vacation
* /docs
* /support
* /social_media
* /initiative
* /finance
* /referal
* /office
* /tf360
* /projects
* /about_Team_Force

* /find - поиск сотрудника по фамилии или должности




### База данных:
* БД пользователей </br>
![БД пользователей](/img/db_users.png)
* Полная БД </br>
![БД](/img/db_requests.png)



### Запуск:
Запуск из докера:
* docker-compose up --build (убедитесь что упаковка БД раскоменчена)

Запуск без докера:
* настроить sqlalchemy (class database в ~/database/requests). Достаточно настроить __init__ для подключения к необходимой БД
* установка зависимостей из requirements.txt
* точка входа main.py (python main.py)

