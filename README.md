# Алгоритм, помогающий выиграть в сапёра
## Вступление
Далее я буду подразумевать, что вы знакомы с правилами игры сапёр. Если нет, то ознакомьтесь с ними перед тем, как продолжить чтение.

Процесс игры можно рассмотреть как комбинацию пяти случаев. Причём на каждом ходу желательно сначала поискать случаи 1 и 2, если не получится, то приступить
к поиску 3 и 4. Если же и это не выйдет, то приступить к пятому. 
#### Первый случай
![first_case](docs/assets/1.png)

Здесь всё просто, если количество свободных ячеек вокруг ячейки с цифрой равно самому числу, то во всех этих свободных клетках находятся мины.
На рисунке это выполняется для любой цифровой клетки, кроме самой нижней правой двойки.
#### Второй случай
![second_case](docs/assets/2.png)

В этом случае тоже всё довольно очевидно. Если вокруг цифровой ячейки количество мин совпадает с числом в этой ячейке, то все другие клетки можно смело открывать, так как они не мины

#### Третий случай
![third_case](docs/assets/3.png)

Этот случай, как и четвёртый, уже не такой интуитивный, и большинство начинающих игроков не пользуются ими. Он позволяет указать местоположение мины.

В этом примере нижняя единица даёт информацию, что в ячейках 1, 2 и 3 содержится только одна мина. А это так же значит, что в ячейках 2 и 3 не может быть
две мины. С другой стороны верхняя двойка говорит о том, что в ячейках 2, 3 и 4 должно быть ровно две мины. Но в 2 и 3 может быть только одна мина, 
поэтому делаем заключение о том, что в 4 ячейке точно есть мина. 
#### Четвёртый случай
![fourth_case](docs/assets/4.png)

Данный случай можно рассмотреть как противоположность третьему, он позволяет открыть ячейку, свободную от мины.

Верхняя единица говорит о том, что в ячейках 1, 2 и 3 есть ровно одна мина. Нижняя же подсказывает, что в ячейках 2 и 3 тоже ровно одна мина.
Но раз мина во 2 и 3 ячейках, то в 1 её точно нет.

Третий и четвёрный случай часто идут рука об руку. Так, например, в третьем случае после того, как мы определили, что мина есть в 4 клетке, то верхняя двойка
теперь даёт информацию о том, что в ячейках 2 и 3 ровно одна мина. Тогда уже пользуясь четвёртым случаем заключаем, что в 1 ячейке нет мины.

#### Пятый случай
![fifth_case](docs/assets/5.png)
 
Самый грустный случай. Если мы пришли к нему, то, значит, мы не может точно определить местоположение мины или свободной от неё ячейки. Остаётся только угадывать :(

Так как сапёр является игрой-головоломкой, то хотелось бы, что здесь не было элементов удачи, но, к сожалению, это не так