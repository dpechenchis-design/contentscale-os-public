---
name: cs-content-strategy
description: >
  ContentSCALE етап 3. Будує Social Media Strategy нового клієнта в Canva: структура строго за
  еталоном reference strategy (≈28 сторінок; сторінки платформ і опційні модулі додаються чи прибираються
  за платформами клієнта), дизайн з майстра ContentSCALE. Кожен факт береться з client context і
  research; cadence і дозволені формати — обов'язкові; AI-slop перевірка; збереження в Canva лише після
  погодження. Використовуй, коли кажуть: стратегія, content strategy, social strategy, стратегія для
  клієнта, зроби стратегію в Canva, cs-content-strategy.
---

# cs-content-strategy: context + research → стратегія в Canva

> **Шляхи.** `$CS` = папка зі скілами плагіна ContentSCALE = батьківська папка для «Base directory for this skill», яку Claude показує під час завантаження скіла (наприклад, `…/contentscale/skills`). У командах підставляй повний шлях замість `$CS`. Python для скриптів, яким потрібні бібліотеки: `~/.contentscale-venv/bin/python` (створює `sh $CS/cs-pipeline/scripts/setup.sh`).

> **Перед початком:** прочитати `$CS/cs-pipeline/brain/team_decisions.md`, розділ цього етапу в `$CS/cs-pipeline/brain/quality_bar.md` і `clients/<slug>/client_rules.md` (правила клієнта перекривають загальні). Після етапу автопілот `cs-pipeline` запускає агента `cs-quality-reviewer`.

Етап 3 пайплайну. Вхід: `clients/<slug>/context/client_context.json`, `clients/<slug>/research/reference_records.json` (+ research xlsx), відповіді CM.
Вихід: дизайн у Canva `<Client>_Social Strategy` (копія майстра) + внутрішній `strategy/strategy_content.json` і `strategy/qa_log.md`.

## Еталони
- **Структура:** reference strategy Social Strategy (`<CANVA_DESIGN_ID>` у Canva; також PDF). Порядок розділів незмінний. Pre-alignment не робимо (рішення команди).
- **Дизайн:** `ContentSCALE — Strategy Master` (Canva `<CANVA_DESIGN_ID>`). Чистий макет із плейсхолдерами `{{KEY}}`. Карта сторінок і плейсхолдерів: `references/master_map.md`.
- **Якість змісту:** затверджена стратегія Example Brand (`<CANVA_DESIGN_ID>`) — рівень конкретики, якого треба досягти. Текст, цифри й структуру pillars з неї **не копіювати** (для the client теж: її будують із свіжих даних).
- Розділи → потрібні факти → джерела: `references/section_fact_map.md`.

## Майстер: де взяти, якщо щось сталося
Працювати завжди з **копією**. Майстер і резерв не редагувати.
1. `<CANVA_DESIGN_ID>` «ContentSCALE — Strategy Master» (`read-design` → якщо доступний і 35 сторінок із `{{…}}` плейсхолдерами — беремо).
2. Немає або змінений (плейсхолдерів немає, сторінок не 35) → резерв `<CANVA_DESIGN_ID>` «ContentSCALE — Strategy Master BACKUP (do not edit)».
3. Немає обох → `search-designs` за запитом «Strategy Master» і перевірити, що знайдене — з плейсхолдерами `{{CLIENT_NAME}}`.
4. Нічого не знайдено → офлайн-резерв `assets/strategy_master_backup.pdf` (той самий майстер, 35 стор.). CM перетягує PDF у Canva (Create → Import), Claude знаходить новий дизайн за назвою, перевіряє плейсхолдери (текст імпортованого PDF може мати артефакти: злиплі слова, намальовані буліти — виправити до першого використання) і робить з нього копію `ContentSCALE — Strategy Master` + новий BACKUP. Оновити ID у цьому файлі й у `references/master_map.md`.
Після відновлення повідомити CM, який крок спрацював.

## Незмінні правила
1. Тільки факти клієнта з контексту, research і відповідей CM. Нічого з reference, the client чи інших стратегій. Відсутній факт → питання, а не вигадка.
2. **Cadence (постів на день/тиждень по платформах) обов'язковий.** Без нього стратегія не фіналізується. Cadence у кожного клієнта свій (the client ≈10/день — це індивідуальне рішення клієнта, а не стандарт).
3. Дозволені Types і 3–4 категорії `Format` мають збігатися з тими, що підуть у Notion-календар.
4. У стратегії (а не в календарі) пояснюється поетапний план: спершу повторюємо те, що вже працює в клієнта (дані з research), далі аналізуємо результати й додаємо формати. Цей план має спиратися на дані, а не на шаблонну фразу.
5. Кожне число має джерело (`sources` у JSON).
6. Не додавати розділів, яких немає в reference, крім затверджених опційних модулів (`section_fact_map.md`), і тільки за наявності даних.
7. Збереження змін у Canva (`edit-design` → `commit`) — **лише після того, як CM побачив прев'ю й погодив.**

## Процес

