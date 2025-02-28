import os

dir_path = os.path.join(os.path.abspath(os.curdir), 'config')
files = ['ball.txt', 'fact.txt', 'quotes.txt', 'when.txt', 'because.txt', 'status.txt']

data = {}
for file in files:
    with open(os.path.join(dir_path, file), 'r', encoding='utf-8') as f:
        data[file[:-4]] = f.read().split('\n')  # Убираем .txt в качестве ключа

# Теперь у тебя есть словарь `data`, где ключи – это имена файлов без расширения
foo = data['ball']
facts = data['fact']
quotes = data['quotes']
when = data['when']
because = data['because']
status = data['status']