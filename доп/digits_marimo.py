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
    [Связь](#test) · [Отдельные цифры](#groups) · [Пороги](#thresholds) · [Итог](#resume)

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
def _(choice, cutoff, mo, selected_test, subset, threshold_comparison, threshold_conclusion):
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

    ## 6. Что в итоге

    **Текущий выбор: {choice.value.lower()}, порог {cutoff}, изображений {len(subset)}.**
    Итог обновляется вместе с переключателями.

    **Форма и заполненность.** Медианная ширина — **{subset.width.median():g}** ячеек,
    медианная заполненность — **{subset.ink.median():g}** активных ячеек.
    {_link_summary}

    **Проверка правила измерения.** При смене порога с 3 на 5 медиана числа активных
    ячеек меняется с **{_a3:g}** до **{_a5:g}**. {threshold_conclusion}

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
    или 5 и проверьте обновившийся итог.
    """)
    return


if __name__ == "__main__":
    app.run()
