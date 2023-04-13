import redis
from redis_lru import RedisLRU
from mongoengine import DoesNotExist
from models import Quotes, Author

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


def find_name(name: str):
    try:
        author = Author.objects(fullname__startswith=name.title()).first()
        quotes = Quotes.objects(author=author)
        result = [f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
        for quote in result:
            print(quote)
    except DoesNotExist:
        print(f'Автора {name.title()} не знайдено в базі')


@cache
def find_one_tag(tag: str):
    try:
        quotes = Quotes.objects(tags__startswith=tag.lower())
        result = [f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
        for quote in result:
            print(quote)
    except DoesNotExist:
        print(f'Тег {tag.lower()} не знайдено в базі')


@cache
def find_tags(tags: list):
    try:
        quotes = Quotes.objects(tags__in=tags)
        result = [f"{quote.quote} ({quote.author.fullname}, {', '.join(quote.tags)})" for quote in quotes]
        for quote in result:
            print(quote)
    except DoesNotExist:
        print(f'Теги {str([tag.lower() for tag in tags])} не знайдено в базі')


if __name__ == '__main__':
    while True:
        text = input('Введіть команду: ')
        if text.lower() == 'exit':
            print('До нових зустрічей!')
            break
        try:
            input_text = text.split(':')
            command = input_text[0]
            data = input_text[1].strip().split(',')
            if len(data) <= 1:
                data = data[0]
            match command:
                case 'name':
                    find_name(data)
                case 'tag':
                    find_one_tag(data)
                case 'tags':
                    find_tags(data)
                case _:
                    print('Невідома команда')
        except Exception as err:
            print(f'Помилка {err}')
