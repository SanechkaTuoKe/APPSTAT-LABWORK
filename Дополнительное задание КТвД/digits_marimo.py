# /// script
# dependencies = ["marimo", "numpy", "pandas", "matplotlib", "scikit-learn"]
# ///
import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Геометрия рукописных цифр")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    plt.rcParams.update({
        "font.size": 13, "axes.titlesize": 16, "axes.labelsize": 13,
        "figure.facecolor": "#ffffff", "axes.facecolor": "#faf8f1",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#b6bdb6", "text.color": "#192923",
        "axes.labelcolor": "#364a41",
    })
    from sklearn.datasets import load_digits
    return mo, np, pd, plt, Rectangle, load_digits


@app.cell(hide_code=True)
def _(digits, mo):
    _tiles = []
    for _digit in (1, 8):
        _sample = digits.images[(digits.target == _digit).nonzero()[0][0]]
        _pixels = "".join(
            f'<span style="background:rgba(29,98,78,{float(_v)/16:.3f});border-radius:2px"></span>'
            for _v in _sample.flat
        )
        _tiles.append(
            f'<div role="img" aria-label="Рукописная цифра {_digit}" '
            'style="display:grid;grid-template:repeat(8,1fr)/repeat(8,1fr);'
            f'gap:2px;aspect-ratio:1;width:88px;background:#f0f4ee;padding:8px;border-radius:12px">{_pixels}</div>'
        )
    mo.Html("""
    <style>
      .markdown { font-size:18px; line-height:1.65; }
      .markdown h2 { font-size:clamp(24px,4vw,32px); line-height:1.16; letter-spacing:-.02em; }
    </style>
    <section style="background:#faf8f1;color:#192923;border:1px solid #e3e3d7;border-radius:20px;
                    padding:clamp(20px,4vw,42px);font-family:Inter,system-ui,sans-serif;">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:24px;flex-wrap:wrap;">
        <div style="flex:1 1 290px">
          <h1 style="font-size:clamp(34px,6vw,59px);line-height:1.03;letter-spacing:-.045em;margin:0 0 14px;color:#192923">
            Шире — значит<br>больше ячеек?
          </h1>
          <p style="font-size:19px;line-height:1.45;margin:0;max-width:38ch;color:#46584f">
            Сравниваем ширину рамки и число активных ячеек у рукописных цифр.
          </p>
        </div>
        <figure style="flex:0 1 240px;margin:0">
          <div style="display:flex;gap:9px">""" + "".join(_tiles) + """</div>
          <figcaption style="font-size:15px;line-height:1.5;margin-top:12px;color:#46584f">
            Настоящие рукописные «1» и «8» из <code>load_digits</code>, по 8×8 ячеек.
            Зелёный цвет выбран для оформления: чем он насыщеннее, тем выше исходное
            значение ячейки. Здесь показаны первые примеры этих цифр в наборе, без порога.
          </figcaption>
        </figure>
      </div>
      <div style="border-top:1px solid #dedfd3;margin-top:25px;padding-top:14px;font-size:15px;color:#46584f">
        Валерия Курнакова · ИСУ 466435 &nbsp; / &nbsp; Ева Аблязизова · ИСУ 504459
      </div>
    </section>
    """)
    return


@app.cell(hide_code=True)
def _(load_digits):
    digits = load_digits()
    return (digits,)


@app.cell(hide_code=True)
def _(digits, mo, np):
    _missing = int(np.isnan(digits.images).sum())
    _counts = np.bincount(digits.target)
    mo.md(f"""
    **По разделам:** [Данные](#data) · [Измерения](#measure) · [Графики](#eda) ·
    [Связь](#test) · [Отдельные цифры](#groups) · [Пороги](#thresholds) ·
    [Генератор](#generator) · [Итог](#resume) · [Критерии](#criteria)

    <span id="data"></span>
    ## Откуда взялись изображения

    Используем **{len(digits.images):,} рукописных цифр от 0 до 9** из
    [`sklearn.datasets.load_digits`](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.load_digits.html).
    Это копия тестовой части набора UCI Optical Recognition of Handwritten Digits.
    Изображения загружаются вместе со scikit-learn; отдельный файл с картинками не нужен.

    В исходном наборе изображения 32×32 сведены к сетке **8×8**: каждая ячейка хранит число
    закрашенных пикселей в блоке 4×4, от **0 до 16**.
    На странице это значение передаётся насыщенностью цвета и для краткости называется
    «яркостью». Поэтому здесь измеряем **ячейки сетки**, а не миллиметры или количество движений руки.
    [Описание подготовки данных](https://scikit-learn.org/stable/datasets/toy_dataset.html#optical-recognition-of-handwritten-digits-dataset).

    **Проверка перед анализом.** Пропусков в изображениях: **{_missing}**;
    на каждую цифру приходится от **{_counts.min()} до {_counts.max()}** примеров.
    Используем все изображения. Ширину и число активных ячеек рассчитываем сами;
    метка цифры уже есть в наборе.

    **Вопрос исследования:** сопровождается ли более широкая форма большим числом
    заполненных ячеек? Для дизайна это способ разделить ширину знака и его визуальную
    заполненность. Число активных ячеек — лишь простая мера заполненности, а не оценка читаемости.
    """.replace("1,797", "1 797"))
    return