### Крок 1. Fact map і прогалини
Для кожного розділу з `section_fact_map.md`: потрібні факти → що є (з посиланням на `evidence_map` / записи research) → чого бракує.
Питання до CM ставити тільки щодо критичних прогалин: cadence, платформи, дозволені Types, бізнес-цілі з цифрами. Решта береться з джерел.
Опційні модулі вмикати лише за умов із таблиці модулів.

### Крок 2. Текст стратегії → `strategy/strategy_content.json`
Формат описано в `scripts/check_strategy.py`. Ключі полів = плейсхолдери з `master_map.md`.
- Писати мовою контенту клієнта (зазвичай EN), конкретно, як у затвердженій the client: цифри з research, дослівні заперечення з дзвінка, назви продуктів.
- **Pillars = категорії `Format`** (3–4). % рахувати так: кожен власний пост клієнта з `passes_ratio = true` віднести до однієї категорії за caption + transcript (+ кадри, якщо є). Таблицю класифікації (URL → категорія → чому) покласти у `fact_map.md`. На слайді формат «<категорія> NN% = X з Y топ-постів». Якщо captions/transcripts для платформи немає → % не ставити, лише якісний опис. Розподіл позначити в open_questions як «CM підтверджує».
- Hooks будувати зі структур хуків, що спрацювали в research, і з болів/заперечень клієнта. `core_objection` іде першим в Objection-Breaking Hooks.
- Сторінки платформ: одна пара Pillars & Schedule + Delivery на кожну запитану платформу. Незапитані платформи → `include: false`.

### Крок 3. AI slop + перевірка
1. Пропустити весь текст через `sharrans-ai-slop` (EN) або `humanizer-ru` (RU). Дослівні цитати клієнта не чіпати.
2. `python3 -I $CS/cs-content-strategy/scripts/check_strategy.py clients/<slug>/strategy/strategy_content.json --clients-dir clients --capacity $CS/cs-content-strategy/references/master_capacity.json`
   Exit 0 обов'язковий. Попередження SLOP переглянути вручну.
3. Повторно звірити, що після AI-slop факти, числа й зміст не змінилися.

### Крок 4. Збірка в Canva
1. `copy-design` майстра з `page_numbers` = лише включені сторінки (порядок reference). Назва: `<Client>_Social Strategy`.
2. `read-design` з `open_transaction: true` (порціями по 3–4 сторінки). Для кожного елемента з `{{KEY}}` зробити `replace_text` текстом з JSON. Списки лишаються списками: одна позиція = один рядок.
   - Якщо плейсхолдер стоїть одразу після жирної мітки, `find_and_replace_text` успадкує жирний. Тоді спершу замінити `KEY}}` на текст, а `{{` прибрати **одним** викликом після всіх ключів цього елемента (find_and_replace б'є по всіх збігах в елементі).
   - Глобальні імена: у заголовках капсом — `{{CLIENT_NAME}}` → «Example Brand», у тексті — як пишеться бренд. Присвійна форма: «’s», але якщо назва закінчується на s — лише «’» («Naturals’»).
   - Після видалення сторінок номери зсуваються: шукати елементи за текстом плейсхолдера, а не за номером чи ID.
3. Зображення: блоки `{{IMAGE: …}}` замінити на фото клієнта (сайт клієнта, бренд-асети, Notion Hub) через `upload-asset-from-url` → `insert_fill`/`update_fill` (заповнює з кропом). Дозволені джерела: лише сайт клієнта й надані клієнтом матеріали, без стокових зображень і без чужих брендів.
   Слоти скриншотів (Competitive, профілі, Delivery): скриншот профілю чи референсу, якщо є (браузер → файл → upload). Якщо скриншоту немає, замість блоку ставити **stat card** з реальними цифрами з research (ключі `COMP_CARD_*`, `P*_PROFILE_CARD_*`, `DELIVERY_P*_REF_*` у `master_capacity.json`). Порожніх блоків не лишати.
4. Заголовки: жодних «İ» (тільки звичайне I).
5. `read-design` thumbnails усіх сторінок: перевірити переповнення, обрізаний текст, залишки `{{`. Виправити (скоротити текст, але не міняти факти).
6. **Показати CM прев'ю** (посилання на дизайн + список відкритих питань) → після «так» зробити `edit-design` `finalize: commit`. Без відповіді → `cancel` і нічого не зберігати.

### Крок 5. Вихід
- Canva: `<Client>_Social Strategy` (edit-посилання → CM).
- `strategy/strategy_content.json`: внутрішній, з джерелами.
- `strategy/qa_log.md`: що ввімкнено або вимкнено й чому, відповіді CM, результат check_strategy, AI-slop.
- `cadence`, `format_categories`, дозволені Types → етап календаря.

## Acceptance
- [ ] Порядок розділів = reference; додаткові сторінки лише з дозволеного списку модулів.
- [ ] `check_strategy.py` exit 0; жодних слів з інших стратегій.
- [ ] Cadence і Types явно вказані; 3–4 категорії Format.
- [ ] Поетапний план спирається на реальні хіти клієнта з research.
- [ ] AI slop пройдено, факти після нього перевірено.
- [ ] Прев'ю погоджено CM до commit.
