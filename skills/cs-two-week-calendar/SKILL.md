---
name: cs-two-week-calendar
description: >
  ContentSCALE етап 4. Будує двотижневий контент-календар у Notion (схема бази «Week 1») за
  затвердженою стратегією: кількість постів за cadence, категорії Format і Types зі стратегії, для
  кожного поста справжній референс із research (Type = Type референсу), feasibility за Client Working
  Model, тексти за format guides (TH-скрипт 1:1 з референсу, BTS без скрипта, Expert video з об'єктом
  реакції, каруселі по слайдах), AI-slop + regression QA, запис у Notion день за днем після погодження.
  Використовуй, коли кажуть: контент-календар, календар на два тижні, заповни Notion, пости на тиждень,
  cs-two-week-calendar.
---

# cs-two-week-calendar: стратегія + research → двотижневий Notion-календар

> **Шляхи.** `$CS` = папка зі скілами плагіна ContentSCALE = батьківська папка для «Base directory for this skill», яку Claude показує під час завантаження скіла (наприклад, `…/contentscale/skills`). У командах підставляй повний шлях замість `$CS`. Python для скриптів, яким потрібні бібліотеки: `~/.contentscale-venv/bin/python` (створює `sh $CS/cs-pipeline/scripts/setup.sh`).

> **Перед початком:** прочитати `$CS/cs-pipeline/brain/team_decisions.md`, розділ цього етапу в `$CS/cs-pipeline/brain/quality_bar.md` і `clients/<slug>/client_rules.md` (правила клієнта перекривають загальні). Після етапу автопілот `cs-pipeline` запускає агента `cs-quality-reviewer`.

Етап 4 пайплайну. Вхід:
- `strategy/strategy_content.json` (cadence, format_categories, Types, pillars і їхні частки, розклад);
- `research/reference_records.json` (референси з Type, транскриптами, кадрами);
- `context/client_context.json` (факти, заперечення, Working Model, асети, хештеги з власних captions клієнта);
- база Notion клієнта.

Вихід:
- сторінки в Notion;
- `calendar/calendar_items.json` (внутрішній);
- `calendar/reskin/<id>.md` (таблиці оригінал | клієнт для TH);
- `calendar/internal_qa_report.md`.

Довідники: `references/notion_mapping.md`, `references/format_guides.md`, `references/regression_tests.md`, правила Head of Content `$CS/cs-two-week-calendar/references/feedback_patterns.md`.

## Незмінні правила
1. Без cadence зі стратегії календар не фіналізується. Кількість постів = cadence × 14 днів (the client ≈ 10/день → ~140; це рішення клієнта, а не стандарт).
2. У календарі тільки контент. Жодних пояснень, стратегії, «AI вирішив», статусів-міток. Внутрішнє йде в `internal_qa_report.md`.
3. `Publishing date` і `Edited video` порожні. `Week day` — день тижня, не дата. `Status` = `Script ready`.
4. Format = категорії стратегії (3–4). Type = Type референсу. Їх не змішувати.
5. Кожен пост має реальний референс із research. Немає придатного референсу → немає поста (а не «напишемо без референсу»).
6. Факти, цитати, коментарі, відгуки — тільки справжні, з джерелом. Вигаданий коментар чи відгук = брак.
7. Тексти клієнта проходять `sharrans-ai-slop` (EN) або `humanizer-ru` (RU); дослівні цитати й транскрипти не переписувати.
8. Запис у Notion: 1 тестова сторінка → «так» від CM → далі **по одному дню**, з переглядом кожного дня.
9. Чужі календарі (база-еталон the client) — лише читати.

## Процес

### Крок 1. План слотів
1. З `strategy_content.json` взяти cadence по платформах, `format_categories`, дозволені Types, частки pillars і акценти розкладу по днях.
2. Розкласти 14 днів × N слотів: категорії за частками, Types за стратегією. Типи чергувати, той самий топік не ставити два дні поспіль.
3. Тиждень 1–2 = «спершу те, що працює» (як у стратегії): більшість слотів — повтори й варіації власних хітів клієнта та перевірених форматів research. Нові формати лише в межах, які дозволяє стратегія.
4. Записати `calendar/plan.md` (внутрішній): день → слот → категорія → Type → тема (з `evidence_map`) → кандидат-референс.

### Крок 2. Референси і feasibility (до написання текстів)
Для кожного слота:
1. Референс з `reference_records.json`: `passes_ratio = true`, `approval_gate = OK`, Type відповідає слоту, тема в ніші клієнта. Ще не класифікований → `fetch_media.py` (скіл `cs-content-research`) → кадри → Type.
2. Feasibility: чи може клієнт це відтворити (Working Model, `new_recordings_allowed`, асети, люди в кадрі, продукт). Ні → інший референс. Не вийшло й так → blocker у `internal_qa_report.md` для CM. У Notion такий пост не йде.
3. Expert video: знайти об'єкт реакції (реальний URL відео, коментаря чи відгуку). Немає → інший референс.
4. Власні хіти клієнта, які варто перезняти (re-record), йдуть за правилом із `format_guides.md`, тільки якщо `new_recordings_allowed = true`.

### Крок 3. Тексти за Type (`format_guides.md`)
Кожен пост пишеться за скілом `cs-post-writer` (ті самі правила для одного поста й для календаря).
- **Talking head:** таблиця reskin 1:1 (оригінал | клієнт) у `calendar/reskin/<id>.md` → SCRIPT = колонка клієнта.
- **BTS:** NOTES (кроки з кадрів референсу) + ON-SCREEN TEXT. Без скрипта.
- **Expert video:** callout з `React to this video` + NOTES з фрагментом і talking points. Без скрипта.
- **Carousel:** усі слайди.
- **NOTES FOR THE CLIENT:** конкретні дії зйомки.
- **CAPTION:** освітній, хештеги клієнта (беруться з його власних captions у research).
- **Name:** коротка тема, різна для кожного поста.
- Кліпи з лайвів (якщо клієнт їх має) записувати як Type, погоджений CM для цього клієнта (the client: Talking head).

### Крок 4. QA
1. AI slop на всі клієнтські тексти, потім перевірити, що факти, хук і структура не змінились.
2. `python3 -I $CS/cs-two-week-calendar/scripts/qa_calendar.py clients/<slug>/calendar/calendar_items.json clients/<slug>/research/reference_records.json [--week 1 --day Monday]` → exit 0.
3. Ручні тести [M] з `regression_tests.md` (структура 1:1, кроки BTS vs кадри, тема з джерелом) → записати в `internal_qa_report.md`.

### Крок 5. Notion
1. `python3 -I $CS/cs-two-week-calendar/scripts/render_notion.py clients/<slug>/calendar/calendar_items.json clients/<slug>/calendar/pages_w<week>_<day>.json --week 1 --day Monday`
2. Перевірити схему бази (`notion-fetch` → `collection://…`) проти `notion_mapping.md`.
3. Створити 1 сторінку (`notion-create-pages`, parent = data source клієнта) → посилання CM → після «так» решту дня → наступний день після перегляду.
4. Перед записом перевірити, чи немає дубля (`Name` + `Week day`). Затверджені сторінки не чіпати.

## Acceptance
- [ ] Кількість постів = cadence × 14; частки категорій ≈ стратегії.
- [ ] Кожен пост: референс із research, Type = Type референсу, тема з джерелом.
- [ ] `qa_calendar.py` exit 0; ручні тести записано.
- [ ] Порожні дати, Status `Script ready`, тільки дозволені properties.
- [ ] Немає слідів AI і внутрішніх приміток у Notion.
- [ ] Записано після погодження тестової сторінки, день за днем.