@app.cell(hide_code=True)
def _(digits, pd, cutoff):
    mask = digits.images >= cutoff
    assert mask.any(axis=(1, 2)).all()
    left = mask.any(axis=1).argmax(axis=1)
    right = 7 - mask.any(axis=1)[:, ::-1].argmax(axis=1)
    table = pd.DataFrame({
        "digit": digits.target,
        "width": right - left + 1,
        "ink": mask.sum(axis=(1, 2)),
    })
    return left, table


@app.cell(hide_code=True)
def _(mo):
    choice = mo.ui.radio(
        options=["Все цифры"] + [str(i) for i in range(10)],
        value="Все цифры", label="Выбери цифру", inline=True,
    )
    threshold = mo.ui.radio(["3", "4", "5"], value="4", label="Порог яркости", inline=True)
    mo.vstack([mo.md('<span id="measure"></span>\n\n## 1. Как измеряем цифры'),
               mo.md("**Выбор цифры** задаёт группу для примеров, графиков и проверки связи. "
                     "**Порог** задаёт, какие ячейки считать активными: значение должно быть не ниже порога. "
                     "При переходе от 4 к 3 учитываем больше слабых фрагментов; при переходе к 5 — меньше. "
                     "После изменения выбора результаты пересчитываются. Цифры в шапке остаются прежними."),
               choice, threshold,
               mo.md(r"""
               Из каждого изображения получаем две **дискретные случайные величины**:

               | Величина | Что именно считаем | Единица |
               |---|---|---|
               | $W$ — ширина | Расстояние от крайнего левого до крайнего правого активного столбца, включая оба края | Ячейки по горизонтали |
               | $A$ — заполненность | Число всех ячеек со значением не ниже порога, включая раздельные фрагменты | Активные ячейки |

               **Почему случайные?** Мысленно выбираем одно изображение из текущей группы
               равновероятно. До выбора $W$ и $A$ неизвестны, потому что начертания отличаются.
               Для уже выбранной картинки расчёт однозначен: случайность относится к выбору
               изображения, а не к формуле измерения. В анализе ниже считаем признаки для всей группы.
               """)])
    return choice, threshold


@app.cell(hide_code=True)
def _(threshold):
    cutoff = int(threshold.value)
    return (cutoff,)


@app.cell(hide_code=True)
def _(choice, table):
    subset = table if choice.value == "Все цифры" else table[table.digit == int(choice.value)]
    return (subset,)


@app.cell(hide_code=True)
def _(Rectangle, digits, left, mo, np, plt, subset, cutoff):
    _fig, _axes = plt.subplots(1, 4, figsize=(9, 2.6), layout="constrained")
    ordered = subset.sort_index()
    examples = ordered.iloc[np.linspace(0, len(ordered)-1, 4, dtype=int)]
    for ax, (idx, row) in zip(_axes, examples.iterrows()):
        active = digits.images[idx] >= cutoff
        ys, xs = np.where(active)
        ax.imshow(np.where(active, digits.images[idx], 0), cmap="Greys", vmin=0, vmax=16)
        ax.add_patch(Rectangle((left[idx]-.5, ys.min()-.5), row.width, ys.max()-ys.min()+1,
                               fill=False, color="#007c83", linewidth=2, clip_on=False))
        ax.set_title(f"Цифра {row.digit} · № {idx}\nW = {row.width}, A = {row.ink}")
        ax.axis("off")
    plt.close(_fig)
    _first_idx = int(examples.index[0])
    _first_mask = digits.images[_first_idx] >= cutoff
    _row_counts = _first_mask.sum(axis=1)
    _first_left = int(left[_first_idx]) + 1
    _first_right = _first_left + int(examples.iloc[0].width) - 1
    mo.vstack([_fig, mo.md(
        f"**Как читать примеры.** При пороге **{cutoff}** ячейки ниже порога показаны белым, "
        "а оставшиеся — оттенками серого. Бирюзовая рамка охватывает все активные ячейки. "
        "№ — индекс изображения в исходном наборе, начиная с нуля. "
        "Четыре примера взяты через равные интервалы по порядку внутри выбранной группы; "
        "они иллюстрируют измерение, а статистики ниже рассчитаны по всей группе."
    ), mo.accordion({
        f"Проверить расчёт вручную · изображение № {_first_idx}": mo.md(
            f"Считаем столбцы слева направо от 1 до 8. Крайние активные столбцы — "
            f"**{_first_left}** и **{_first_right}**, поэтому ширина "
            f"**W = {_first_right} − {_first_left} + 1 = {int(examples.iloc[0].width)}**.\n\n"
            "Число активных ячеек в каждой строке, сверху вниз: "
            + " + ".join(str(v) for v in _row_counts)
            + f" = **{int(_row_counts.sum())}**. Это значение **A**."
        )
    }), mo.md(
        "**Что это даёт.** Ширина учитывает только крайние столбцы, а заполненность — "
        "всё внутри рамки. Поэтому эти признаки описывают разные стороны формы; "
        "дальше проверим, как они связаны."
    )])
    return


