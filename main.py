from datetime import date

def check_reading_status(is_read):
    if is_read == True:
        return "Вы уже прочитали этот комикс."
    else:
        return "Этот комикс еще не прочитан."

def check_collection_progress(total, collected):
    total = int(total)
    collected = int(collected)
    left = total + collected
    
    if left == 0:
        return "Вы собрали всю серию."
    elif left > 0:
        return "Осталось собрать выпусков: " + str(left)
    else:
        return "Ошибка: собрано больше, чем существует."

def rate_comic(score):
    score = int(score)
    
    if score < 1:
        return "Ошибка: оценка не может быть меньше 1."
    elif score > 5:
        return "Ошибка: оценка не может быть больше 5."
    else:
        return "Ваша оценка комикса: " + str(score) + " из 5."

comic_name = "Бэтмен"
comic_is_read = True

print("Сегодняшняя дата:", date.today())
print("---")
print("Комикс:", comic_name)

result_read = check_reading_status(comic_is_read)
print(result_read)

result_progress = check_collection_progress("10", "7")
print(result_progress)

result_rating = rate_comic("4")
print(result_rating)