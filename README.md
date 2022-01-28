# Telegram Bot для получения и конвертации курсов криптовалют

## Описание
Бот реализован с помощью фреймворка [AIOgram](https://docs.aiogram.dev/en/latest/index.html).
Данный бот, используя актуальные данные с [PancakeSwap API](http://github.com/pancakeswap/pancake-info-api), может сообщать пользователю курс токена к USDT либо курс одного токена к другому.

Бот имеет два режима:
* Показать текущий курс валюты к USDT при отправке её названия (полного или сокращённого) или адреса.
	> Пример названий:  
	> Полное - TRON  
	> Сокращённое - TRX  
	> Адрес - 0x85EAC5Ac2F758618dFa09bDbe0cf174e7d574D5B  
* Показывать курс валютной пары при отправке двух названий (полного или сокращённого) или адресов.


## Запуск
```
sh start.sh <YOUR_TELEGRAM_API_TOKEN>
```

## Настройка
`app/config.py` - конфигурационный файл.
Доступные настройки:
* `url` адреса для API 
* сообщения, которые бот использует для реакции на действия пользователя 
* `SIM_IND` - параметр, с помощью которого можно настроить чувствительность бота к опечаткам пользователя: чем больше параметр, тем ниже чувствительность и больше предлагаемых варинтов в случае опечатки. Пример:
```
SIM_IND=1 is_similar("ethereum", "ethireume") -> False
SIM_IND=2 is_similar("ethereum", "ethireume") -> True 
```
* `UP_TOKEN_LIST` - с помощью этого параметра можно включить обновление списка токенов с определённой периодичностью, задаваемой с помощью параметров `UP_EVERY` и `UP_PERIOD`. Например, при параметрах `UP_EVERY = 5` и `UP_PERIOD = 'seconds'` обновление списка токенов будет происходить каждые 5 секунд.

## Архитектура
* `handlers` - обработчики команд и сообщений пользователя
* `keyboards` - клавиатуры (для команды `/start` и для сообщения с предложением выбрать один из вариантов в случае опечатки)
* `modules` - классы для работы с API и для получения адреса валюты по её названию

## Требования для запуска
* [pipenv](https://pypi.org/project/pipenv/)
* Docker