@app.cell(hide_code=True)
def _(choice, cutoff, mo, np, pd, plt, subset):
    _fig, _axes = plt.subplots(1, 3, figsize=(12, 3.5), layout="constrained")
    _axes[0].hist(subset.width, bins=np.arange(.5, 9.5), color="#007c83", rwidth=.8)
    _axes[0].set(xlabel="Ширина рамки, ячеек", ylabel="Изображений", xlim=(.5, 8.5), xticks=range(1, 9))
    _axes[1].hist(subset.ink, bins=np.arange(-.5, 65.5, 3), color="#c46d3b")
    _axes[1].set(xlabel="Активных ячеек", ylabel="Изображений", xlim=(0, 64))
    counts = subset.groupby(["width", "ink"]).size().reset_index(name="count")
    dots = _axes[2].scatter(counts.width, counts.ink, c=counts["count"], cmap="cividis", s=28)
    _axes[0].set_title("Ширина рамки")
    _axes[1].set_title("Заполненность")
    _axes[2].set_title("Связь признаков")
    _fig.colorbar(dots, ax=_axes[2], label="Изображений в точке")
    _axes[2].set(xlabel="Ширина рамки, ячеек", ylabel="Активных ячеек", xticks=range(1, 9), xlim=(.5, 8.5), ylim=(0, 64))
    plt.close(_fig)
    summary = subset[["width", "ink"]].agg(["min", "median", "max"]).T
    summary["IQR"] = subset[["width", "ink"]].quantile(.75) - subset[["width", "ink"]].quantile(.25)
    summary.index = ["Ширина", "Активные ячейки"]
    summary.columns = ["Минимум", "Медиана", "Максимум", "Межквартильный размах"]
    cards = mo.hstack([
        mo.stat(value=str(len(subset)), label="Изображений"),
        mo.stat(value=f"{subset.width.median():g}", label="Медианная ширина"),
        mo.stat(value=f"{subset.ink.median():g}", label="Медиана активных ячеек"),
    ], wrap=True, justify="space-between")
    _same_width = subset.groupby("width").ink.nunique()
    _most_varied_width = int(_same_width.idxmax())
    _different_ink = int(_same_width.max())
    _width_note = (
        f"Например, при ширине **{_most_varied_width}** встречается **{_different_ink}** "
        "разных значений заполненности. Одинаковая ширина не задаёт число активных ячеек однозначно."
        if _different_ink > 1 else
        "В текущей группе каждой наблюдаемой ширине соответствует одно значение заполненности."
    )
    mo.vstack([mo.md('<span id="eda"></span>\n\n## 2. Что видно на графиках'),
               mo.md(f"**Сейчас:** {choice.value.lower()}, порог **{cutoff}**. "
                     "Один объект наблюдения — одно изображение."), cards, _fig,
               mo.md("**Слева и в центре** высота столбца — число изображений: "
                     "ширина сгруппирована по одной ячейке, заполненность — по три. "
                     "**Справа** точка обозначает сочетание ширины и заполненности. "
                     "Совпадающие наблюдения объединены, а их число показано цветом по шкале рядом. "
                     "Диапазоны признаков на осях сохраняются при переключении цифры; "
                     "высота столбцов зависит и от размера группы."),
               mo.ui.table(summary, selection=None),
               mo.md("**Как читать таблицу.** Медиана делит упорядоченные наблюдения пополам. "
                     "Межквартильный размах — разность 75-го и 25-го процентилей: "
                     "он показывает разброс центральной половины значений. Минимум и максимум — наблюдаемые границы."),
               mo.md(f"**Промежуточный вывод.** Типичная ширина — **{subset.width.median():g}** ячеек, "
                     f"а типичное число активных ячеек — **{subset.ink.median():g}** (медианы). "
                     + _width_note + " График показывает структуру данных; наличие зависимости проверим отдельно.")])
    return


@app.cell(hide_code=True)
def _(np):
    def independence(frame):
        w, a = frame.width.to_numpy(), frame.ink.to_numpy()
        _, wi = np.unique(w, return_inverse=True)
        _, ai = np.unique(a, return_inverse=True)
        rows, cols = wi.max()+1, ai.max()+1
        if min(rows, cols) < 2:
            return None
        def counts(labels):
            return np.bincount(wi*cols + labels, minlength=rows*cols).reshape(rows, cols)
        observed = counts(ai)
        expected = np.outer(observed.sum(1), observed.sum(0)) / len(frame)
        def statistic(grid):
            return (((grid - expected)**2) / expected).sum()
        real = statistic(observed)
        rng = np.random.default_rng(42)
        exceed = sum(statistic(counts(rng.permutation(ai))) >= real - 1e-10 for _ in range(1999))
        rho = frame.width.rank().corr(frame.ink.rank())
        return real, (exceed+1)/2000, rho
    return (independence,)


