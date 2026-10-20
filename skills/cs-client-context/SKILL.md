---
name: cs-client-context
description: >
  ContentSCALE етап 1. З транскрипту Unpacking-дзвінка (і доступних матеріалів клієнта) будує
  внутрішній client_context.json з evidence map і Client Working Model, а також клієнтське
  Client Intelligence Dossier у точній структурі зразка Example Brand (23 розділи). Нічого не вигадує:
  відсутній факт = UNKNOWN. Використовуй, коли користувач каже: client context, context document,
  досьє клієнта, client intelligence, розбери unpacking, unpacking клієнта, контекст клієнта,
  новий клієнт після дзвінка, cs-client-context.
---

# cs-client-context: Unpacking → Client Context

> **Шляхи.** `$CS` = папка зі скілами плагіна ContentSCALE = батьківська папка для «Base directory for this skill», яку Claude показує під час завантаження скіла (наприклад, `…/contentscale/skills`). У командах підставляй повний шлях замість `$CS`. Python для скриптів, яким потрібні бібліотеки: `~/.contentscale-venv/bin/python` (створює `sh $CS/cs-pipeline/scripts/setup.sh`).

> **Перед початком:** прочитати `$CS/cs-pipeline/brain/team_decisions.md`, розділ цього етапу в `$CS/cs-pipeline/brain/quality_bar.md` і `clients/<slug>/client_rules.md` (правила клієнта перекривають загальні). Після етапу автопілот `cs-pipeline` запускає агента `cs-quality-reviewer`.

Перший етап пайплайну ContentSCALE (`process_map.md`). Вихід цього етапу читають усі наступні: research, strategy, calendar.
Цей скіл **не змінює** наявні скіли. Він перевикористовує принципи `client-intelligence-dossier` (дослівні цитати, синтез позначено окремо) і `dna-verify` (перевірка цитат).

## Незмінні правила
1. Факти про клієнта беремо тільки з транскрипту, сайту клієнта чи наданих матеріалів. Факту немає → `UNKNOWN`/`null`. Якщо факти суперечать один одному → `CONFLICT` і питання.
2. Unpacking = транскрипт дзвінка: команда проходить питання Unpacking усно. Окрему форму не вимагати.
3. Дослівні цитати не перекладаються і не переписуються. Можна лише прибрати філери й виправити явну помилку транскрибації в `[дужках]`.
4. Цитату атрибутуємо **тому, хто її сказав**. Слова агенції (Head of Content та ін.) — не голос клієнта.
5. Синтез (persona, ICP, psychology, transformation) позначається `INTERP` і не подається як факт.
6. Не питати те, що вже є в джерелах. Питання до CM — лише критичні (вони блокують наступний етап).
7. У досьє немає технічних приміток, згадок про Claude/AI чи внутрішніх QA-слідів.

## Вхід
- **Обов'язково:** транскрипт(и) Unpacking. Із Fathom їх можна взяти через MCP (`get_recording_by_call_id` → `get_meeting_transcript`) і зберегти дослівно у `clients/<slug>/sources/*.txt` у форматі `MM:SS - Speaker: text`.
- **Онбординг-бриф** (`$CS/cs-pipeline/brain/onboarding_brief_template.md`), заповнений командою: платформи, формати, частота, Client Working Model, конкуренти.
- **Решта матеріалів з онбордингу** (повний список у шаблоні): Notion Hub, стратегічні документи (ICP doc, Brand voice guide, стратегія), брендові матеріали, референси, що подобаються клієнту, дані про перформанс і кращі пости.
- **AI збирає сам:** сайт клієнта, соцмережі, публічні відгуки.
- **Правило 5 джерел (Head of Content, 2026-10-20):** тільки Unpacking недостатньо. Якщо джерел менше 5, AI **спершу** показує CM інвентар (що є, чого бракує, що AI збере сам) і просить надати більше. Працювати лише з тим, що є, можна тільки після того, як CM підтвердив, що інших матеріалів немає; тоді в досьє позначити розділи, які спираються лише на Unpacking.

## Процес

