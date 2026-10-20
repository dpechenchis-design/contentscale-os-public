---
name: cs-content-research
description: >
  ContentSCALE етап 2. Сирі експорти SortFeed (акаунт клієнта + конкуренти) перетворює на канонічну
  research-таблицю команди (ті самі вкладки й колонки) і внутрішній список референсів: правило
  «перегляди ≥ 2× підписники», approval-gate для конкурентів, знайдених AI, Type за візуальною механікою
  (Talking head / BTS / Expert video / Carousel), транскрипти (SortFeed → локальний Whisper).
  Нічого не вигадує: немає даних = null. Використовуй, коли кажуть: content research, ресерч клієнта,
  research таблиця, конкуренти, best performing, SortFeed експорт, що залетіло у клієнта, референси
  для календаря, cs-content-research.
---

# cs-content-research: SortFeed → канонічна research-таблиця + референси

> **Шляхи.** `$CS` = папка зі скілами плагіна ContentSCALE = батьківська папка для «Base directory for this skill», яку Claude показує під час завантаження скіла (наприклад, `…/contentscale/skills`). У командах підставляй повний шлях замість `$CS`. Python для скриптів, яким потрібні бібліотеки: `~/.contentscale-venv/bin/python` (створює `sh $CS/cs-pipeline/scripts/setup.sh`).

> **Перед початком:** прочитати `$CS/cs-pipeline/brain/team_decisions.md`, розділ цього етапу в `$CS/cs-pipeline/brain/quality_bar.md` і `clients/<slug>/client_rules.md` (правила клієнта перекривають загальні). Після етапу автопілот `cs-pipeline` запускає агента `cs-quality-reviewer`.

Етап 2 пайплайну. Вхід: `clients/<slug>/context/client_context.json` (від `cs-client-context`) + сирі експорти SortFeed.
Вихід читає `cs-two-week-calendar`. Наявний `content-research-analyzer` не змінюється. Його можна окремо запустити на тих самих експортах для аналізу хуків і тем.

## Одноразове налаштування (кожен CM)
`sh $CS/cs-pipeline/scripts/setup.sh`. Створює `~/.contentscale-venv` (openpyxl, faster-whisper) і перевіряє `yt-dlp` та `ffmpeg`.
Далі всі скрипти запускаються так: `~/.contentscale-venv/bin/python -I $CS/cs-content-research/scripts/<script>.py …`

## Незмінні правила
1. Метрики беруться тільки з експорту SortFeed. Підписники — з профілю акаунта з датою. Немає числа → `null`, «віральним» не називати.
2. Конкуренти з `competitors_named_by_client` не потребують погодження (якщо акаунт ідентифіковано однозначно). Конкурентів, знайдених AI, показати CM на approve/reject **до** роботи з їхнім контентом.
3. `Approved?` у таблиці ставить лише людина. Скрипт його не заповнює й не перезаписує.
4. Вкладки таблиці (рішення 2026-10-20): `Best performing content IG / Tik Tok`, `Competitors (IG) / (Tik Tok)`, `Carousels`, плюс довідкова `Why selected`. Окремих вкладок BTS, Expert videos, IG Competitors, Competitive analysis, Accounts немає: у кожній вкладці з відео є колонки `Transcript` (біля кожного посилання, якщо транскрипт є) і `Type`.
5. Type визначається за кадрами (`references/type_rules.md`), а не за транскриптом і не «на око» за назвою.
6. Транскрипт: спочатку SortFeed (Transcribe), потім локальний Whisper. Якщо немає жодного → `TRANSCRIPT_MISSING`. Ніколи не писати «проаналізовано транскрипт», якщо його немає.

## Процес

### Крок 1. Research-бриф (заповнює команда)
Research іде за заповненим брифом `references/research_brief_template.md` (платформи, ніша, акаунт клієнта, конкуренти, формати). Скіл не визначає нішу чи платформу сам, а фільтрує за критеріями брифу. Поле порожнє → питання CM, не здогадка. Брифу немає → взяти ці поля з `client_context.json` (`accounts`, `platforms_requested` / `primary_platform`, `competitors_named_by_client`, `content_types_allowed`, `client_working_model`) і показати CM як чернетку брифу на підтвердження.
- Платформа не вказана → Instagram за замовчуванням. Але якщо клієнт явно TikTok-first (як the client), research іде по TikTok. Питати лише за справжньої невизначеності.
- Формати не вказані → research охоплює всі 4 Types. Пули для недозволених Types не заповнювати.