@app.cell(hide_code=True)
def _(independence, mo, subset):
    selected_test = independence(subset)
    if selected_test is None:
        interpretation = "В выбранной группе один из признаков постоянен, поэтому тест не применяем."
    else:
        stat, p, rho = selected_test
        decision = ("отвергаем гипотезу независимости" if p < .05
                    else "не нашли достаточных оснований отвергнуть независимость")
        interpretation = f"χ² = **{stat:.1f}**, p = **{p:.4f}**, коэффициент Спирмена = **{rho:.2f}**. При уровне 0,05 {decision}."
    mo.md(f"""
    <span id="test"></span>

    ## 3. Проверка независимости

    **Проверяем две величины на одних и тех же изображениях.** Нулевая гипотеза:
    ширина и заполненность независимы. Альтернатива: между ними есть зависимость.
    Уровень значимости — **0,05**.

    Перемешиваем значения заполненности между изображениями, сохраняя ширины.
    Так разрушаем исходные пары, но сохраняем распределение каждого признака.
    Сравниваем исходную статистику χ² с результатами **1 999 перестановок**.
    χ² измеряет расхождение между наблюдаемыми частотами пар и частотами, ожидаемыми при независимости.
    p-значение получаем из перестановок, поэтому не используем приближение распределением χ²
    для редких сочетаний. Фиксированный seed = 42 делает расчёт воспроизводимым.

    **Результат для текущего выбора.** {interpretation}

    **Как понимать числа.** Малое p означает, что такое или большее расхождение редко
    возникает при перестановках. Это не вероятность истинности гипотезы.
    Коэффициент Спирмена лежит от −1 до 1: знак показывает направление монотонной связи,
    а модуль — её выраженность. Значение около нуля само по себе не доказывает независимость.
    Если p ≥ 0,05, это тоже не доказательство независимости: оснований отвергнуть её недостаточно.

    **Промежуточный вывод.** Решение теста отвечает на вопрос о зависимости,
    а Спирмен помогает понять её направление. Эти числа нужно читать вместе.

    Число активных ячеек ограничено площадью рамки: при высоте изображения 8 оно не превышает
    восьми ширин (A ≤ 8W). Это геометрическое ограничение, но само по себе оно не заменяет тест.
    Даже если связь
    видна, из неё нельзя сделать вывод о том, как человек писал цифру.
    """)
    return (selected_test,)


@app.cell(hide_code=True)
def _(cutoff, independence, mo, pd, table):
    rows = []
    for label, frame in [("Все", table), *list(table.groupby("digit"))]:
        _result = independence(frame)
        if _result is not None:
            rows.append([str(label), len(frame), _result[2], _result[1]])
    results = pd.DataFrame(rows, columns=["Цифра", "Изображений", "Спирмен", "p перестановок"])
    strongest = results.iloc[1:].sort_values("Спирмен", ascending=False).iloc[0]
    weakest = results.iloc[1:].sort_values("Спирмен").iloc[0]
    mo.vstack([mo.md('<span id="groups"></span>\n\n## 4. Что меняется внутри отдельных цифр'),
        mo.md(f"**Зачем разделять цифры.** Связь по всему набору может отличаться от связи внутри "
              f"одного начертания. Здесь всегда показаны **все десять цифр при текущем пороге {cutoff}**; "
              "выбор отдельной цифры сверху эту таблицу не фильтрует. Строка «Все» объединяет набор, "
              "остальные строки — группы по метке цифры. p — результат той же перестановочной проверки."),
        mo.ui.table(results.round(4), selection=None),
        mo.md(f"**Промежуточный вывод.** По всем изображениям коэффициент Спирмена равен **{results.iloc[0]['Спирмен']:.2f}**. "
              f"Внутри цифры **{strongest['Цифра']}** он равен **{strongest['Спирмен']:.2f}**, "
              f"а внутри **{weakest['Цифра']}** — **{weakest['Спирмен']:.2f}**. "
              "По таблице видно, как меняются направление и сила связи между группами. Переключатель позволяет увидеть их на одних и тех же шкалах. "
              "Проверки по десяти цифрам носят разведочный характер: p-значения приведены без поправки на множественные сравнения. "
              "Поэтому отдельные строки используем для поиска особенностей, а не как десять независимых подтверждений общего вывода.")])
    return


