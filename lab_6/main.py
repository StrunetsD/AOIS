class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.C = False  # Коллизия
        self.U = True  # Занято
        self.T = True  # Терминальный
        self.L = False  # Связь
        self.D = False  # Удален


class HashTable:
    def __init__(self, size=20):
        self.size = size
        self.table = [None] * size
        self.base_address = 0
        self.letters_ru = [
            'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ж', 'З', 'И', 'Й',
            'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У',
            'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э',
            'Ю', 'Я'
        ]

    def get_code(self, char):
        return self.letters_ru.index(char) if char in self.letters_ru else 0

    def hash_function(self, key):
        key = key.upper().ljust(2, 'А')
        first, second = key[0], key[1]
        code_first = self.get_code(first)
        code_second = self.get_code(second)
        v = code_first * 33 + code_second
        return (v % self.size + self.base_address) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        if self.table[index] is None:
            self.table[index] = Node(key, value)
        else:
            current = self.table[index]
            while True:
                if current.key == key and not current.D:
                    raise ValueError(f"Ключ '{key}' уже существует!")
                if current.T:
                    break
                current = current.next
            new_node = Node(key, value)
            new_node.C = True
            current.T = False
            current.next = new_node
            self.table[index].C = True

    def search(self, key):
        index = self.hash_function(key)
        current = self.table[index]
        while current:
            if current.key == key and not current.D:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        index = self.hash_function(key)
        current = self.table[index]
        prev = None
        while current:
            if current.key == key and not current.D:
                current.D = True
                current.U = False
                if prev:
                    prev.next = current.next
                    if prev.next is None:
                        prev.T = True
                else:
                    self.table[index] = current.next
                return True
            prev = current
            current = current.next
        return False

    def display(self):
        print("\nСостояние хеш-таблицы:\n")
        print("{:<6} | {:<40} | {:<30}".format("Индекс", "Цепочка ключей и значений", "Статусы"))
        print("-" * 90)
        for idx in range(self.size):
            current = self.table[idx]
            if current is None:
                print(f"{idx:<6} | [пусто]")
                continue

            chain_output = []
            status_output = []
            while current:
                status = []
                if current.C: status.append("коллизия")
                if not current.U: status.append("свободно")
                if current.T: status.append("конец цепи")
                if current.D: status.append("удалено")
                if not status:
                    status.append("нормально")

                chain_output.append(f"{current.key} → {current.value}")
                status_output.append(f"[{', '.join(status)}]")
                current = current.next

            print(f"{idx:<6} | {' -> '.join(chain_output):<40} | {' -> '.join(status_output)}")

    def update(self, key, new_value):
        index = self.hash_function(key)
        current = self.table[index]
        while current:
            if current.key == key and not current.D:
                current.value = new_value
                return True
            current = current.next
        return False

    def load_factor(self):
        occupied = sum(1 for bucket in self.table if bucket is not None)
        return occupied / self.size


ht = HashTable()

data = [
    ("Футбол", "Командная игра с мячом"),
    ("Баскетбол", "Игра с кольцом"),
    ("Волейбол", "Игра через сетку"),
    ("Волейболпляжный", "Песчаный вариант"),
    ("Теннис", "Игра с ракетками"),
    ("Биатлон", "Лыжи и стрельба"),
    ("Бокс", "Кулачный бой"),
    ("Борьба", "Борьба на поясах"),
    ("Гимнастика", "Художественная и спортивная"),
    ("Плавание", "Водный вид спорта"),
    ("Фигурноекатание", "Ледовые выступления"),
]

ht.update("Футбол", "Модернизированное описание игры")

for key, value in data:
    try:
        ht.insert(key, value)
    except ValueError as e:
        print(e)

ht.display()
print(f"\nКоэффициент заполнения: {ht.load_factor():.2f}")