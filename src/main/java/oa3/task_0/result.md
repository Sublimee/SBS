# **Техническое задание на разработку проекта “Шахматы”**

Цель данного документа — описать требования и спецификации для разработки проекта.

**1. Введение**
”Шахматы” — игра, в которой шахматная партия ведётся по классическим правилам шахмат между двумя игроками на виртуальной шахматной доске путём “передвижения” шахматных фигур.

**2. Общие требования**

- Игра должна быть реализована как отдельное приложение на языке Java, запускаемое на любой операционной системе, поддерживающей JVM версии 17 и выше.
- Программа должна быть консольной, то есть интерфейс пользователя реализуется через стандартный текстовый терминал.
- Программа должна позволять двум игрокам играть друг против друга на одном компьютере.

**3. Функциональные требования**

**3.1. Инициализация программы**

- Игроки видят приветствие программы.
- Одновременно с приветствием пользователям предлагается ввести свои никнеймы, которые в дальнейшем будут использоваться для идентификации игроков за игровым полем.
- После заполнения никнеймов пользователи видят приглашение к игре.

3.2. **Инициализация игры**

- При запуске игры пользователи должны видеть шахматную доску с расположенными на ней фигурами.
- Доска должна быть представлена в виде поля 8x8 клеток, где каждая клетка может содержать символ, представляющий шахматную фигуру или быть пустой.
- Каждая горизонталь идентифицируется числом от 1 до 8 в порядке возрастания, а вертикаль — символом от A до H. Каждая клетка должна быть обозначена соответствующим образом для идентификации строки и столбца (например, A1, H8).
- Шахматная доска располагается между игроками таким образом, чтобы в левом нижнем углу располагалось поле A1, а в правом верхнем — H8.
- Фигуры должны быть представлены специальными символами (например, '♔' для короля, '♕' для королевы и т.д.).
- Каждый игрок имеет в распоряжении 16 фигур одного цвета. Белые фигуры располагаются на 1 и 2 горизонталях, а черные на 7 и 8:
    - 8 пешек (размещаются в ряду перед всеми остальными фигурами);
    - 2 ладьи (занимают угловые клетки слева и справа);
    - 2 коня (занимают места рядом с ладьями);
    - 2 слона (занимают места рядом с конями);
    - ферзь (занимает центральную клетку своего цвета);
    - король (занимает место рядом с ферзем).

**3.3. Ход игры**

- Игроки делают ходы по очереди. Программа выводит никнейм пользователя, который должен сделать ход.
    - За исключением рокировки, ходом называется передвижение одной фигуры с одного поля на другое — свободное либо занятое фигурой соперника.
    - Рокировка — ход в шахматах, заключающийся в горизонтальном перемещении короля в сторону ладьи своего цвета на 2 клетки и последующем перемещении ладьи на соседнюю с королём клетку по другую сторону от короля. Каждая из сторон может сделать одну рокировку в течение партии. Рокировка окончательно невозможна, если король во время партии двигался. Также рокировка невозможна с ладьёй, которая уже двигалась. Рокировка временно невозможна, если поле, на котором находится король, или поле, которое он должен пересечь или занять, находится под ударом фигуры соперника. Также рокировка невозможна, если на горизонтали между королём и соответствующей ладьёй есть другая фигура — собственная или фигура соперника.
- Если фигура перемещается на поле, занятое фигурой противника, то фигура противника должна быть заменена текущей фигурой. Такой ход называется взятием. Единственной фигурой, которая не может быть заменена, является король.
- Допускаются следующие ходы фигур:
    - **Король** — за исключением рокировки, передвигается со своего поля на одно из свободных смежных полей, которое не находится под ударом фигур соперника. Рокировка выполняется по правилам, указанным выше.
    - **Ферзь** — ходит по вертикалям, диагоналям и горизонталям, на которых он находится.
    - **Ладья** — ходит по вертикалям и горизонталям, на которых она находится.
    - **Слон** — ходит по диагоналям, на которых он находится.
    - **Конь** — может пойти на одно из полей, ближайших к тому, на котором он стоит, но не на той же самой горизонтали, вертикали или диагонали.
    - **Пешка** — передвигается на одно поле только вперёд, за исключением взятия. Со стартовой позиции пешка может пойти как на одну, так и на две клетки вперёд. Пешка может взять любую фигуру соперника (кроме короля), которая расположена впереди неё на одну клетку по диагонали. Если пешка делает первый ход сразу на две клетки и после хода оказывается в одной горизонтали рядом с пешкой соперника, то она может быть взята этой пешкой; тогда последняя переходит на поле, через которое перешла сбитая пешка. Это взятие называется «взятие на проходе». Оно может быть осуществлено только сразу после того, как соперник сделал такой ход. Любая пешка, достигающая крайней горизонтали, должна быть тем же ходом заменена на ферзя, ладью, слона или коня того же цвета, что и пешка.
- Игрок, играющий белыми фигурами, начинает партию.
- Программа должна запросить у игрока ввод координат откуда и куда хочет переместить фигуру (например, "E2 E4").
- После каждого хода программа должна отображать обновленное состояние доски в консоли.
- Программой должна быть реализована проверка на корректность ходов согласно правилам выше. Некорректные ходы программа опускать не должна. Сообщение о некорректности хода должно быть выведено игрокам.
- Программа должна определять состояние “шах” и оповещать об этом игроков:
    - Шах королю имеет место, когда поле, которое он занимает, оказалось под ударом фигур противника. Шах королю должен быть отражён следующим ходом. Шах можно отбить одним из следующих способов:
        - отойти королём на поле, которое не находится под ударом фигур соперника;
        - взять фигуру, которая угрожает королю;
        - прикрыть короля, поставив другую свою фигуру под удар на поле, находящееся между королём и фигурой, которая его атакует.
    - Второй и третий способ защиты невозможны, если объявлен двойной шах, а также невозможно прикрыть короля фигурой, если атакует конь.
- Если шах невозможно отразить следующим ходом, то объявляется “мат”*.* Программа должна определять состояния “мат” и оповещать об этом игроков.

**3.4. Завершение игры**

- Партия считается выигранной игроком:
    - который дал мат королю соперника;
    - противник которого признал себя побеждённым (сдался).
- Партия заканчивается вничью:
    - В положении, когда возможность выигрыша исключена из-за «мёртвой позиции» (например, недостаточный материал — король против короля, король против короля с конём, король против короля с одним или несколькими однопольными слонами, король со слоном против короля со слоном при однопольных слонах).
    - Если король игрока (при его очереди хода) не находится под шахом и игрок не может сделать ни одного хода. Такое положение называется *патом*.
    - При взаимном согласии игроков.
    - Если одна и та же позиция возникает три раза, причём очередь хода каждый раз принадлежит одному и тому же игроку и, кроме того, во всех случаях имеются абсолютно одинаковые возможности игры (право на рокировку или взятие на проходе).
    - Когда обеими сторонами сделано не менее 50 ходов, в течение которых ни одна фигура не была взята и ни одна пешка не сделала хода.
- Программа должна оповестить игроков о результате партии.
- При завершении игры должна быть возможность начать новую игру или выйти из программы.