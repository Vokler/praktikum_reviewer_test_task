"""
Условные обозначения перед комментарием к коду:

Fix - надо исправить;
CBB - можно лучше (could be better);
G - отлично (Great).
"""

import datetime as dt


class Record:
    def __init__(self, amount, comment, date=''):
        self.amount = amount
        # Fix
        # Здесь лучше добавить валидатор для значения `date`, так как,
        # если пользователь введет дату не в нужном формате, то будет выдана
        # ошибка. Рекомендую посмотреть данную статью, в которой показываются
        # различные способы валидации атрибута:
        # https://towardsdatascience.com/6-approaches-to-validate-class-attributes-in-python-b51cffb8c4ea
        self.date = (
            dt.datetime.now().date() if
            not
            date else dt.datetime.strptime(date, '%d.%m.%Y').date())
        self.comment = comment


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    # CBB
    # Логика этого метода - отлично, но есть пару предложений по улучшению.
    # 1. Вместо записи `today_stats = today_stats + Record.amount`
    # можно использовать инкремент.
    # 2. Весь этот метод можно записать буквально в одну строчку, используя
    # List Comprehension. Подробнее можно посмотреть пример тут:
    # https://www.w3schools.com/python/python_lists_comprehension.asp
    # Подсказка: в Python есть еще функция sum(), которая здесь отлично подойдет :)
    def get_today_stats(self):
        today_stats = 0
        # Fix
        # При использовании переменных в Python следует использовать
        # строчные буквы согласно PEP8.
        # Рекомендую исправть `Record` на `record`. Здесь вы сможете найти
        # более подробную информацию:
        # https://peps.python.org/pep-0008/#method-names-and-instance-variables
        for Record in self.records:
            if Record.date == dt.datetime.now().date():
                today_stats = today_stats + Record.amount
        return today_stats

    # CBB
    # Вам необязательно следует указывать второе условие `>= 0`, так как
    # по условию задачи необходимо предоставить данные за последние 7 дней и
    # если возьмете все записи, в которых `date` < последних 7 дней, то
    # получите нужную выборку.
    #
    # Также пакет `datetime` имеет отличную функцию, которая называется
    # `timedelta()`. Вы можете попробовать использовать ее в своем коде :)
    #
    # И, конечно, можете также использовать и здесь List Comprehension.
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        for record in self.records:
            if (
                (today - record.date).days < 7 and
                (today - record.date).days >= 0
            ):
                week_stats += record.amount
        return week_stats


class CaloriesCalculator(Calculator):
    # Fix
    # Прочитайте, пожалуйста, про требования к коду, а именно раздел,
    # как положено оформлять комментарии к функциям/методам:
    # https://docs.google.com/document/d/1s_FqVkqOASwXK0DkOJZj5RzOm4iWBO5voc_8kenxXbw/edit
    def get_calories_remained(self):  # Получает остаток калорий на сегодня
        # Fix
        # Также следует из требований к коду, что переменные названы в
        # соответствии с их смыслом. Избегайте однобуквенных названий, так как
        # другим программистам, читающий ваш код, может быть не понятно,
        # что вы имели в виду под `x`.
        x = self.limit - self.get_today_stats()
        # CBB
        # Небольшое предложение по улучшению стилистики кода:
        # здесь можно создать, например, две переменные
        # `is_ok_msg` и `is_not_ok_msg` и присвоить им возвращаемые значения
        # соответственно. А затем использовать тернарный оператор:
        # https://stackoverflow.com/questions/2802726/putting-a-simple-if-then-else-statement-on-one-line
        # Это на ваше усмотрение потому что, то, как вы сделали
        # - хороший вариант.
        if x > 0:
            return f'Сегодня можно съесть что-нибудь' \
                   f' ещё, но с общей калорийностью не более {x} кКал'
        else:
            # Fix
            # Здесь используются круглые скобки, которые не несут никакой
            # функциональности, поэтому их можно удалить. + не хватает пробела
            # между `return` и возвращаемым значением.
            return('Хватит есть!')


