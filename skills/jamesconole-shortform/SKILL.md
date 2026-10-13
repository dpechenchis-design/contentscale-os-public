---
name: jamesconole-shortform
description: >
  Фреймворк коротких віральних скриптів James Conole (@jamesconole, retirement/financial planning).
  13 виральних фреймворків з аналізу 999 рілсів: X/10 Scorecard, Uncomfortable Flip, Two-Person Dialogue,
  Geographic Ranking, Dollar Amount Hook, Myth vs Fact, Right vs Wrong Way та ін. Движок для фінансового/
  пенсійного контенту з оцінками, рейтингами та емоційними переворотами. Використовуй коли користувач
  згадує: James Conole, jamesconole, retirement content, financial planning reels, scorecard format,
  X out of 10, retirement expert rates, pension, social security, 401k, withdrawal strategy.
---

# James Conole Viral Short-Form Framework Engine

This skill is a viral framework engine for retirement and financial planning content, reverse-engineered from an analysis of 999 Instagram reels by James Conole (@jamesconole). It provides 13 proven content frameworks ranked by average views, along with visual format specifications and strategic insights for producing high-performing financial planning short-form content.

## ⚠️ ДЖЕРЕЛО ДАНИХ — жорстке правило

Усі рілсів для роботи беруться **ТІЛЬКИ з бази цього скіла**. Інших джерел немає.

- `references/reels-database.md` — 100 рілсів @jamesconole: посилання, дата, перегляди, лайки, коменти, фоловери і **повний дослівний транскрипт**. Відсортовано за переглядами.
- `references/reels-table.xlsx` — оригінальна таблиця (ті самі дані; картинки винесені в `visuals/`, щоб скіл важив мало).
- `references/visuals/<shortcode>.jpg` — скрін формату і хука на екрані (100 з 100). **Перед вибором рілса відкрий його скрін (Read) і подивись**: формат зйомки (talking head / split-screen / вулиця / BTS / текст на екрані), текст хука в кадрі. Формат у примітці ресогу пишеш за скріном, а не вгадуєш з транскрипту.

Правила:
1. Посилання, метрика, транскрипт — **копіюються з бази дослівно**. Не округлювати (4,549,912, не «4.5M»), не переказувати, не скорочувати транскрипт — ліва колонка ресогу = ВЕСЬ транскрипт, біт за бітом.
2. Не скрейпити і не шукати рілси інструментами (vidIQ тощо), не брати приклади «з пам'яті» — поки у базі є потрібне.
3. `BTS` / порожній транскрипт / пісня / не англійською = без мови креатора → для 1:1 ресогу не годиться (хіба скелет повністю в тексті на екрані — тоді дивись скрін).
4. Метрика — на дату вивантаження таблиці; у доці так і підписувати.
5. `references/viral-frameworks.md` / `framework.md` — для назв фреймворків і розуміння скелетів, **не** як джерело оригінального тексту.

## Reference Files

- `references/viral-frameworks.md` — Full 13-framework analysis with performance data, structural breakdowns, visual format specifications, and brand elements.

## Top 5 Frameworks (Quick Selection Guide)

| # | Framework | Avg Views | When to Use |
|---|-----------|-----------|-------------|
| 1 | **Best/Worst State Geographic Ranking** | 330K | When the topic can be tied to specific U.S. states or locations (taxes, cost of living, healthcare access). Massive engagement multiplier from geographic specificity. |
| 2 | **The Uncomfortable Flip** | 152K | When challenging a common belief or "comfortable lie" people tell themselves about retirement ("I'll just work one more year", "I'll travel later"). Best for emotional, regret-driven content. |
| 3 | **Two-Person Dialogue** | 133K | When comparing two legitimate perspectives or life situations where neither is strictly wrong. Generates enormous comment sections (7,251 comments on top performer). |
| 4 | **X out of 10 Scorecard** | 121K | When rating multiple items in a category (withdrawal strategies, retirement accounts, income sources). Controversial low scores drive engagement. 12x the average views of the most-produced format. |
| 5 | **Dollar Amount Hook** | 99K | When a specific dollar figure can anchor the hook ("$10,000/month in retirement", "What does $1 million actually get you?"). Challenges conventional wisdom like the 4% rule. |

## KEY INSIGHTS

