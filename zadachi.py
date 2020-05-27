import random
import os

hero = (
    'Винни-Пуха', 'Пятачка', 'папы', 'мамы', 'мальчика', 'ГуммиБера', 'Цыплёнка', 'девочки', 'тёти', 'дяди', 'Максима',
    'Артёма')

itemsList1 = (
    'карандаш', 'яблоко', 'банан', 'книжка', 'пирог', 'конфета', 'стул', 'шарик', 'ботинок', 'игрушка')
itemsList2 = (
    'карандаша', 'яблока', 'банана', 'книжки', 'пирога', 'конфеты', 'стула', 'шарика', 'ботинка', 'игрушки')
itemsList3 = (
    'карандашей', 'яблок', 'бананов', 'книжек', 'пирогов', 'конфет', 'стульев', 'шариков', 'ботинок', 'игрушек')


run = True
while run:

    item1 = random.randint(1, 15)
    item2 = random.randint(1, 15)

    if item1 == 1:
        chosen_item1 = random.choice(itemsList1)
        k = itemsList1.index(chosen_item1)
    elif item1 < 5:
        chosen_item1 = random.choice(itemsList2)
        k = itemsList2.index(chosen_item1)
    else:
        chosen_item1 = random.choice(itemsList3)
        k = itemsList3.index(chosen_item1)

    if item2 == 1:
        chosen_item2 = itemsList1[k]
    elif item2 < 5:
        chosen_item2 = itemsList2[k]
    else:
        chosen_item2 = itemsList3[k]

    chosen_item3 = itemsList3[k]

    chosen_hero1 = random.choice(hero)
    chosen_hero2 = random.choice(hero)

    while chosen_hero1 == chosen_hero2:
        chosen_hero2 = random.choice(hero)

    str1 = 'У ' + chosen_hero1 + ' было ' + str(item1) + ' ' + chosen_item1 + '. '
    str2 = 'А у ' + chosen_hero2 + ' было ' + str(item2) + ' ' + chosen_item2 + '. '
    str3 = 'Сколько всего ' + chosen_item3 + ' у ' + chosen_hero1 + ' и ' + chosen_hero2 + '?'

    print()
    print(str1 + str2 + str3)

    summa = item1 + item2
    answer = 0
    while answer != summa:
        answer = input('Напиши ответ:')
        try:
            answer = int(answer)
        except:
            print('Надо вводить число. Попробуй ещё раз!')
#            os.system('cls||clear')

            continue
        if answer != summa:
            print('Не правильно. Попробуй ещё раз!')

    print()
    print('Правильно! У {} и {} {} {}.'.format(chosen_hero1, chosen_hero2, summa,
                                               itemsList2[k] if summa < 5 else chosen_item3))
