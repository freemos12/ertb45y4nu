import PySimpleGUI as sg
import random
import json
import os

# Файл для сохранения истории
HISTORY_FILE = "task_history.json"

# Предопределённые задачи с типами
PREDEFINED_TASKS = [
    {"task": "Прочитать статью", "type": "учёба"},
    {"task": "Сделать зарядку", "type": "спорт"},
    {"task": "Проверить почту", "type": "работа"},
    {"task": "Поучить английский", "type": "учёба"},
    {"task": "Пробежка в парке", "type": "спорт"},
    {"task": "Составить отчёт", "type": "работа"}
]

def load_history():
    """Загрузка истории из JSON-файла"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    """Сохранение истории в JSON-файл"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_task(tasks, new_task, task_type):
    """Добавление новой задачи с проверкой на пустоту"""
    if new_task.strip():
        tasks.append({"task": new_task.strip(), "type": task_type})
        return True
    return False

def generate_random_task(tasks):
    """Генерация случайной задачи"""
    return random.choice(tasks) if tasks else None

def filter_tasks(history, filter_type):
    """Фильтрация истории по типу задачи"""
    if filter_type == "все":
        return history
    return [task for task in history if task["type"] == filter_type

def main():
    # Загрузка истории
    history = load_history()
    tasks = PREDEFINED_TASKS.copy()

    # Макет интерфейса
    layout = [
        [sg.Text("Генератор случайных задач", font=("Arial", 16))],
        [sg.Button("Сгенерировать задачу", key="-GENERATE-", size=(20, 2))],
        [sg.Text("Текущая задача:", font=("Arial", 12))],
        [sg.Text("", size=(50, 2), key="-CURRENT-", relief="sunken")],
        [sg.HorizontalSeparator()],
        [sg.Text("Добавить новую задачу:")],
        [sg.Input(key="-NEW_TASK-", size=(40, 1)),
         sg.Combo(["учёба", "спорт", "работа"], default_value="учёба", key="-TASK_TYPE-")],
        [sg.Button("Добавить задачу", key="-ADD-")],
        [sg.HorizontalSeparator()],
        [sg.Text("Фильтр по типу:"),
         sg.Combo(["все", "учёба", "спорт", "работа"], default_value="все", key="-FILTER-", enable_events=True)],
        [sg.Listbox(values=[], size=(60, 10), key="-HISTORY-")],
        [sg.Button("Очистить историю", key="-CLEAR-"), sg.Button("Выход", key="-EXIT-")]
    ]

    window = sg.Window("Random Task Generator", layout, finalize=True)

    # Обновление списка истории
    def update_history_display():
        filter_type = values["-FILTER-"]
        filtered_history = filter_tasks(history, filter_type)
        window["-HISTORY-"].update(
            [f"[{task['type']}] {task['task']}" for task in filtered_history]
        )

    # Основной цикл
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "-EXIT-"):
            break

        elif event == "-GENERATE-":
            task = generate_random_task(tasks)
            if task:
                window["-CURRENT-"].update(task["task"])
                history.append(task)
                save_history(history)
                update_history_display()

        elif event == "-ADD-":
            new_task = values["-NEW_TASK-"]
            task_type = values["-TASK_TYPE-"]
            if add_task(tasks, new_task, task_type):
                window["-NEW_TASK-"].update("")  # Очистка поля ввода
                sg.popup("Задача добавлена!")
            else:
                sg.popup_error("Ошибка: задача не может быть пустой!")

        elif event == "-FILTER-":
            update_history_display()

        elif event == "-CLEAR-":
            history.clear()
            save_history(history)
            update_history_display()

    window.close()

if __name__ == "__main__":
    main()
