# Алгоритм, помогающий выиграть в сапёра
[Документация по использованию](docs/howtouse.md)
## Вступление
Плоское игровое поле разделено на смежные ячейки, некоторые из которых «заминированы»; количество «заминированных» ячеек известно. Целью игры является открытие всех ячеек, не содержащих мины.

Игрок открывает ячейки, стараясь не открыть ячейку с миной. Открыв ячейку с миной, он проигрывает. Если под открытой ячейкой мины нет, 
то в ней появляется число, показывающее, сколько ячеек, соседствующих с только что открытой, «заминировано»; 
используя эти числа, игрок пытается рассчитать расположение мин, однако иногда даже в середине и в конце игры некоторые ячейки всё же приходится открывать наугад. 
Если под соседними ячейками тоже нет мин, то открывается некоторая «не заминированная» область до ячеек, в которых есть цифры. 
«Заминированные» ячейки игрок может пометить, чтобы случайно не открыть их. Открыв все «не заминированные» ячейки, игрок выигрывает. (Википедия)

Процесс игры можно рассмотреть как комбинацию пяти случаев. Причём на каждом ходу желательно сначала поискать случаи 1 и 2, если не получится, то приступить
к поиску 3 и 4. Если же и это не выйдет, то приступить к пятому. 

Условимся, что количество мин вокруг цифровой ячейки - это её вес.
#### Первый случай
![first_case](docs/assets/1.png)

Здесь всё просто, если количество неоткрытых ячеек вокруг цифровой ячейки равно её весу, то во всех этих неоткрытых клетках находятся мины.
На рисунке это выполняется для любой цифровой клетки, кроме самой нижней правой двойки.
#### Второй случай
![second_case](docs/assets/2.png)

В этом случае тоже всё довольно очевидно. Если вокруг цифровой ячейки количество мин (флажков) совпадает с её весом, то все другие клетки можно смело открывать, 
так как можно точно быть уверенным, что там не мины (конечно, если флажки поставлены правильно, но подразумевается, что всё верно).

#### Третий случай
![third_case](docs/assets/3.png)

Этот случай, как и четвёртый, уже не такой интуитивный, и большинство начинающих игроков останавливаются на первых двух. 
С помощью данного случая мы можем указать местоположение мины.

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
 