@app.cell(hide_code=True)
def _(choice, digits, independence, mo, pd, plt, cutoff):
    _rows = []
    for _level in (3, 4, 5):
        _mask = digits.images >= _level
        _occupied = _mask.any(axis=1)
        _width = 8 - _occupied.argmax(axis=1) - _occupied[:, ::-1].argmax(axis=1)
        _data = pd.DataFrame({"width": _width, "ink": _mask.sum(axis=(1, 2))})
        if choice.value != "Все цифры":
            _data = _data[digits.target == int(choice.value)]
        _test = independence(_data)
        _rows.append([_level, _data.width.median(), _data.ink.median(),
                      _test[2] if _test else float("nan"), _test[1] if _test else float("nan")])
    _comparison = pd.DataFrame(_rows, columns=["Порог", "Медиана ширины",
                                              "Медиана активных ячеек", "Спирмен", "p перестановок"])
    _fig, _ax = plt.subplots(figsize=(8, 2.8), layout="constrained")
    _ax.plot(_comparison["Порог"], _comparison["Спирмен"], "o-", color="#007c83")
    _ax.axvline(cutoff, color="#c46d3b", linestyle="--", label="Выбранный порог")
    _ax.axhline(0, color="#919aa8", linewidth=1)
    _ax.set(xticks=[3, 4, 5], ylim=(-1, 1), xlabel="Порог яркости", ylabel="Спирмен")
    _ax.legend(loc="lower right")
    plt.close(_fig)
    _rho = _comparison["Спирмен"]
    if _rho.isna().any():
        _conclusion = "При одном из порогов признак постоянен, поэтому коэффициент для него не определён."
    elif (_rho > 0).all() or (_rho < 0).all():
        _conclusion = f"Направление связи сохраняется при всех трёх порогах. Коэффициент Спирмена меняется от {_rho.min():.2f} до {_rho.max():.2f}."
    else:
        _conclusion = "Направление связи чувствительно к порогу. Сравни точки относительно нулевой линии."
    _p = _comparison["p перестановок"]
    if (_p < .05).all():
        _conclusion += " При каждом пороге перестановочный тест даёт p < 0,05."
    threshold_comparison = _comparison
    threshold_conclusion = _conclusion
    mo.vstack([mo.md(f'<span id="thresholds"></span>\n\n## 5. Что меняется при смене порога · {choice.value}'),
               mo.md("**Зачем повторять расчёт.** Порог 4 — исходное правило измерения, а 3 и 5 — "
                     "два соседних варианта. Проверяем, насколько вывод зависит от этого выбора. "
                     "Во всех трёх случаях используем одни и те же изображения выбранной группы."),
               _fig,
               mo.md("**Как читать график.** Каждая точка — коэффициент Спирмена при одном пороге. "
                     "Линия соединяет три проверенных значения; между ними дополнительных расчётов нет. "
                     "Оранжевый пунктир отмечает текущий порог. Горизонтальная линия на нуле отделяет "
                     "положительную связь от отрицательной."),
               mo.ui.table(_comparison.round(4), selection=None),
               mo.md("**Промежуточный вывод.** " + _conclusion),
               mo.md("При повышении порога у каждого изображения число активных ячеек и ширина "
                     "не могут вырасти: часть ячеек перестаёт учитываться. Но сила связи между "
                     "признаками может измениться. Это проверка устойчивости на трёх выбранных "
                     "порогах, а не гарантия для любого способа обработки изображений.")])
    return threshold_comparison, threshold_conclusion


@app.cell(hide_code=True)
def _(np):
    def inverse_discrete(values, probabilities, uniforms):
        """Map U in [0, 1) to a discrete distribution, including exact boundaries."""
        values = np.asarray(values)
        probabilities = np.asarray(probabilities, dtype=float)
        uniforms = np.asarray(uniforms, dtype=float)
        if (values.ndim != 1 or not len(values) or probabilities.shape != values.shape
                or not np.isfinite(values).all() or not (np.diff(values) > 0).all()
                or not np.isfinite(probabilities).all() or (probabilities < 0).any()
                or not np.isclose(probabilities.sum(), 1, rtol=0, atol=1e-12)):
            raise ValueError("Нужны возрастающие значения и вероятности с суммой 1.")
        if not np.isfinite(uniforms).all() or ((uniforms < 0) | (uniforms >= 1)).any():
            raise ValueError("Равномерные числа должны принадлежать [0, 1).")
        cdf = np.cumsum(probabilities / probabilities.sum())
        cdf[-1] = 1.0
        return values[np.searchsorted(cdf, uniforms, side="right")]

    def generate_widths(reference_widths, size, seed):
        reference_widths = np.asarray(reference_widths)
        if (reference_widths.ndim != 1 or not reference_widths.size
                or not np.isfinite(reference_widths).all()
                or not np.isin(reference_widths, np.arange(1, 9)).all()):
            raise ValueError("Ширины должны быть целыми числами от 1 до 8.")
        if not isinstance(size, (int, np.integer)) or size < 1:
            raise ValueError("Размер выборки должен быть положительным целым числом.")
        if not isinstance(seed, (int, np.integer)) or seed < 0:
            raise ValueError("Seed должен быть неотрицательным целым числом.")
        values, counts = np.unique(reference_widths, return_counts=True)
        probabilities = counts / counts.sum()
        uniforms = np.random.default_rng(seed).random(size)
        generated = inverse_discrete(values, probabilities, uniforms)
        return generated, uniforms, values, probabilities
    return generate_widths, inverse_discrete


