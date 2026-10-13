# Структура Client Intelligence Dossier (канон = S10, Example Brand)


Оболонка: `../assets/dossier_shell.html`. CSS, навігація й рушій ті самі; змінюються лише константи та масив `S`.
Мова досьє: англійська (як в еталоні), якщо CM не вказав іншу. Цитати **ніколи не перекладаються**.

## Мітки джерел (flag під заголовком секції)

| Константа | Коли ставити |
|---|---|
| без flag | Факти з дзвінка або сайту, без інтерпретації (Overview, Value, Matrix, Content, Evidence) |
| `INTERP` | Синтез і композити (Persona, ICP, Psychology, Transformation) |
| `BRIEF` | Дзвінок + сайт + скан конкурентів (Part II) |
| `DATA` | Агреговані відгуки (Part III). Текст flag: `Data · N public reviews` |

## Хелпери оболонки
- `head(eyebrow, titleHTML, intro, flag)`: заголовок секції. `<span class="hl">…</span>` виділяє ключове слово.
- `entries([{l, q:[...], s}])`: картки з дослівними цитатами (`q`) і джерелом (`s`).
- `litems([{t, q, s}])`: компактні цитати (Triggers, Fears).
- `bars(rows, max, ticks, cls)`: горизонтальні бари (лише для реальних підрахунків).
- Класи: `statgrid/stat`, `pills/pill`, `cards/pcard[data-go]`, `duo/box`, `callout`, `tablewrap/table.matrix`, `prose`, `icp good/bad`, `pillars/pillar`, `ngrid/ncard`, `arch/comp/cc`, `ice-top/ice-bot/chips`, `quad-wrap/quad/q.moat`, `ptable`, `years`, `trans`.

## Секції (порядок і id фіксовані)

| # | id | group | label | Зміст і формат | Джерела |
|---|---|---|---|---|---|
| 00 | overview | null | Overview | Eyebrow «Client Intelligence Dossier», головна теза; 4–5 `stat` (лише підтверджені числа з позначкою джерела); pills «Sources» і «The buyers»; `cards` на 5 частин | call, site, reviews |
| 01 | value | Part I · The Business | Value Proposition | `duo` (2 продуктові лінії або 2 обіцянки) + `callout` core proposition + `note` про поточні SKU і proof points | call, site |
| 02 | matrix | Part I · The Business | Audience Matrix | `table.matrix`: колонки = сегменти покупців, рядки = Finds via / Budget / Primary emotion / Time to result / Where they live + `note` | call |
| 03 | persona | Part I · The Business | The Persona | `INTERP`; `prose` з 2–3 композитами + `callout` «What all of them actually want» | call (+review quote із джерелом) |
| 04 | icp | Part I · The Business | ICP Diagnostics | `INTERP`; `icp good/bad` по 5 рядків + box «Why it's structural» | call |
| 05 | content | Part I · The Business | Content Architecture | 3 `pillar`: назва, етап воронки, опис. Лише з того, що є в дзвінку чи активах | call |
| 06 | questions | Evidence · Verbatim (the call) | Questions | `entries`, count = кількість | **тільки дослівні цитати клієнта** |
| 07 | objections | Evidence · Verbatim (the call) | Objections | `entries` | те саме |
| 08 | beliefs | Evidence · Verbatim (the call) | Limiting Beliefs | `entries` | те саме |
| 09 | desires | Evidence · Verbatim (the call) | Desires | `entries` | те саме |
| 10 | pains | Evidence · Verbatim (the call) | Pain Points | `entries` | те саме |
| 11 | triggers | Evidence · Verbatim (the call) | Buying Triggers | `litems` | те саме |
| 12 | fears | Evidence · Verbatim (the call) | Fears | `litems` | те саме |
| 13 | hero | Part II · The Market | The Shared Hero | `BRIEF`; `ngrid` 4 картки: Demographics / Origin arc / Catalyst / Destination | call |
| 14 | competitors | Part II · The Market | Competitor Topography | `BRIEF`; `arch` з картками `cc` (Positioning, Price point/Target, «Client's read», джерело). Конкурент не досліджений → «Not yet researched» | call + сайти конкурентів |
| 15 | iceberg | Part II · The Market | Objection Iceberg | `chips` (дослівні фрази) + `ice-bot` (переконання) + 2 `olist` Top 5 questions / objections | call, reviews |
| 16 | whitespace | Part II · The Market | White Space | `quad` 2×2 з осями, `q.moat` = позиція клієнта + `callout` strategic imperative | синтез з call/конкурентів |
| 17 | snapshot | Part III · The Reviews | Review Snapshot | `DATA`; stat, розподіл рейтингів, таблиця по продуктах, роки | **тільки реальний pull відгуків** |
| 18 | praise | Part III · The Reviews | What They Praise | `DATA`; bars за темами (keyword match) + `entries` з цитатами відгуків | те саме |
| 19 | wrong | Part III · The Reviews | What Goes Wrong | `DATA`; bars `neg` + `entries` | те саме |
| 20 | switch | Part III · The Reviews | The Switch Story | `DATA`; відгуки, що називають конкурента | те саме |
| 21 | psych | Synthesis | Psychology | `INTERP`; `ngrid` 6 драйверів, кожен спирається на цитату | синтез |
| 22 | transform | Synthesis | Transformation | `INTERP`; `trans` Before → After по 5 пунктів + `callout` «What's actually sold» | синтез |

## Правила, коли даних немає
- Немає публічних відгуків → **Part III не вигадується.** Секції 17–20 лишаються з flag `Not collected` і `note` «No public review feed was available for this client.» Видаляти їх можна лише з дозволу CM. Цифр і цитат немає.
- Немає цитат для Evidence-категорії → секція лишається, у ній `note` «Not discussed on the call.» `count` = 0.
- Число без джерела → не ставити `stat`.
- Конкурент лише згаданий → `cc` зі статусом «Not yet researched».
- Дослівні цитати: дозволено прибрати філери (um, like, you know) і виправити явну помилку транскрибації в `[квадратних дужках]` (Bass → [Competitor A]). Зміст не змінюється.
