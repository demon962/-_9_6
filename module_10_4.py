import threading
import time
import random
import queue

class Table:
    def __init__(self, number):
        self.number = number
        self.guest = None


class Guest(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def run(self):
        # Эмуляция приёма пищи
        time_to_eat = random.randint(3, 10)
        time.sleep(time_to_eat)


class Cafe:
    def __init__(self, *tables):
        self.queue = queue.Queue()
        self.tables = list(tables)

    def guest_arrival(self, *guests):
        for guest in guests:
            free_table = next((t for t in self.tables if t.guest is None), None)
            if free_table:
                free_table.guest = guest
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")
                guest.start()
            else:
                self.queue.put(guest)
                print(f"{guest.name} в очереди")

    def discuss_guests(self):
        while not self.queue.empty() or any(table.guest for table in self.tables):
            for table in self.tables:
                if table.guest and not table.guest.is_alive():
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")
                    table.guest = None
                    print(f"Стол номер {table.number} свободен")
                    if not self.queue.empty():
                        new_guest = self.queue.get()
                        table.guest = new_guest
                        print(f"{new_guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")
                        new_guest.start()
            time.sleep(0.01)


cafe = Cafe(Table(1), Table(2), Table(3))

guests = [
    Guest('Иван'),
    Guest('Мария'),
    Guest('Петр'),
    Guest('Анна'),
    Guest('Сергей')
]

cafe.guest_arrival(*guests)
cafe.discuss_guests()