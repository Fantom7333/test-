from itertools import tee
#Потом продлим
key_words = ["ООП"]

#Для записи названия в БД
def to_camel_case(word):
    if " " in word:
        spaces = True
    else:
        spaces = False
    #Будет использоваться в БД и url
    word_bd = word.title()
    word_bd = word_bd.replace(' ', '')
    return word_bd


#Для отображения на фронтэнде. Меняет CamelCase на отображение с пробелами.
def for_display(word):
    indexList = [i for i, c in enumerate(word) if c.isupper()]
    #Индекс конца строки. Единицу не отнимаем, потому что этот индекс идёт включительно.
    last_index = len(word)
    indexList.append(last_index)
    indexList.pop(0)
    print(indexList)
    # Первый знак всегда заглавный. Поэтому нам не нужно его рассматривать. Удаляем его индекс из списка.
    word_space = []
    for i in range(len(indexList)):
        if i == 0:
            if indexList[0] == 1:

                word_space.append(word[0:1])

            else:
                word_space.append(word[0:indexList[0]])
        else:

            word_space.append(word[indexList[i-1]:indexList[i]])
    word_space = " ".join(word_space)
    #Преобразуем абривеатуры и тд в нормальный вид.
    for i in key_words:
        if i.capitalize() in word_space:
            word_space = word_space.replace(i.capitalize(), i)
        elif i.lower() in word_space:
            word_space = word_space.replace(i.lower(), i)
        else:
            word_space = word_space
    return word_space

print(for_display("Python"))