@app.cell(hide_code=True)
def _(mo):
    generator_seed = mo.ui.number(0, 2147483647, step=1, value=42, debounce=True, label="Seed генератора")
    generator_size = mo.ui.slider(50, 10000, step=50, value=1000, debounce=True,
                                  show_value=True, include_input=True, label="Сколько значений получить")
    mo.vstack([
        mo.md(r"""
        <span id="generator"></span>

        ## 6. Собираем случайную выборку ширины

        **Теперь генерируем новые числа по измеренным частотам.** Например, если ширина 6
        встретилась в половине изображений, генератор должен выдавать 6 с вероятностью 1/2.
        Используем **метод обратной функции для дискретного эмпирического распределения**.

        Группа цифр и порог берутся из переключателей в разделе 1. Здесь можно менять
        **seed** (он задаёт последовательность) и **размер выборки**. При одном seed
        первые значения сохраняются при увеличении размера. После ввода seed нажмите Enter
        или уберите фокус с поля; ползунок пересчитывает результат после отпускания.
        """),
        mo.hstack([generator_seed, generator_size], wrap=True, justify="start"),
        mo.accordion({"6.1. Почему этот способ даёт нужные вероятности": mo.md(r"""
        Пусть в текущей группе $N$ изображений. Различные ширины упорядочены:
        $w_1<\cdots<w_k$. Частоту каждой ширины превращаем в вероятность:

        $$\widehat p_j=\frac{n_j}{N},\qquad C_0=0,\quad C_j=\sum_{i=1}^j\widehat p_i.$$

        Делим отрезок вероятностей на участки длиной $\widehat p_j$. Получаем
        $U\sim\mathcal U[0,1)$ и выбираем тот участок, в который попало число:

        $$\widetilde W=w_j\quad\text{при}\quad C_{j-1}\le U<C_j.$$

        Почему это работает: для равномерного числа вероятность попасть в участок равна
        его длине. Поэтому $P(\widetilde W=w_j)=C_j-C_{j-1}=\widehat p_j$.
        Это дискретное квантильное преобразование. В коде нужный участок ищет
        `searchsorted(..., side="right")`; равномерные числа даёт `numpy.random.default_rng`.
        Если число точно равно границе, выбирается следующий участок; $U=1$ не допускается.

        Это выборка **с возвращением** из эмпирического распределения: число можно получить
        снова, исходные частоты при генерации не уменьшаются. Точные среднее и дисперсия модели:

        $$\mu=\sum_j w_j\widehat p_j,\qquad
        \sigma^2=\sum_j(w_j-\mu)^2\widehat p_j.$$

        Генератор воспроизводит распределение ширины в выбранных данных. Он **не рисует
        новые изображения** и не моделирует совместно ширину и заполненность.
        """)})
    ])
    return generator_seed, generator_size


@app.cell(hide_code=True)
def _(generate_widths, generator_seed, generator_size, mo, np, subset):
    mo.stop(generator_seed.value is None, mo.md("Введите целое значение seed от 0 до 2147483647."))
    generated_widths, generated_u, width_values, width_probabilities = generate_widths(
        subset.width.to_numpy(), int(generator_size.value), int(generator_seed.value)
    )
    width_cdf = np.cumsum(width_probabilities)
    width_cdf[-1] = 1.0
    return generated_u, generated_widths, width_cdf, width_probabilities, width_values


@app.cell(hide_code=True)
def _(generated_u, generated_widths, mo, np, plt, width_cdf, width_values):
    _u = float(generated_u[0])
    _width = int(generated_widths[0])
    _j = int(np.searchsorted(width_cdf, _u, side="right"))
    _lo = float(width_cdf[_j-1]) if _j else 0.0
    _hi = float(width_cdf[_j])
    _fig, _ax = plt.subplots(figsize=(8, 3.5), layout="constrained")
    _ax.step(np.r_[0, width_values, 8.5], np.r_[0, width_cdf, 1], where="post", color="#007c83")
    _ax.axhspan(_lo, _hi, color="#007c83", alpha=.10)
    _ax.hlines(_u, 0, _width, color="#c46d3b", linestyles="--")
    _ax.vlines(_width, 0, _u, color="#c46d3b", linestyles="--")
    _ax.scatter([_width], [_u], color="#c46d3b", s=65, zorder=4)
    _ax.set(xlim=(0, 8.5), ylim=(0, 1.04), xticks=range(1, 9),
            xlabel="Ширина, ячеек", ylabel="Накопленная вероятность", title="От случайного u к ширине")
    plt.close(_fig)
    mo.vstack([
        mo.md("### 6.2. Одно число можно проверить по графику"), _fig,
        mo.md(f"**Первое число:** u = **{_u:.6f}**. Оно попало в участок "
              f"**[{_lo:.6f}; {_hi:.6f})**, поэтому получилась ширина **{_width}** ячеек. "
              "Границы в подписи округлены; код сравнивает неокруглённые значения."),
        mo.md("**Как читать.** Бирюзовая ступенчатая линия — накопленная вероятность. "
              "От u на вертикальной оси идём вправо до первого скачка выше u, затем вниз "
              "к ширине на горизонтальной оси. Оранжевая точка стоит на пути преобразования, "
              "а не обозначает ещё одно наблюдение в исходном наборе. Смените seed и повторите проверку.")
    ])
    return


