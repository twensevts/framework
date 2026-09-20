from storage import load_data, save_data
from series import add_series, get_all_series
from comics import add_comic, mark_as_read
from utils import input_int

FILE_SERIES = "data/series.json"
FILE_COMICS = "data/comics.json"

def show_menu() -> None:
    """Печатает главное меню."""
    print("\n--- Моя коллекция ---")
    print("1. Посмотреть добавленные серии")
    print("2. Добавить новую серию")
    print("3. Добавить выпуск в серию")
    print("4. Отметить выпуск как прочитанный")
    print("0. Выйти")

def main() -> None:
    """Главный цикл программы."""
    series_data = load_data(FILE_SERIES)
    comics_data = load_data(FILE_COMICS)
    
    while True:
        show_menu()
        choice = input("Выберите действие: ")
        
        if choice == "1":
            items = get_all_series(series_data)
            if not items:
                print("Серий пока нет.")
            for s in items:
                print(f"ID серии: {s['id']} | Название: {s['name']}")
                
        elif choice == "2":
            name = input("Название серии: ")
            add_series(series_data, name)
            save_data(FILE_SERIES, series_data)
            print("Серия добавлена.")
            
        elif choice == "3":
            s_id = input_int("Введите ID серии: ")
            issue = input_int("Введите номер тома: ")
            add_comic(comics_data, s_id, issue)
            save_data(FILE_COMICS, comics_data)
            print("Выпуск добавлен.")
            
        elif choice == "4":
            c_id = input_int("Введите ID выпуска: ")
            if mark_as_read(comics_data, c_id):
                save_data(FILE_COMICS, comics_data)
                print("Отмечено как прочитанное!")
            else:
                print("Выпуск с таким ID не найден.")
                
        elif choice == "0":
            break

if __name__ == "__main__":
    main()