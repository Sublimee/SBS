Существуют ли ситуации, когда связи между модулями должны делаться публичными?

Если говорить о степени проникновения одного модуля в другой, т.е. об импортах, то кажется, что в идеальном варианте модули должны быть абсолютно независимыми. Если модули сильно и много интегрируются друг в друга, то стоит провести работу над переосмыслением их наполнения. Однако мир не такой уж солнечный и приветливый. Если изучить структуру модулей OpenJDK 1.9, то мы увидим и импорты и транзитивные зависимости https://cr.openjdk.org/~mr/jigsaw/jdk9-module-summary.html

Какие метрики вы бы предложили для количественной оценки принципов организации модулей?

Это может быть, например:
1. Число импортируемых модулей
2. Число транзитивных зависимостей (вытекает из п.1)
3. Число других модулей, которые импортируют исследуемый модуль

Если вы разрабатывали программы, в которых было хотя бы 3-5 классов, как бы вы оценили их модульность по этим метрикам?

Вероятно, я бы оценивал, насколько каждая из групп классов (модулей) может существовать автономно от других. Если между этими группами будет высокая связность, то поддерживаемость такого кода будет низкой.