### 1. The "Judgment" Principle
His top performers share one trait: he JUDGES things. Scoring, rating, labeling myth vs fact, ranking states, grading strategies. Content where James passes explicit judgment consistently outperforms content where he simply explains or advises. The audience craves verdicts, not just information.

### 2. The "Regret > Fear" Principle
The best emotional content focuses on REGRET (wasted years, unlived life, "you don't have 30 years of retirement") rather than FEAR (running out of money, market crashes). Fear is the default emotion in financial content. Regret is the differentiator that makes his content stand out and hit harder.

### 3. The "Geographic" Multiplier
Naming specific states or locations produces a massive engagement boost. His #1 reel ever (1.57M views) is a state ranking. People tag friends, argue about their state, and share to local groups. Any retirement topic that can be framed geographically should be.

### 4. The "Format Novelty" Effect
Dialogue, Personification, and Bracket formats outperform expectations relative to their production effort. The Two-Person Dialogue format generated 7,251 comments on a single reel. Novel visual formats (clone comparisons, triple-split debates) signal effort and stop the scroll.

### 5. The "Repost" Strategy
Near-identical content reposted weeks or months later achieves comparable performance. This is a volume strategy — the algorithm serves content to new audiences each time, so high performers can be recycled with minimal modification.

### 6. Volume vs Virality Paradox
"Should You Yes/No Gateway" is the most-produced format (16 reels) but the lowest-performing (avg 13K views). Meanwhile, "X/10 Scorecard" averages 121K — roughly 12x the views. Producing more of a format does not make it perform better; the framework structure itself determines the ceiling.

## Usage Instructions

When generating scripts for James Conole style content:

1. Identify the core topic (retirement timing, Social Security, withdrawal strategy, etc.)
2. Select the highest-performing framework that fits the topic naturally
3. Reference `references/viral-frameworks.md` for the full structural breakdown and visual format
4. Apply the Judgment Principle — ensure James is rating, scoring, or labeling something
5. Apply the Regret > Fear Principle for emotional hooks
6. Check if the topic can use the Geographic Multiplier
7. Match the script to one of the 7 visual formats documented in the reference file

## Режим: 1:1 Viral Reskin (два стовпці)

Коли команда дає конкретне віральне відео як референс, Claude виконує повний 1:1 реског замість генерації з 13 фреймворків.

### Процес
1. Взяти рілс з `references/reels-database.md` (або той, що назвала команда, — теж шукати в базі): посилання, метрика і ДОСЛІВНИЙ повний транскрипт звідти. Подивитись його скрін у `references/visuals/`.
2. Розібрати скелет построково: кожен рядок = окремий біт (хук, приклад, число, CTA).
3. Переписати рядок-в-рядок, підставляючи змінні під клієнта: нішу, приклади, числа, CTA.
4. НЕ додавати / НЕ прибирати / НЕ міняти порядок бітів.

### Головне правило
**Віральний хук залишається 1:1.** Хук не змінюється — змінюється ТІЛЬКИ контекст під клієнта. Структура вже доведена переглядами; міняємо лише змінні (ніша, приклади, числа, CTA keyword).

### Формат виводу: шапка + таблиця з двох колонок

**Шапка (завжди перед таблицею):**
> **Референс:** [назва/опис відео](посилання на оригінал) | **Views:** X | **Likes:** X | **Creator:** @handle

| Original | Версія під клієнта |
|---|---|
| [біт 1 оригіналу дослівно] | [біт 1 під клієнта] |
| [біт 2 оригіналу дослівно] | [біт 2 під клієнта] |
| ... | ... |

Ліва колонка = дослівний транскрипт оригінального відео.
Права колонка = версія під клієнта, вирівняна біт-в-біт.
Посилання + метрика оригіналу завжди у шапці над таблицею.

### Гейти
- **Чесність:** кожна підставлена заявка = правда для клієнта зараз. Не присвоювати чужий результат.
- **On-topic ICP:** змінні з НІШІ клієнта, не тягти чужу тему.
- **ToV:** лексика клієнта, структура/ритм оригіналу не чіпаються.

### Контекст клієнта
Контекст (DNA, voice notes, ніша, ToV) надає ОКРЕМО людина з команди, яка працює зі своїм клієнтом. Цей скіл пояснює лише ПРОЦЕС адаптації.