### Крок 1. Інвентаризація джерел
Створити `clients/<slug>/` з підпапками `sources/` і `context/`. Кожному джерелу дати `source_id` (U1 — дзвінок, W1 — сайт, R1 — відгуки, A1… — асети). Записати їх у `sources[]` разом зі спікерами (хто з боку клієнта, хто з боку агенції).
Перевірити, що файли відкриваються. Недоступне джерело позначити як `BLOCKED_SOURCE: <що саме потрібно>`.
Звірити отримане з переліком матеріалів онбордингу й записати `source_inventory`: `have` / `missing` / `ai_can_collect`. Джерел < 5 → **СТОП:** показати інвентар CM і попросити бракуюче (правило 5 джерел вище). Поля онбординг-брифу (платформи, формати, частота, Working Model) AI не визначає сам: перевіряє, чи вони заповнені, а порожні виносить у питання до CM. Формати й частоту остаточно затверджуємо на етапі стратегії.

### Крок 2. Прочитати транскрипт ПОВНІСТЮ
Прочитати весь файл, не лише початок: найкращі цитати зазвичай у середині. Під час читання виписувати кандидатів у категорії: offer/products, audience segments, pains, objections, limiting beliefs, desires, fears, buying triggers, questions, proof, differentiation, competitors, platforms, content constraints, frequency, formats, recordings/assets, brand voice, заборонені claims.

### Крок 3. Заповнити `client_context.json`
Схема: `references/client_context_schema.json`. Правила:
- Кожен важливий claim, objection чи позиція має запис у `evidence_map`: `field`, `source_id`, `speaker`, `timestamp`, `quote` (дослівно), `kind` (`QUOTE`, `FACT` або `SYNTHESIS`).
- `core_objection`: головне заперечення продукту так, як його формулює клієнт. Для the client це «natural shampoo doesn't foam». Його не можна підмінювати іншою проблемою.
- `competitors_named_by_client`: лише ті, кого назвав клієнт. Найдених AI сюди не вписувати (вони підуть через approval-gate на етапі research).
- `posts_per_week`, `platforms_requested`, `content_types_allowed`: лише якщо явно сказано. Інакше `null` (не `[]`) і питання в `missing_critical_questions` з `blocks_stage`. Частота по платформах іде в `cadence_by_platform` (наприклад, TikTok = 70/тиждень з C1, Instagram = null).
- Формати, які клієнт лише згадав або пропонував (подкаст, лайви, UGC), записувати в `content_types_mentioned`, а не в `allowed`.
- Бренди, з якими клієнт порівнює себе на сайті, записувати в `competitors_referenced_on_client_site` (джерело W1), а не в `competitors_named_by_client`.
- `CONFLICT` між джерелами записувати завжди. Питання до CM ставити, лише якщо конфлікт блокує наступний етап.
- Додаткові поля поза схемою дозволені (`sources[].coverage`, `sources[].diarization_notes` тощо), якщо вони внутрішні й описані в `qa_log.md`.
- Скрипти, якими будувався контекст чи аналізувались відгуки, зберігати в `clients/<slug>/work/`, щоб результат можна було відтворити.

### Крок 4. Client Working Model
Модель заповнює команда в онбордингу (`onboarding_brief_template.md`, там же таблиця, як модель впливає на Research, Strategy і Calendar). Якщо поле заповнене, взяти його. Якщо порожнє, перевірити ознаки нижче й поставити CM 1 питання; модель не вгадувати.
| Модель | Ознаки в джерелах |
|---|---|
| `ACTIVE` | Клієнт регулярно знімає чи пише, обіцяє нові матеріали, має процес (наприклад, «we record every live») |
| `LIMITED` | Зйомки можливі, але нерегулярні («maybe this weekend») |
| `EXISTING_ONLY` | Прямо сказано, що нового не буде; робота лише з архівом |
| `UNKNOWN` | Немає ні ознак, ні заперечень. **Ставити 1 питання до CM про модель.** Окреме питання про наявні асети допустиме, якщо вони теж невідомі |

У `working_model_evidence` записати цитати з таймкодами. `new_recordings_allowed` = `true` лише при явних ознаках. Не робити висновок «зніматиме» за замовчуванням.
Окремо зафіксувати `available_assets`: що вже є (архів, лайви, B-roll, UGC) і що лише обіцяно.

### Крок 5. Додаткові джерела (за наявності)
- **Сайт:** продукти, ціни, proof points, склад. Кожен факт з URL.
- **Відгуки:** якщо є публічний фід (наприклад, публічний API віджета відгуків на сайті клієнта, тільки читання), витягнути весь (дедуп за ID) і зберегти сирим у `sources/reviews_<provider>_<date>.json` у форматі `{"source","pulled","reviews":[{"id","title","body","rating","created_at",...}]}`. Далі порахувати рейтинги й теми (keyword match) і відібрати дослівні цитати. В `evidence_map` кожна цитата з відгуку має `review_id`, `rating`, `product`, дату. Без фіду Part III лишається з позначкою `Not collected`.
- **Конкуренти, яких назвав клієнт:** позиціонування й ціни з їхніх сайтів, з URL. Що не перевірено, позначити «Not yet researched».

