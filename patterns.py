# patterns.py
# Kod napisał Kornel

from model import Task, TaskManager, TaskNotFoundException

# --- WZORZEC STRATEGIA (STRATEGY) ---
# Kornel: Różne sposoby sortowania zadań

class SortStrategy:
    """Interfejs strategii sortowania zadań."""
    def sort(self, tasks):
        raise NotImplementedError

class SortByPriority(SortStrategy):
    # Kornel: sortowanie po priorytecie rosnąco
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.get_priority())

class SortByDate(SortStrategy):
    # Kornel: sortowanie po dacie utworzenia
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.get_created_at())

class SortByName(SortStrategy):
    # Kornel: sortowanie po nazwie zadania (alfabetycznie)
    def sort(self, tasks):
        return sorted(tasks, key=lambda t: t.get_name().lower())

# --- WZORZEC POLECENIE (COMMAND) ---
# Kornel: Każda akcja (dodaj, usuń, oznacz jako wykonane) jest osobną klasą

class Command:
    """Bazowa klasa polecenia."""
    def execute(self):
        raise NotImplementedError

class AddTaskCommand(Command):
    def __init__(self, task_manager, task):
        self.task_manager = task_manager
        self.task = task

    def execute(self):
        self.task_manager.add_task(self.task)
        print("[Polecenie] Zadanie dodane.")

class RemoveTaskCommand(Command):
    def __init__(self, task_manager, task_id):
        self.task_manager = task_manager
        self.task_id = task_id

    def execute(self):
        self.task_manager.remove_task(self.task_id)
        print("[Polecenie] Zadanie usunięte.")

class MarkTaskDoneCommand(Command):
    def __init__(self, task_manager, task_id):
        self.task_manager = task_manager
        self.task_id = task_id

    def execute(self):
        self.task_manager.mark_task_done(self.task_id)
        print("[Polecenie] Zadanie oznaczone jako wykonane.")

# --- WZORZEC DEKORATOR (DECORATOR) ---
# Kornel: Dekorator pozwala dodać np. tag lub notatkę do zadania bez zmiany oryginalnej klasy

class TaskDecorator(Task):
    """Bazowy dekorator zadań - opakowuje inne zadanie."""
    def __init__(self, task):
        self._task = task  # zadanie, które dekorujemy

    def display(self):
        # Wywołuje display oryginalnego zadania
        self._task.display()

    # Przekazujemy pozostałe metody do oryginału (prosty forward)
    def get_id(self):
        return self._task.get_id()

    def get_name(self):
        return self._task.get_name()

    def get_priority(self):
        return self._task.get_priority()

    def is_done(self):
        return self._task.is_done()

    def get_created_at(self):
        return self._task.get_created_at()

class TagDecorator(TaskDecorator):
    """Dekorator dodający tag do zadania."""
    def __init__(self, task, tag):
        super().__init__(task)
        self._tag = tag  # nowy atrybut

    def display(self):
        # Wyświetlamy zadanie z dodatkowym tagiem (np. [Tag: PILNE])
        print(f"{self._task} [Tag: {self._tag}]")