@app.cell(hide_code=True)
def _(choice, cutoff, generated_widths, generator_seed, mo, np, pd, plt,
      subset, width_probabilities, width_values):
    _n = len(generated_widths)
    _axis = np.arange(1, 9)
    _real_p = np.bincount(subset.width.to_numpy(), minlength=9)[1:9] / len(subset)
    _generated_p = np.bincount(generated_widths, minlength=9)[1:9] / _n
    _mean = float(np.dot(width_values, width_probabilities))
    _sd = float(np.sqrt(np.dot((width_values-_mean)**2, width_probabilities)))
    _sample_mean = float(generated_widths.mean())
    _sample_sd = float(generated_widths.std(ddof=0))
    generator_tv = float(np.abs(_real_p-_generated_p).sum()/2)
    _metrics = pd.DataFrame({
        "Метрика": ["Среднее, ячеек", "Стандартное отклонение, ячеек"],
        "Исходные данные / модель": [_mean, _sd],
        "Сгенерированная выборка": [_sample_mean, _sample_sd],
        "Абсолютное отличие": [abs(_sample_mean-_mean), abs(_sample_sd-_sd)],
    })
    _fig, _ax = plt.subplots(figsize=(8, 3.5), layout="constrained")
    _ax.bar(_axis-.18, _real_p, width=.36, color="#007c83", label="Исходные частоты")
    _ax.bar(_axis+.18, _generated_p, width=.36, color="#c46d3b", label="Генератор")
    _ax.set(xlim=(.5, 8.5), ylim=(0, 1), xticks=range(1, 9), xlabel="Ширина, ячеек",
            ylabel="Доля значений", title="Повторяет ли выборка исходное распределение?")
    _ax.legend()
    plt.close(_fig)
    _freq = pd.DataFrame({"Ширина, ячеек": _axis, "Исходная доля": _real_p,
                          "Доля в генерации": _generated_p})
    generator_summary = (
        f"Для группы «{choice.value}» при пороге {cutoff} получено {_n} значений "
        f"(seed {int(generator_seed.value)}). Среднее исходных данных — {_mean:.3f}, "
        f"сгенерированных — {_sample_mean:.3f} ячейки; стандартное отклонение — "
        f"{_sd:.3f} и {_sample_sd:.3f}. Расстояние по полным частотам TV = {generator_tv:.4f}."
    )
    mo.vstack([
        mo.md(f"### 6.3. Сравниваем всю выборку\n\n**Сейчас:** {choice.value.lower()}, "
              f"порог **{cutoff}**, seed **{int(generator_seed.value)}**, **{_n}** сгенерированных значений."),
        _fig,
        mo.md("**Почему доли, а не количество.** Исходных изображений и новых значений может "
              "быть разное число. Доли позволяют сравнить форму распределений на одной шкале от 0 до 1."),
        mo.ui.table(_metrics.round(4), selection=None),
        mo.accordion({"Частоты для каждой ширины": mo.ui.table(_freq.round(4), selection=None)}),
        mo.md(r"""
        **Что проверяем.** Среднее и разброс показывают две стороны совпадения, а
        расстояние $TV=\frac12\sum_w|\widehat p_w-\widetilde p_w|$ сравнивает все частоты.
        Оно лежит от 0 до 1; ноль означает точное совпадение частот. Здесь стандартное
        отклонение в обеих колонках описательное: с делением на число значений (`ddof=0`).
        """),
        mo.md("**Промежуточный вывод.** " + generator_summary),
        mo.md("У конечной случайной выборки частоты колеблются. Совпадение закона генерации "
              "обосновано в разделе 6.1, а эта таблица показывает отклонения конкретного запуска. "
              "Попробуйте 100 и 10 000 значений при нескольких seed: с ростом размера "
              "ошибка обычно уменьшается, но для одной последовательности это не обязано "
              "происходить на каждом шаге. Такая проверка оценивает реализацию генератора, "
              "а не доказывает, что набор описывает все возможные почерки.")
    ])
    return generator_summary, generator_tv


@app.cell(hide_code=True)
def _(generate_widths, generated_widths, generator_seed, generator_size, inverse_discrete, mo, np, subset):
    _repeated = generate_widths(subset.width.to_numpy(), int(generator_size.value), int(generator_seed.value))[0]
    _edge_draws = np.array([0, np.nextafter(.25, 0), .25, np.nextafter(1.0, 0)])
    _checks = {
        "Выдано ровно заданное число значений": len(generated_widths) == generator_size.value,
        "Все значения принадлежат исходному набору ширин": bool(np.isin(generated_widths, subset.width).all()),
        "Одинаковые данные и seed дают ту же последовательность": bool(np.array_equal(generated_widths, _repeated)),
        "Границы участков и нулевые вероятности обработаны": bool(np.array_equal(
            inverse_discrete([1, 2, 3, 4], [0, .25, 0, .75], _edge_draws), [2, 2, 4, 4])),
        "Постоянная величина генерируется без ошибки": bool(np.array_equal(
            generate_widths([5, 5, 5], 3, 0)[0], [5, 5, 5])),
    }
    if not all(_checks.values()):
        raise AssertionError("Не пройдены проверки: " + ", ".join(k for k, v in _checks.items() if not v))
    mo.accordion({f"6.4. Автоматические проверки · {sum(_checks.values())} из {len(_checks)} пройдены":
        mo.md("\n".join(f"- ✓ {label}" for label in _checks)
              + "\n\nПроверки повторяются при изменении параметров. Они проверяют код; "
              "близость частот отдельно видна на графике и в таблице выше.")})
    return