### Крок 2. Акаунти і gate для конкурентів
1. Знайти handle кожного названого конкурента на потрібних платформах (сайт бренду, посилання в профілі). Сумнів в ідентифікації (кілька схожих акаунтів) → показати CM.
2. Конкуренти беруться з **брифу конкурентів** (секція в `research_brief_template.md`): спершу ті, кого назвав клієнт, потім додаткові від AI за нішею й аудиторією (`competitor_source = ai_found`, `approved = pending`), навіть якщо клієнт когось назвав. Research лише силами AI дає слабку якість, тому **СТОП: показати CM список від AI (handle, підписники, чому релевантний) і чекати approve/reject.**
3. Заповнити `clients/<slug>/sources/accounts.csv` за шаблоном `$CS/cs-content-research/references/accounts_template.csv`. `followers` береться з профілю (можна через браузер), `followers_source` = звідки й коли.

### Крок 3. Збір постів
**TikTok: автоматично, 0 кредитів (рішення 2026-10-13).**
`python3 -I $CS/cs-content-research/scripts/fetch_tiktok.py clients/<slug>/sources/accounts.csv clients/<slug>/sources/auto --months 12 --max 400`
- Підписники з публічної сторінки профілю записуються в `accounts.csv` автоматично.
- Список відео з метриками береться через `yt-dlp` (без завантаження відео); Outlier Score = перегляди / медіана акаунта.
- Акаунт `FAILED` (TikTok щось змінив чи заблокував) → для нього SortFeed-експорт вручну (нижче).

**Instagram: спершу SortFeed (конектор Claude), рішення 2026-10-20.** Перед збором перевірити SortFeed за `references/sortfeed_setup.md`: немає інструментів SortFeed у сесії або розширення не відповідає → показати CM кроки налаштування; CM не налаштовує зараз → запасний спосіб нижче. Встановити розширення за CM не можна, лише підказати.
Як збирати через SortFeed (тест 2026-10-20: Competitor D, 500 рілсів за ~6 хв, 100 за 21 с; вручну було ~15 хв):
1. `bridge_status` → Connected? Ні → кроки з `sortfeed_setup.md`.
2. Для кожного IG-акаунта по черзі (не паралельно): `sort_profile(username, depth=500, sort_by=views, next_profile=<наступний>)`; якщо RUNNING → `sort_status(job_id)` до результату. Ліміт: 500 рілсів на профіль; бюджет Instagram 200 запитів/год (≈ 4 акаунти по 500).
3. Повний CSV: з відповіді взяти посилання `https://mcp.sortfeed.com/csv/...` (діє 24 год) і зберегти `curl -s -o clients/<slug>/sources/auto/<handle>_ig_reels_sortfeed.csv <посилання>` (або `export_csv`). Формат = експорт SortFeed (Profile, Reel, Create Date, Views, Outlier Score, Likes, Comments), `ingest_sortfeed.py` читає без змін.
4. SortFeed **не дає підписників** і транскриптів (масові транскрипти в конекторі «Soon»): підписники беруться з профілю (Claude у Chrome або CM) в `accounts.csv`; транскрипти й кадри — `fetch_media.py` для шортлиста.
5. Помилка `No current window` = Chrome запущений без відкритого вікна → попросити CM відкрити звичайне вікно Chrome **з кількома вкладками** і повторити. У тесті 2026-10-20 після сортування вікно інколи зникало: тримати в ньому ще одну звичайну вкладку.
6. Не покладатися на прокрутку сітки як на повний список: на examplebrand прокрутка бачила 32 рілси, SortFeed — 96 (11 віральних замість 7).

**Instagram, запасний спосіб: через браузер, безкоштовно (рішення 2026-10-13).** Відео й транскрипти відібраних рілсів: `fetch_media.py` з сесією Chrome CM (`--ig-cookies chrome`, за замовчуванням). Не вийшло → SortFeed Transcribe + «Download .txt» (кожне завантаження файлу CM підтверджує). Claude у Chrome CM читає сітку Reels (перегляди + підписники), відбирає віральні й відкриває лише їх, щоб узяти посилання. Інструкція: `references/instagram_browser_capture.md` → `ig_capture_to_csv.py` → `sources/auto/`.
Запасний варіант (браузер недоступний, Instagram просить вхід, акаунтів багато): SortFeed вручну:
```
Для кожного IG-акаунта з accounts.csv:
1. Відкрий профіль → вкладка Reels (для каруселей ще й Posts).
2. SortFeed → Sort by Views → дочекайся, поки завантажаться всі пости.
3. (Pro) Transcribe для топ-постів, якщо доступно.
4. Export → Excel. Файл без змін поклади в clients/<slug>/sources/sortfeed/.
```

