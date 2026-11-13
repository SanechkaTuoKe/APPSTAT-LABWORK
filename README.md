# Лабораторная работа 01 · APPSTAT

**Работу выполнили:**  
**Инфохимики:** Демина Александра — ИСУ 504844; Козлова Дарья — ИСУ 504686.  
**Дизайнеры КТвД:** Аблязизова Ева — ИСУ 504459; Курнакова Валерия — ИСУ 466435.

## Открыть работу

| Раздел | Просмотр и запуск | Файлы на GitHub |
|---|---|---|
| Основное исследование | [Открыть в Colab](https://colab.research.google.com/github/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/APPSTAT_Lab01_KTvD.ipynb) | [Итоговый ноутбук](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/APPSTAT_Lab01_KTvD.ipynb) |
| Оформление основной работы КТвД | [Интерактивный сайт APPSTAT](https://eviavsis.github.io/APPSTAT-site/) | [Главная HTML-страница](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/docs/index.html) |
| Дополнительное задание КТвД | [Запустить в браузере](https://marimo.app/?src=https%3A%2F%2Fraw.githubusercontent.com%2FSanechkaTuoKe%2FAPPSTAT-LABWORK%2Fmain%2F%25D0%2594%25D0%25BE%25D0%25BF%25D0%25BE%25D0%25BB%25D0%25BD%25D0%25B8%25D1%2582%25D0%25B5%25D0%25BB%25D1%258C%25D0%25BD%25D0%25BE%25D0%25B5%2520%25D0%25B7%25D0%25B0%25D0%25B4%25D0%25B0%25D0%25BD%25D0%25B8%25D0%25B5%2520%25D0%259A%25D0%25A2%25D0%25B2%25D0%2594%2Fdigits_marimo.py) | [Исходник marimo](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/%D0%94%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%9A%D0%A2%D0%B2%D0%94/digits_marimo.py) · [HTML-просмотр](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/%D0%94%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%9A%D0%A2%D0%B2%D0%94/digits_marimo_preview.html) |

Для знакомства с результатами откройте сайт; для проверки и повторения расчётов — Colab.

## 1. Основная часть — дефекты полупроводниковых пластин

Исследуем 15 881 пластину из выбранной подвыборки WM-811K: как распределены дефекты и связаны ли их количества в центре и у края.

| Случайная величина | Что измеряем | Исследовательская тетрадь |
|---|---|---|
| `n_center` | Число дефектных чипов в центральной зоне | [n_centerDescription.ipynb](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/n_centerDescription.ipynb) |
| `n_edge` | Число дефектных чипов у края | [rv02_n_edge.ipynb](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/rv02_n_edge.ipynb) |
| `r_def` | Нормированное смещение центра дефектов | [rv03_r_def.ipynb](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/rv03_r_def.ipynb) |

Проверка связи центра и края — [Independence.ipynb](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/Independence.ipynb). В итоговом ноутбуке собраны EDA, распределения, нормализация, исследование оценок и выборок, проверка гипотез и генератор.

**Почему выбрали эти данные.** Производство полупроводников связано с химико-технологическими процессами, включая осаждение плёнок CVD/LPCVD. Например, температура при LPCVD влияет на результат осаждения. Карты WM-811K показывают расположение исправных и дефектных чипов, но не измеряют толщину плёнки и не устанавливают конкретную причину дефекта.

**Где искать итог:** выводы первого спринта — **01.5**, генератор — **02.1**, таблицы критериев `cat_mark_table` — **01.6** и **02.2**.

**Повторный запуск:** в Colab выполните ячейки по порядку. [Таблица данных](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/notebooks/wm811k_features.parquet) загружается автоматически из репозитория. [Расчёт признаков](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/src/features.py) хранится отдельно.

## 2. Часть дизайнеров — представление основной работы

Собрали исследование в оформленный ноутбук и HTML-сайт: оглавление, переходы между разделами, скрываемый код в Colab, единый стиль графиков, подписи единиц измерения и формулы LaTeX. К графикам добавлены пояснения и промежуточные выводы.

- [Генератор на сайте](https://eviavsis.github.io/APPSTAT-site/generator.html): изменение seed и параметров, сравнение графиков и метрик, проверка одного случайного числа. [HTML-файл](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/docs/generator.html).
- [Выводы и критерии первого спринта](https://eviavsis.github.io/APPSTAT-site/results.html). [HTML-файл](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/docs/results.html).

HTML-файлы на GitHub показывают исходный код; для просмотра используйте ссылки на сайт.

## 3. Дополнительное задание КТвД — рукописные цифры

**Выполнили Ева Аблязизова и Валерия Курнакова.**

Отдельное исследование 1 797 изображений из `load_digits`: ширина цифры и число активных ячеек, их зависимость и устойчивость выводов при изменении порога.

В marimo можно выбрать цифру и порог обработки, проверить измерения на изображении, изменить seed и размер выборки генератора ширины. **Генератор и автопроверки — раздел 6, итог — 7, критерии и источники — 8.**

[Инструкция и описание файлов](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/%D0%94%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5%20%D0%B7%D0%B0%D0%B4%D0%B0%D0%BD%D0%B8%D0%B5%20%D0%9A%D0%A2%D0%B2%D0%94/README.md). Интерактивная версия запускается по ссылке в начале README; при первом открытии дождитесь загрузки библиотек. HTML-просмотр нужно скачать и открыть в браузере — он показывает сохранённые результаты без пересчёта.

## Список литературы

<details>
<summary>Литература по генерации случайных чисел</summary>

1. Devroye L. *Non-Uniform Random Variate Generation*. New York: Springer, 1986. [Обзор методов генерации, размещённый автором](https://luc.devroye.org/handbooksimulation1.pdf).
2. Marsaglia G., Tsang W. W. A simple method for generating gamma variables // *ACM Transactions on Mathematical Software*. 2000. Vol. 26, № 3. P. 363–372. [DOI: 10.1145/358407.358414](https://doi.org/10.1145/358407.358414).
3. Vose M. D. A linear algorithm for generating random numbers with a given distribution // *IEEE Transactions on Software Engineering*. 1991. Vol. 17, № 9. P. 972–975. [DOI: 10.1109/32.92917](https://doi.org/10.1109/32.92917).
4. Walker A. J. An efficient method for generating discrete random variables with general distributions // *ACM Transactions on Mathematical Software*. 1977. Vol. 3, № 3. P. 253–256. [DOI: 10.1145/355744.355749](https://doi.org/10.1145/355744.355749).
5. Knuth D. E. *The Art of Computer Programming*. Vol. 2: *Seminumerical Algorithms*, § 3.4.1.
6. Hörmann W., Leydold J., Derflinger G. *Automatic Nonuniform Random Variate Generation*. Springer, 2004.

</details>

О датасете и технологическом контексте: [статья авторов WM-811K](https://doi.org/10.1109/TSM.2014.2364237), [исследование температурной однородности при LPCVD](https://store.astm.org/stp26035s.html). Остальные источники основной работы приведены в [sources.html](https://github.com/SanechkaTuoKe/APPSTAT-LABWORK/blob/main/docs/sources.html), дополнительной — во введении и разделе 8.