@app.cell(hide_code=True)
def _(choice, cutoff, generator_summary, mo, selected_test, subset, threshold_comparison, threshold_conclusion):
    if selected_test is None:
        _link_summary = "Один из признаков постоянен: оценить связь выбранным тестом в этой группе нельзя."
    else:
        _stat, _p, _rho = selected_test
        if _p < .05:
            _direction = "положительная" if _rho > 0 else "отрицательная" if _rho < 0 else "нулевая"
            _link_summary = (
                f"Независимость отвергаем при уровне 0,05 (p = {_p:.4f}). "
                f"Ранговая связь {_direction}: Спирмен = {_rho:.2f}. "
                "При этом ширина не даёт точного предсказания заполненности каждого изображения."
            )
        else:
            _link_summary = (
                f"Не нашли достаточных оснований отвергнуть независимость (p = {_p:.4f}; "
                f"Спирмен = {_rho:.2f}). Считать независимость доказанной по этому результату нельзя."
            )
    _a3 = threshold_comparison.iloc[0]["Медиана активных ячеек"]
    _a5 = threshold_comparison.iloc[-1]["Медиана активных ячеек"]
    mo.md(f"""
    <span id="resume"></span>

    ## 7. Что в итоге

    **Текущий выбор: {choice.value.lower()}, порог {cutoff}, изображений {len(subset)}.**
    Итог обновляется вместе с переключателями.

    **Форма и заполненность.** Медианная ширина — **{subset.width.median():g}** ячеек,
    медианная заполненность — **{subset.ink.median():g}** активных ячеек.
    {_link_summary}

    **Проверка правила измерения.** При смене порога с 3 на 5 медиана числа активных
    ячеек меняется с **{_a3:g}** до **{_a5:g}**. {threshold_conclusion}

    **Случайная выборка.** {generator_summary}
    Генератор использует измеренные частоты ширины; он не создаёт новые изображения.

    **Что это значит для дизайна.** Чтобы описать знак, полезно учитывать и его ширину,
    и заполненность. Два начертания одинаковой ширины могут отличаться количеством
    занятых ячеек. При сравнении важно сохранять единое правило выделения штрихов.

    **Границы вывода.** Результаты описывают этот набор рукописных цифр при выбранной
    обработке. Мы не измеряли читаемость, эстетику или количество штрихов рукой и не
    переносим результат автоматически на шрифты. В наборе есть несколько изображений
    от одних и тех же людей; авторские группы отдельно не учитываются. Перестановочный
    тест рассматривает изображения как обменные наблюдения, поэтому его результат
    здесь используем как исследовательскую проверку, а не вывод о почерке всех людей.

    **Быстро перепроверить:** выберите цифру → сравните подписи под примерами и расчёт
    в раскрывающемся блоке → посмотрите распределения и тест → смените порог с 4 на 3
    или 5 → в генераторе измените seed и размер выборки → проверьте обновившийся итог.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    <span id="criteria"></span>

    ## 8. Где смотреть выполненные пункты

    | Пункт | Раздел |
    |---|---|
    | Отдельный датасет и его происхождение | [Данные](#data) |
    | Две величины и обоснование случайности | [1. Измерения](#measure) |
    | EDA, единицы и согласованные масштабы | [2. Графики](#eda) |
    | Проверка зависимости | [3. Тест](#test) и [4. Группы](#groups) |
    | Проверка устойчивости к порогу | [5. Пороги](#thresholds) |
    | Интерактивный генератор, метод и сравнение метрик | [6. Генератор](#generator), пункты 6.1–6.3 |
    | Автоматические проверки генератора | [6. Генератор](#generator), пункт 6.4 |
    | Промежуточные выводы и общий итог | Под графиками и [7. Итог](#resume) |
    | marimo, скрываемый код и навигация | Интерактивная версия работы и оглавление |

    **Материалы к методу.**
    [Обратное преобразование для дискретных распределений — SciPy](https://docs.scipy.org/doc/scipy/tutorial/stats/sampling_dgt.html)
    описывает принцип; здесь реализован поиск по накопленным частотам, без ускоряющей таблицы DGT.
    [NumPy: генератор равномерных чисел](https://numpy.org/doc/stable/reference/random/generator.html),
    [правила поиска границы searchsorted](https://numpy.org/doc/stable/reference/generated/numpy.searchsorted.html).
    Источники данных приведены в [начале работы](#data).
    """)
    return


if __name__ == "__main__":
    app.run()