### Крок 4. Розбір експортів
`~/.contentscale-venv/bin/python -I $CS/cs-content-research/scripts/ingest_sortfeed.py clients/<slug>/sources/<auto|sortfeed> clients/<slug>/sources/accounts.csv clients/<slug>/research/reference_records.json`
- Exit 2 = є непогоджені AI-конкуренти. Їхні рядки помічені `BLOCKED_PENDING_APPROVAL` і в таблицю не підуть.
- `WARN … not in accounts.csv` → додати акаунт із підписниками й перезапустити.
- Звіт показує по кожному акаунту: скільки постів, скільки проходить правило, скільки без даних, скільки з транскриптом. Записати це в `research/research_log.md`.
- **Віральність:** правило `views ≥ 2× followers` (`viral_signal = RATIO`). Поріг не знижується.
- **Виняток, а не правило:** тільки якщо в акаунта < 5 постів проходять 2×, скрипт позначає кандидатів: `EXCEPTION_1X` (перегляди ≥ 1× підписників) або `OUTLIER` (≥ 3× медіани акаунта) і друкує `EXCEPTION`. Тоді спитати CM; лише за згоди додати їх (`write_workbook.py … --include-exceptions`) з позначкою «виняток». Якщо умова не виконується, кандидатів немає.
- ⚠️ Якщо у великого акаунта (мільйони підписників) правило проходить 0–2 пости, це не помилка. Зафіксувати в лозі. Брати такі пости вручну «бо багато переглядів» не можна; рішення про виняток ухвалює CM.

### Крок 5. Shortlist і Type
1. Для кожного дозволеного Type відібрати кандидатів серед `passes_ratio = true`: релевантність ніші й аудиторії клієнта, тема збігається з болями/запереченнями з контексту. Пріоритет — власні хіти клієнта.
2. Для shortlist (не для всієї таблиці!) отримати кадри й транскрипт:
   `~/.contentscale-venv/bin/python -I $CS/cs-content-research/scripts/fetch_media.py clients/<slug>/research/reference_records.json clients/<slug>/work --workers 6 --mosaic --urls <url1> <url2> …`
   Шортлист за замовчуванням: топ-10 віральних з кожного акаунта. Прискорення (2026-10-20): TikTok-транскрипт береться з власних субтитрів відео (~3 с, `TIKTOK_CAPTIONS`), Whisper лише для Instagram або відео без субтитрів; завантаження паралельні (`--workers`); `--mosaic` складає кадри 4 відео в одну картинку (`media/mosaics/`, порядок зверху вниз = `index.json`), тож Type визначається вчетверо швидше. 47 відео ≈ 6 хв.
3. Каруселі: слайди за `references/carousel_capture.md`.
4. Переглянути кадри (Read jpg) і заповнити за `references/type_rules.md`: `type`, `type_evidence`, `hook`, `asset_requirements`, для Expert video `reaction_target_url`, для Carousel `carousel_slides` (текст кожного слайду; кадри або скриншоти з браузера).
4. **Existing Content Only** (`client_working_model = EXISTING_ONLY`): глибше пройти архів клієнта (довгі відео, подкасти, лайви). Референс брати лише тоді, коли його можна реалізувати без нових зйомок.
5. Пост `/p/` без візуальної перевірки в таблицю не йде (це може бути одиночне фото).

### Крок 6. Канонічна таблиця
`~/.contentscale-venv/bin/python -I $CS/cs-content-research/scripts/write_workbook.py clients/<slug>/research/reference_records.json "clients/<slug>/research/<Client> research (IG+Tik Tok).xlsx"`
- Власні пости → `Best performing content IG / Tik Tok`. Конкуренти → `Competitors (IG) / (Tik Tok)` блоками по акаунтах. Type кожного поста — у колонці `Type` (за кадрами; `not classified`, поки кадри не перевірені). Каруселі → `Carousels`.
- Повторний запуск зберігає ручні `Approved?` / `Used?`.
- Таблицю можна завантажити в Google Drive команди, якщо CM попросить (через Google Drive connector).

### Крок 7. QA (перед передачею далі)
- [ ] Кожен URL у таблиці є в експорті SortFeed (provenance) і відкривається.
- [ ] Жодного вигаданого числа; підписники з джерелом і датою.
- [ ] Непогоджені AI-конкуренти не потрапили в таблицю.
- [ ] У shortlist кожен референс має `type` з `type_evidence` за кадрами або `NEEDS_REVIEW`.
- [ ] Expert video має об'єкт реакції; Carousel — усі слайди; BTS — on-screen hook.
- [ ] `transcript_status` чесний (SORTFEED / WHISPER_LOCAL / NO_SPEECH / TRANSCRIPT_MISSING).
- [ ] `Approved?` порожній, доки CM не погодив.

## Вихід
- `research/<Client> research (IG+Tik Tok).xlsx`: клієнтська або командна таблиця в канонічному форматі.
- `research/reference_records.json`: внутрішній; повні записи з Type, транскриптами, provenance.
- `research/research_log.md`: внутрішній; акаунти, підписники з джерелами, gate, статистика правила, винятки.
- `work/media/`: кадри shortlist (відео видаляються автоматично; у git не потрапляє).