### Крок 6. Досьє в структурі S10
Структура, формат кожної секції й правила для відсутніх даних: `references/dossier_structure.md`.
⚠️ Еталон — це **формат**, а не джерело. Цифри, цитати й тексти з нього не копіювати, навіть для того самого клієнта: дані застарівають, а частина фраз у ньому не дослівна.
1. Написати `context/dossier_meta.json`: TITLE, MARK, CLIENT_NAME, BIZ_LINE, SIDE_FOOT, FOOT_SOURCES, DATA_FLAG, SLUG, CONSTANTS_JS (посилання на продукти, `CALL`, хелпер для відгуків, якщо вони є).
2. Написати `context/dossier_sections.js`: 23 секції, ті самі `id` і в тому самому порядку.
3. Усі цитати в Evidence і Part III беруться **з `evidence_map`**, не пишуться заново.
4. Зібрати HTML:
   `python3 -I $CS/cs-client-context/scripts/build_dossier.py clients/<slug>/context/dossier_meta.json clients/<slug>/context/dossier_sections.js clients/<slug>/context/dossier.html`
   Скрипт має завершитися без WARN.

### Крок 7. Верифікація (обов'язковий gate)
`python3 -I $CS/cs-client-context/scripts/verify_context.py clients/<slug>/context/client_context.json clients/<slug>/sources/<transcript>.txt --dossier clients/<slug>/context/dossier_sections.js [--reviews clients/<slug>/sources/reviews_<provider>_<date>.json]`
Скрипт перевіряє цитати з `evidence_map` і `working_model_evidence`, а з `--reviews` ще й цитати з відгуків (за `review_id`, дослівно).
- `NOT_FOUND` → цитату виправити або прибрати.
- `MISMATCH` → відкрити запис у Fathom на таймкоді. Fathom часто зсуває межі реплік: слова клієнта опиняються в рядку агенції. Якщо транскрипт помиляється, а ми ні, додати до запису `attribution_note` з чесною підставою: «audio checked @21:18», якщо перевірено на слух, або «judged from content, audio not checked», якщо ні. Якщо помиляємось ми, виправити `speaker`. Скрипт виводить список таких перевизначень. Ті, що не перевірені на слух, іти в `critical_questions.md` як пункт «CM: spot-check у Fathom» (некритичний).
- `ORPHAN` (цитата є в досьє, але не в evidence_map) → додати її в evidence_map з джерелом або прибрати з досьє.
- `PARAPHRASE` → переглянути вручну. Допустимо лише тоді, коли прибрано філери або склеєно кілька реплік через «…».
Досьє не віддається, доки скрипт не завершиться з кодом 0.

### Крок 8. AI Slop
Пропустити через `sharrans-ai-slop` (EN) або `humanizer-ru` (RU) **лише згенерований текст**: заголовки, intro, синтез, callouts, описи. Цитати й факти не чіпати. Після цього заново запустити крок 7 і перевірити, що зміст і числа не змінились.

### Крок 9. Вихід
- `context/client_context.json`: внутрішній, для наступних етапів.
- `context/dossier.html`: опублікувати як Artifact (приватний), посилання передати CM.
- `context/critical_questions.md`: внутрішній. Лише питання, без яких не почати наступний етап, з позначкою, який етап вони блокують.
- `context/qa_log.md`: внутрішній. Результати верифікації, що отримало `UNKNOWN`, які рішення ухвалено.

## Acceptance
- [ ] 0 `NOT_FOUND`, 0 `MISMATCH`, 0 `ORPHAN` у verify.
- [ ] Немає вигаданих продуктів, кейсів, цифр, цитат. Кожен `stat` має джерело.
- [ ] Working Model визначено з цитатою або стоїть `UNKNOWN` + 1 питання.
- [ ] 23 секції в порядку S10 (`build_dossier.py` без WARN).
- [ ] Синтез позначено `INTERP`, Part II — `BRIEF`, Part III — `DATA` або `Not collected`.
- [ ] AI slop пройдено, факти після нього перевірено повторно.
- [ ] У досьє немає згадок про AI, Claude чи внутрішні примітки.
