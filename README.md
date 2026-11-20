# Лабораторная работа 01 · APPSTAT

**Работу выполнили:**

- **Инфохимики:** Демина Александра — ИСУ 504844; Козлова Дарья — ИСУ 504686.
- **Дизайнеры КТвД:** Аблязизова Ева — ИСУ 504459; Курнакова Валерия — ИСУ 466435.

## Открыть работу

| Материал | Ссылка |
|---|---|
| Интерактивный сайт с графиками и пояснениями | [Открыть сайт APPSTAT](https://leeeeera.github.io/html/APPSTAT_site/) |
| Итоговый ноутбук основной работы | [Посмотреть на GitHub](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/APPSTAT_Lab01_KTvD.ipynb) |
| Запуск и пересчёт ноутбука | [Открыть в Google Colab](https://colab.research.google.com/github/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/APPSTAT_Lab01_KTvD.ipynb) |
| Файлы сайта | [Открыть папку docs](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/tree/main/docs) |

Для знакомства с результатами начните с сайта. Расчёты, код и подробные пояснения находятся в ноутбуках.

## 1. Основная часть — исследование дефектов пластин

Исследуем выбранную подвыборку WM-811K из **15 881 полупроводниковой пластины**. Смотрим, как распределены дефекты, связаны ли их количества в центре и у края и насколько далеко от центра пластины смещён центр дефектов.

### Данные и случайные величины

| Величина | Что измеряем | Исследовательский ноутбук |
|---|---|---|
| `n_center` | Число дефектных чипов в центральной зоне пластины | [n_centerDescription.ipynb](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/n_centerDescription.ipynb) |
| `n_edge` | Число дефектных чипов у края пластины | [rv02_n_edge.ipynb](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/rv02_n_edge.ipynb) |
| `r_def` | Расстояние от центра пластины до центра дефектов, нормированное на радиус пластины | [rv03_r_def.ipynb](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/rv03_r_def.ipynb) |

- [Таблица данных wm811k_features.parquet](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/wm811k_features.parquet).
- [Проверка зависимости величин n_center и n_edge](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/Independence.ipynb).
- [Код расчёта признаков](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/src/features.py).

**Почему выбрали эти данные.** Производство полупроводников связано с химико-технологическими процессами, включая осаждение плёнок. Карты дефектов позволяют исследовать пространственную неоднородность результата производства. При этом сами карты не устанавливают конкретную химическую причину дефекта.

### Что исследуем

**Первый спринт:** природа случайных величин, разведочный анализ данных (EDA), распределения и преобразования, зависимость величин, поведение оценок при увеличении выборки, выборки с возвращением и без, проверка гипотез и выводы.

**Второй спринт:** генератор на основе модели Рэлея для `r_def`, метод обратной функции, математическое обоснование и сравнение с реальными данными.

### Где искать результаты

В [итоговом ноутбуке](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/APPSTAT_Lab01_KTvD.ipynb):

| Раздел | Содержание |
|---|---|
| 01.1–01.4 | Анализ величин и их зависимости |
| 01.5 | Итоговые выводы первого спринта |
| 01.6 | Таблица критериев `cat_mark_table` первого спринта |
| 02.1 | Генератор случайных чисел и его проверка |
| 02.2 | Таблица критериев `cat_mark_table` второго спринта |

Промежуточные выводы расположены рядом с соответствующими расчётами и графиками.

## 2. Часть КТвД — оформление и визуализация основной работы

Исследование представлено в оформленном ноутбуке и на HTML-сайте. Добавлены оглавление, нумерация разделов, навигационные ссылки, скрываемый код в Colab, единый стиль графиков, подписи осей и единиц измерения, формулы LaTeX и пояснения к результатам.

На сайте можно:

- [Посмотреть исходные данные и описание признаков](https://leeeeera.github.io/html/APPSTAT_site/data.html).
- [Изучить связь дефектов в центре и у края](https://leeeeera.github.io/html/APPSTAT_site/dependence.html).
- [Проверить работу генератора](https://leeeeera.github.io/html/APPSTAT_site/generator.html): изменить seed и параметры, сравнить графики и метрики, проследить получение одного случайного числа.
- [Прочитать выводы и посмотреть критерии первого спринта](https://leeeeera.github.io/html/APPSTAT_site/results.html).

В папке [docs](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/tree/main/docs) можно посмотреть файлы сайта: HTML-страницы, стили, скрипты и изображения графиков.

## Список литературы

**Датасет и технологический контекст:**

- [Статья о WM-811K](https://doi.org/10.1109/TSM.2014.2364237).
- [Исследование температурной однородности при LPCVD](https://store.astm.org/stp26035s.html).

<details>
<summary>Литература по генерации случайных чисел</summary>

1. Devroye L. *Non-Uniform Random Variate Generation*. New York: Springer, 1986. [Обзор методов генерации, размещённый автором](https://luc.devroye.org/handbooksimulation1.pdf).
2. Marsaglia G., Tsang W. W. A simple method for generating gamma variables // *ACM Transactions on Mathematical Software*. 2000. Vol. 26, № 3. P. 363–372. [DOI](https://doi.org/10.1145/358407.358414).
3. Vose M. D. A linear algorithm for generating random numbers with a given distribution // *IEEE Transactions on Software Engineering*. 1991. Vol. 17, № 9. P. 972–975. [DOI](https://doi.org/10.1109/32.92917).
4. Walker A. J. An efficient method for generating discrete random variables with general distributions // *ACM Transactions on Mathematical Software*. 1977. Vol. 3, № 3. P. 253–256. [DOI](https://doi.org/10.1145/355744.355749).
5. Knuth D. E. *The Art of Computer Programming*. Vol. 2: *Seminumerical Algorithms*, § 3.4.1.
6. Hörmann W., Leydold J., Derflinger G. *Automatic Nonuniform Random Variate Generation*. Springer, 2004.

</details>

Ссылки по отдельным методам также приведены в ноутбуках и в [разделе «Источники» на сайте](https://leeeeera.github.io/html/APPSTAT_site/sources.html).
