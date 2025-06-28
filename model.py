# model.py
# Kod napisał Kuba

from datetime import datetime


# Klasa bazowa Task - wszystkie zadania w systemie
class Task:
    # Statyczny licznik do generowania unikalnych ID dla zadań
    _id_counter = 1

    def __init__(self, name, description, priority=1):
        # Prywatne atrybuty (enkapsulacja)
        self._id = Task._id_counter
        Task._id_counter += 1  # Po każdym nowym zadaniu zwiększamy licznik
        self._name = name
        self._description = description
        self._priority = priority
        self._done = False
        self._created_at = datetime.now()  # Data utworzenia zadania

    # Gettery i settery - enkapsulacja danych, zabezpieczenie przed bezpośrednią edycją
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_description(self):
        return self._description

    def set_description(self, desc):
        self._description = desc

    def get_priority(self):
        return self._priority

    def set_priority(self, priority):
        self._priority = priority

    def mark_done(self):
        # Oznacz zadanie jako wykonane
        self._done = True

    def is_done(self):
        return self._done

    def get_created_at(self):
        return self._created_at

    def display(self):
        # Wyświetl informacje o zadaniu
        print(self)

    def __str__(self):
        # Czytelna reprezentacja zadania (na potrzeby printa)
        return f"Zadanie[{self._id}]: {self._name} (priorytet: {self._priority}, wykonane: {self._done})"

    # Metoda klasowa - alternatywny konstruktor, np. przy odczycie z pliku
    @classmethod
    def from_dict(cls, data):
        # Tworzy zadanie na podstawie słownika (np. wczytanego z JSON)
        obj = cls(
            data.get('name', 'Brak nazwy'),
            data.get('description', ''),
            data.get('priority', 1)
        )
        if data.get('done', False):
            obj.mark_done()
        return obj

    @staticmethod
    def static_example():
        # Przykład metody statycznej (nie używa self ani cls)
        print("To jest metoda statyczna w klasie Task.")


# Dziedziczenie - przykład zadania specjalnego
class SpecialTask(Task):
    # Tutaj Kuba pokazuje dziedziczenie, nadpisywanie metod, super()
    def __init__(self, name, description, priority=1, tag="SPECJALNE"):
        super().__init__(name, description, priority)
        self._tag = tag  # Dodatkowy atrybut tylko dla SpecialTask

    def get_tag(self):
        return self._tag

    def display(self):
        # Nadpisujemy display, żeby wyświetlić tag
        print(f"[{self._tag}] {self}")

    def __str__(self):
        # Nadpisujemy __str__ (polimorfizm) - inny opis dla zadań specjalnych
        return f"SpecjalneZadanie[{self.get_id()}]: {self.get_name()} (priorytet: {self.get_priority()}, tag: {self._tag}, wykonane: {self.is_done()})"


# Własny wyjątek (Custom Exception) - zgodnie z wymaganiami
class TaskNotFoundException(Exception):
    def __init__(self, task_id):
        super().__init__(f"Nie znaleziono zadania o id {task_id}.")


# Klasa zarządzająca zadaniami (TaskManager)
class TaskManager:
    # Tutaj Kuba pokazuje agregację i zarządzanie listą obiektów
    def __init__(self):
        self._tasks = []  # Lista wszystkich zadań

    def add_task(self, task):
        self._tasks.append(task)

    def remove_task(self, task_id):
        # Usuwa zadanie po id - rzuca wyjątek jeśli nie znajdzie
        task = self.find_task(task_id)
        self._tasks.remove(task)

    def find_task(self, task_id):
        # Szuka zadania po ID, jeśli nie znajdzie - wyjątek
        for t in self._tasks:
            if t.get_id() == task_id:
                return t
        raise TaskNotFoundException(task_id)

    def mark_task_done(self, task_id):
        task = self.find_task(task_id)
        task.mark_done()

    def set_task_priority(self, task_id, priority):
        task = self.find_task(task_id)
        task.set_priority(priority)

    def list_tasks(self):
        # Zwraca listę wszystkich zadań (do wyświetlenia/sortowania)
        return self._tasks

    @staticmethod
    def print_tasks(tasks):
        # Statyczna metoda - drukowanie dowolnej listy zadań
        for t in tasks:
            t.display()