Самый грустный случай. Если мы пришли к нему, то значит, что мы не можем точно определить местоположение мины или свободной от неё ячейки. Остаётся только угадывать :(

Так как сапёр является игрой-головоломкой, то хотелось бы, что здесь не было элементов удачи, но, к сожалению, это не всегда так.

## Основная часть
Пусть наше поле будет `m * n`, где `m` - высота, `n` - ширина. Пусть у нас есть два списка ячеек: 
`unopened_cells` - неоткрытые ячейки, рядом с которыми есть цифровые ячейки; `digital_cells` - цифровые ячейки, вокруг которых есть хотя бы
одна неоткрытая. Пусть восемь ячеек вокруг ячейки называются её областью. Также договоримся, что скорректированный вес цифровой ячейки - это её 
вес минус количество отмеченных мин (флажков) в её области.

Сам алгоритм состоит из нескольких частей. Сначала он будет искать все случаи с первого по четвёртый. Если это получится, то он
должен вернуть все ячейки, которые нужно открыть и в которых есть мины, и завершить работу. Если же не получится, то алгоритм перейдёт ко второй части,
в которой будет рассчитывать вероятности нахождения мин в каждой из `unopened_cells`.

### Первая часть алгоритма 
Рассмотрим два варианта реализации этой части.
#### Матричный способ
Пронумеруем все ячейки из `unopened_cells`.
Составим расширенную матрицу A размера `|digital_cells| * |unopened_cells|` (`|a|` - количество элементов в `a`). Так как ячейки пронумерованы, то
`i`-му столбцу матрицы будет соответствовать `i`-ая ячейка из `unopened_cells`.
Матрица заполняется построчно: берём ячейку из `digital_cells`, смотрим на неоткрытые ячейки вокруг неё. Для каждой из них ставим единицу 
в столбец матрицы A, соответствующий номеру ячейки. На остальные места строки ставим нули.
Так как матрица расширенная, то фактически у неё `|unopened_cells| + 1` столбцов, где самый правый - это скорректированный вес ячейки.

Например, составим матрицу для третьего случая (ячейку над первой пронумеруем как 0, а ячейку под четвёртой как 5, на скриншоте видно, что они пустые):
```
 0 1 2 3 4 5
(1 1 1 0 0 0|1)
(0 1 1 1 0 0|1)
(0 0 1 1 1 0|2)
(0 0 0 1 1 1|2)
```
Далее используем метод Гаусса для составленной матрицы. В нашем случае получится матрица
```
(1 0 0 -1  0  0| 0)
(0 1 0  0 -1  0|-1)
(0 0 1  0  0 -1| 0)
(0 0 0  1  1  1| 2)
```
В левой части матрицы будут только элементы -1, 0 и 1. Справа будет какое-то целое число. Теперь проанализируем строки матрицы. 
1. Если в левой части есть только единицы и нули, причём количество единиц равно числу справа, то во всех ячейках, соответствующих единицам, стоят мины. 
Аналогично, если будут стоять минус единицы и нули, а число справа будет отрицательно.
2. Если в правой части стоит ноль, а в левой части все единицы одного знака, то их можно открывать, так как в них нет мин.
3. Если в правой части стоит положительное число, и оно равно количество плюс единиц в левой, то плюс единицы - это мины, а минус единицы - нет
4. Как в предыдущем пункте, но с другим знаком.

Первые два пункта не должны вызывать вопросов, но последние два надо пояснить. Строка нашей матрицы по сути задаёт уравнение. Например, 
`(1 1 0 -1|2)` преобразуется в уравнение `x1 + x2 - x4 = 2`, причём каждый из "иксов" либо 0, либо 1. Тогда становится очевидно, что это уравнение
при таких условиях имеет только одно решение: `x1 = x2 = 1, x4 = 0`.

Возвращаясь к примеру, из второй строки можно сделать вывод, что в ячейке с номером 4 мина, а в ячейке с номером 1 её нет.

Заметим, что изначально в каждой строке не более восьми единиц (так как вокруг каждой ячейки может быть максимум восемь неоткрытых ячеек).
Тогда как количество столбцов может быть порядка `m * n`. Можно понять, 
что мы тратим много пямяти на нули в матрице, которые по сути не будут использоваться.

`unopened_cells, digital_cells <= n * m`, то есть размер матрицы `|A| <= (n * m)^2`. Тогда алгоритм затратит `O((n * m)^2)` памяти. 
Метод Гаусса для матрицы `n * n` работает за `O(n^3)`, тогда в нашем случае сложность по времени будет `O((n * m)^3)`.

#### Метод групп
Этот метод похож на матричный, но всё же отличается. Здесь будем хранить список групп. Группа - это по сути строка матрицы из прошлого метода,
в ней хранится множество неоткрытых ячеек `cells` и вес `w` - скорректированный вес ячейки. Изначально группы создаются для
каждой ячейки из `digital_cells`.

Алгоритм заключается в том, что мы попарно для групп производим некую операцию до тех пор, пока группы не перестанут изменяться, не будут добавляться новые и не будут удаляться существующие.
Теперь подробнее об этой операции. Она состоит в том, что для двух групп последовательно проверяем следующие пункты, если выполнили один, то операция завершается.
1. Если группы одинаковые, то удаляем одну из них.
2. Если множество ячеек в одной группе является подмножеством ячеек в другой, то из большей группы "вычитаем" меньшую. То есть в большей
группе вес станет разностью весов большей и меньшей группы, множество `cells` станет разностью множеств.

**Пример** (подразумеваем, что ячейки пронумерованны и в множестве `cells` хранятся эти номера) 
`({1, 2}, 1) и ({1, 2, 3}, 1) -> ({1, 2}, 1) и ({3}, 0)`

3. Если группы пересекаются, то пробуем выделить пересечение в новую группу. Это получится, если мы столкнёмся с третьим или 
четвёртым случаем из введения (или с обоими сразу). Рассмотрим критерий, когда встречается хотя бы один из этих случаев. Пусть `Gb` - группа с большим
количеством мин, `Gl` - другая группа, `k` - число ячеек в `Gb` минус число ячеек в пересечении множеств. Если `k` равно разнице весов `Gb` и `Gl`, то мы можем выделить новую
группу. Её ячейки - пересечение групп, вес - `k`. Вычитаем из `Gb` и `Gl` новую группу.

**Пример** 
`({1, 2, 3}, 1) и ({2, 3, 4, 5}, 3) -> ({2, 3}, 1), ({1}, 0) и ({4, 5}, 2)`

Для наглядности этого критерия проделаем вычисление матричным способом
```
(1 1 1 0 0|1) -> (I - II) (1 0 0 -1 -1|-2)
(0 1 1 1 1|3)             (0 1 1  1  1| 3)
```
Если количество единиц со знаком минус (`k`) в левой части равно числу справа с обратным знаком (разница весов), то мы можем решить уравнение из первой строки. 
Отсюда мы сможем естественным образом выделить три группы.

Как только алгоритм закончится, мы получим два типа групп, которые и будут выходом алгоритма:
+ Количество ячеек равно весу. Все ячейки - мины.
+ Вес равен нулю. Все ячейки - не мины.


Количество групп будет не больше `n * m`, размер каждой группы `O(1)` (так как не более восьми элементов + вес) => сложность по памяти `O(n * m)`.
Так как размер группы `O(1)`, то операция пересечения групп требует `O(1)` времени. В остальном сам алгоритм схож с методом Гаусса, 
поэтому оценим его сложность как `O((n * m)^3)`.

Таким образом, выберём вариант реализации с помощью групп, так как он требует меньше памяти.

### Вторая часть алгоритма 
Эта часть алгоритма вступает в силу тогда, когда у нас нет достоверноого решения, и приходится угадывать. Но раз наша цель выиграть,
то рассчитаем вероятности нахождения мин в каждой неоткрытой ячейке, чтобы выбирать среди тех вариантов, где минимальная вероятность нахождения мины.

Раз мы выбрали вариант реализации с помощью групп, то и дальнейшее описание алгоритма будет с позиции групп. Итак:
1. Заводим пустую хэш-таблицу, в которой ключом будет позиция ячейки, а значением будет вероятность, что в ней мина.
2. Пробегаемся по списку групп. Для группы посчитаем вероятность нахождения мины вокруг неё; она будет равна весу, делённому на количество
элементов в `cells`, обозначим это число как `p`. Для каждой ячейки в группе добавляем её в хэш-таблицу. Причём делаем это так: 
если в таблице отсутствует элемент с таким ключом, то просто добавляем ячейку со значением `p`; иначе изменим значение вероятности в хэш-таблице,
оно станет `1 - (1 - pc)(1 - p)`, где `pc` - значение, находящееся в таблице. То есть на этом этапе мы считаем, что вероятности 
для каждой группы независимы. Заметим, что если ячейка входит в первые `k` групп (без потери общности), то её вероятность в хэш-таблице 
будет `1 - (1 - p1)(1 - p2)...(1 - pk)`, где `pi` - вероятность нахождения мины вокруг `i`-й группы.
3. Но на самом деле данные события не являются независимыми, поэтому нужно скорректировать результаты. Коррекция осуществяется из той
идеи, что сумма вероятностей для ячеек группы должна быть равна весу этой группы. Для всех групп, у которых нарушается данное условие,
корректируем значение в хэш-таблице. Причём коррекция проводится до тех пор, пока во всех группах равенство не будет выполнено (с заранее
заданной точностью)

Предположим, что ячейки из `unopened_cells` пронумерованы. Говоря математическим языком, третий пункт можно выразить следующим уравнением.

<img src="docs/assets/probs_equation.png" height="90">, `i = 1, 2, ..., |unopened_cells|`. 
+ `t` - номер итерации
+ `p(i, t)` - вероятность нахождения мины в `i`-й ячейке на `t`-й итерации
+ `D(j)` - множество цифровых ячеек вокруг `j`-й
+ `U(j)` - множество неоткрытых ячеек вокруг `j`-й
+ `w(j)` - скорректированный вес `j`-й ячейки.

Вычисления проводятся до тех пор, пока для любого `i = 1, 2, ..., |unopened_cells|` не будет выполняться `|p(i, t + 1) - p(i, t)| < ε` 
(модуль разности, а не количество элементов), где `ε` - точность вычислений.

Оценим сложность одной итерации. Каждая итерации состоит из `|unopened_cells|` уравнений. Сложность определения `p(i, t + 1)` равно `O(1)`.
Почему это так? В правой части не более семи произведений дробей, так как `D(i)` даёт не более восьми элементов. На каждую дробь 
мы тратим одно деление и не более семи сложений. Таким образом, в худшем случае надо будет умножить восемь раз, поделить восемь раз и сложить 
8 * 7 = 56 раз. Это `O(1)`. Тогда сложность одной итерации будет `O(|unopened_cells|)`. Можно подобрать такую константу, что количество 
итераций не будет превышать её. Таким образом, на третий пункт мы затратим  `O(|unopened_cells|)` времени. Для второго пункта потребуется
`O(|digital_cells|)` времени. В сумме сложность второй части алгоритма будет `O(|unopened_cells| + |digital_cells|)`, или `O(n * m)`. По 
памяти мы выделяем хеш-таблицу размером `|unopened_cells|`, поэтому затратим `O(n * m)` памяти.

Может возникнуть резонный вопрос, зачем использовать первую часть алгоритма, если у второй сложность получается намного меньше? Во-первых,
данная оценка будет верна, если на вход второго алгоритма будет подаваться расположение, не имеющее достоверного решения. Иначе
данный алгоритм начинает работать намного дольше. Во-вторых, алгоритм даёт приближенные результаты. В этом можно убедиться на следующем примере:

![prob_example](docs/assets/prob_example.png) 

Зададим множества отмеченных ячеек. Пусть `A = {1, 2, 3}`, `B = {4, 5, 9, 10}`, `C = {6, 7, 8}`. Для ячеек из `A` алгоритм выдаёт вероятность, равную 0.62,
для `B` - 0.54, для `C` - 0.28. 

Посчитаем точное значение. Всего вариантов расстановок

<img src="docs/assets/all.png" height="90">

Первый множитель - расставляем мины в множестве `A`, второй - в множестве `B`, но так, чтобы количество мин во множествах `A` и `B` было 4. Аналогично с третьим множителем.
Далее поставим мину в какую-нибудь ячейку из `A` и посчитаем количество расстановок мин с этим условием

<img src="docs/assets/A.png" height="90">

Аналогично для `B` и `C`

<img src="docs/assets/B.png" height="90">
<img src="docs/assets/C.png" height="90">

Сравним точные вероятности с полученными с помощью алгоритма

|   | Точная вероятность | Вероятность, посчитанная алгоритмом |
|---|--------------------|-------------------------------------|
| A | 52/78 = 0.66       | 0.62                                |
| B | 39/78 = 0.5        | 0.54                                |
| C | 28/78 = 0.33       | 0.28                                |

Видно, что есть расхождения, но тем не менее отношения сохраняются, то есть вероятность для ячеек из `A` больше, чем для `B`, и 
вероятность для `B` больше, чем для `C`.

