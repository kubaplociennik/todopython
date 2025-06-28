# main.py
# Kod napisał Igor

from model import Task, TaskManager, TaskNotFoundException
from patterns import (
    AddTaskCommand, RemoveTaskCommand, MarkTaskDoneCommand,
    SortByPriority, SortByDate, SortByName,
    TagDecorator
)

# Funkcja pozwalająca użytkownikowi wybrać sposób sortowania zadań
def choose_sort_strategy():
    print("\nSortowanie zadań po:")
    print("1. Priorytecie")
    print("2. Dacie utworzenia")
    print("3. Nazwie")
    choice = input("Twój wybór: ")
    if choice == "1":
        return SortByPriority()
    elif choice == "2":
        return SortByDate()
    elif choice == "3":
        return SortByName()
    else:
        print("Nieprawidłowy wybór, domyślnie sortuję po priorytecie.")
        return SortByPriority()

# Menu główne programu - Igor
def main_menu():
    print("\n=== APLIKACJA TO-DO ===")
    print("1. Dodaj zadanie")
    print("2. Usuń zadanie")
    print("3. Oznacz zadanie jako wykonane")
    print("4. Zmień priorytet zadania")
    print("5. Wyświetl wszystkie zadania")
    print("6. Wyświetl zadania (posortowane)")
    print("7. Dodaj tag do zadania (dekorator)")
    print("0. Wyjdź z programu")

# Bezpieczne pobieranie liczby od użytkownika
def get_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Błędna liczba!")
        return None

# Główna pętla programu (CLI)
def run_cli():
    tm = TaskManager()
    while True:
        main_menu()
        choice = input("Wybierz opcję: ")
        if choice == "1":
            # Dodawanie zadania
            name = input("Nazwa zadania: ")
            desc = input("Opis zadania: ")
            prio = get_int("Priorytet (liczba całkowita): ") or 1
            task = Task(name, desc, prio)
            cmd = AddTaskCommand(tm, task)
            cmd.execute()
        elif choice == "2":
            # Usuwanie zadania
            task_id = get_int("ID zadania do usunięcia: ")
            try:
                cmd = RemoveTaskCommand(tm, task_id)
                cmd.execute()
            except TaskNotFoundException as e:
                print(e)
        elif choice == "3":
            # Oznaczanie zadania jako wykonane
            task_id = get_int("ID zadania do oznaczenia jako wykonane: ")
            try:
                cmd = MarkTaskDoneCommand(tm, task_id)
                cmd.execute()
            except TaskNotFoundException as e:
                print(e)
        elif choice == "4":
            # Zmiana priorytetu
            task_id = get_int("ID zadania do zmiany priorytetu: ")
            prio = get_int("Nowy priorytet (liczba całkowita): ") or 1
            try:
                task = tm.find_task(task_id)
                task.set_priority(prio)
                print("Priorytet zadania został zmieniony.")
            except TaskNotFoundException as e:
                print(e)
        elif choice == "5":
            # Wyświetlanie wszystkich zadań
            tasks = tm.list_tasks()
            if tasks:
                for t in tasks:
                    t.display()  # korzystamy z polimorfizmu
            else:
                print("Brak zadań do wyświetlenia.")
        elif choice == "6":
            # Wyświetlanie posortowanych zadań
            strategy = choose_sort_strategy()
            tasks = strategy.sort(tm.list_tasks())
            for t in tasks:
                t.display()
        elif choice == "7":
            # Dodanie tagu do zadania (dekorator)
            task_id = get_int("ID zadania do dekorowania: ")
            tag = input("Podaj tag: ")
            try:
                task = tm.find_task(task_id)
                decorated = TagDecorator(task, tag)
                decorated.display()
            except TaskNotFoundException as e:
                print(e)
        elif choice == "0":
            print("Do zobaczenia!")
            break
        else:
            print("Nieznana opcja. Spróbuj ponownie.")

if __name__ == "__main__":
    run_cli()