class CashCalculator(Calculator):
    USD_RATE = float(60)  # Курс доллар США.
    EURO_RATE = float(70)  # Курс Евро.

    # CBB
    # Ваш метод get_today_cash_remained() работает правильно, но я хотел бы
    # предложить вам улучшение по нему, чтобы сократить кол-во выполняемых
    # операций, а также кол-во строк кода - чтобы данный метод стал более легко
    # читаем.
    #
    # А в рамках вашего метода я дам рекомендации по улучшению в самом методе.
    #
    # Чтобы убрать `if else` для определения `cash_remained` в валюте и
    # `currency_type`, я бы рекомендовал вам использовать словарь, который
    # содержал бы в себе всю эту информацию.
    # Например CURRENCIES = {'usd': {'rate': USD_RATE, 'type': 'USD'}, ...}
    # Далее вы в методе обращаетесь к словарю и достаете всю нужную информацию
    # о валюте по ключу `currency`, который передается в метод.
    # Но учтите такой сценарий, что пользователь может передать несуществующую
    # валюту, которая вызовет ошибку, так что нужно будет вывести сообщение о
    # том, какие валюты пользователь может использовать.

    # Fix
    # Теперь по вашему методу. Атрибуты `USD_RATE` и `EURO_RATE` необязательно
    # использовать, так как вы их уже определили, как константы в классе и
    # можете к ним обращаться - self.USD_RATE
    def get_today_cash_remained(self, currency,
                                USD_RATE=USD_RATE, EURO_RATE=EURO_RATE):
        currency_type = currency
        cash_remained = self.limit - self.get_today_stats()
        # Fix
        # Следует учесть, что пользователь может передать не существующую
        # валюту, например ILS.
        if currency == 'usd':
            cash_remained /= USD_RATE
            currency_type = 'USD'
        elif currency_type == 'eur':
            cash_remained /= EURO_RATE
            currency_type = 'Euro'
        elif currency_type == 'rub':
            # Fix
            # У вас здесь идет сравнение `cash_remained` со значением 1.00 и
            # так как далее после этого сравнения нет выполнения какого-либо
            # кода, то данная операция не несет никакой смысл.
            # В данном блоке достаточно только присвоить значение
            # к `currency_type`, так как мы изначально работаем с рублями и
            # деление никакое не требуется.
            cash_remained == 1.00
            currency_type = 'руб'
        if cash_remained > 0:
            # Fix
            # Согласно требованию к коду для студентов в f-строках применяется
            # только подстановка переменных и нет логических или арифметических
            # операций:
            # https://docs.google.com/document/d/1s_FqVkqOASwXK0DkOJZj5RzOm4iWBO5voc_8kenxXbw/edit
            return (
                f'На сегодня осталось {round(cash_remained, 2)} '
                f'{currency_type}'
            )
        elif cash_remained == 0:
            return 'Денег нет, держись'
        elif cash_remained < 0:
            return 'Денег нет, держись:' \
                   ' твой долг - {0:.2f} {1}'.format(-cash_remained,
                                                     currency_type)

    # Fix
    # Если метод планируется переопределить (т.е. изменить его поведение от
    # изначального, которое заложено в родительском классе Calculator) с
    # сохранением логики родительского метода, то тогда есть смысл определение
    # этого же метода в унаследованном классе. В данном случае же у вас нет
    # никакой новой логики, поэтому определение вновь этого метода здесь
    # не несет никакой смысл.
    def get_week_stats(self):
        # Fix
        #  Также обратите внимание, если вы уже вызываете логику
        #  родительского класса, то необходимо вернуть полученное значение с
        #  помощью `return`, потому что в данном случае у вас метод всегда
        #  будет возвращать None.
        super().get_week_stats()
