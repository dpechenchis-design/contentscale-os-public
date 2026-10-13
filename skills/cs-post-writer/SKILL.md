---
name: cs-post-writer
description: >
  ContentSCALE: пише ОДИН пост для клієнта на запит, у будь-якому форматі — Talking head (скрипт 1:1 за
  референсом), перезйомка власного хіта, Expert video (реакція на реальне відео/відгук), BTS (кроки +
  текст на екрані), Carousel (кожен слайд), caption, або скрипт за фреймворком creator skill, коли
  референсу немає. Ті самі правила, «мозок» і агент якості, що й календар; може записати картку в Notion
  після погодження. Використовуй, коли кажуть: напиши скрипт, talking head для, BTS для, карусель для,
  expert video, реакція на відео, напиши caption, капшин, один пост, ще один пост, перепиши пост,
  скрипт за Dan Martell / Joao / Jun Yuh, cs-post-writer.
---

# cs-post-writer: один пост будь-якого формату

> **Шляхи.** `$CS` = папка зі скілами плагіна ContentSCALE = батьківська папка для «Base directory for this skill». Python з бібліотеками: `~/.contentscale-venv/bin/python`.

> **Перед початком:** `$CS/cs-pipeline/brain/team_decisions.md`, `$CS/cs-pipeline/brain/quality_bar.md` (розділ «Етап 4»), `$CS/cs-pipeline/brain/banned_phrases.md`, `clients/<slug>/client_rules.md`. Гайди за форматами: `$CS/cs-two-week-calendar/references/format_guides.md`.

Календар (`cs-two-week-calendar`) пише свої пости за цим самим скілом. Тут описано, як зробити **один** пост на запит CM.

## 1. Що потрібно (питати лише те, чого немає)
| Поле | Звідки |
|---|---|
| Клієнт | `clients/<slug>/`: потрібен `context/client_context.json`. Немає → спершу `cs-client-context` |
| Формат | з запиту (Talking head / Expert video / BTS / Carousel / Caption / Framework) |
| Тема або референс | з запиту. Якщо є лише тема → підібрати референс із `research/reference_records.json` (Type = формат, `passes_ratio = true`) |
| Категорія (Format) | зі стратегії клієнта, якщо вона є; інакше з запиту |

## 2. Референс → матеріал
- **Відео-референс:** якщо немає кадрів чи транскрипту → `~/.contentscale-venv/bin/python -I $CS/cs-content-research/scripts/fetch_media.py clients/<slug>/research/reference_records.json clients/<slug>/work --urls <url>`. Переглянути контакт-лист, Type за `$CS/cs-content-research/references/type_rules.md`. **Type поста = Type референсу.**
- **Референс не з research** (CM дав посилання) → додати запис у `reference_records.json` (джерело: CM) і пройти той самий шлях. Метрики лише реальні (зі сторінки чи експорту), інакше `null`.
- **Carousel-референс** → `$CS/cs-content-research/references/carousel_capture.md` (слайди зі скриншотів).

## 3. Написання за форматом
| Формат | Результат | Обов'язкові правила |
|---|---|---|
| **Talking head** (чужий референс) | таблиця `оригінал \| клієнт` біт-у-біт (`calendar/reskin/<id>.md`) → SCRIPT | хук: та сама структура, 1–2 слова під клієнта; build-up до відповіді; лише факти клієнта; ~25–90 с |
| **Перезйомка свого хіта** | той самий хук дослівно + трохи змінений скрипт; NOTES: що змінити в кадрі | лише якщо `new_recordings_allowed = true` |
| **Expert video** | callout `React to this video` + NOTES: фрагмент (таймкод або цитата) + 3–5 talking points | реальний об'єкт реакції; позиція клієнта лише з контексту; без SCRIPT |
| **BTS** | NOTES: кроки зйомки точно за кадрами референсу; ON-SCREEN TEXT: плашки по порядку | без spoken script; нічого, чого немає в референсі; асети реально є |
| **Carousel** | SLIDES: Slide 1 (хук) … Slide N (фінал/CTA, якщо був у референсі), кожен з текстом; NOTES: візуал кожного слайду (фото продукту, скрин, фон) | кількість і ролі слайдів = референс; факти лише клієнта; кожне слово несе цінність |
| **Caption** (окремо або до поста) | 1–4 короткі речення: суть або цінність, не переказ скрипта; CTA лише якщо він був у референсі; хештеги клієнта | освітній, а не продажний (якщо пост освітній); без `—`, `« »`, кліше |
| **Framework** (референсу немає) | скрипт за **одним** creator skill (`dan-martell-shortform`, `nameisjoao-shortform`, `jun-yuh-shortform`, `personalbrandlaunch-shortform`, `jamesconole-shortform`, `roninxsocials-shortform`, `sharransrivatsaa-carousel` для каруселей) | вибір творця за таблицею з `$CS/cs-pipeline/brain/creator_skills_sop.md` (форма теми → творець); скелет 1:1 творця; slot-by-slot QC; у внутрішньому файлі вказати `Creator: … / Skeleton …` |

Потім: AI-slop (`sharrans-ai-slop` EN / `humanizer-ru` RU) → перевірити, що факти й хук не змінились.

## 3a. Правила, що знімають конфлікти (за тестом 2026-10-13)
- **Режими в JSON:** звичайний пост — без `mode`; лише caption до вже опублікованого відео — `"mode": "caption_only"` (Type = Type того відео, NOTES = «перепостити без змін»); скрипт без референсу — `"mode": "framework"` + `creator`, `skeleton`, `framework_slots`; один пост поза календарем — `"single": true` (Week day не обов'язковий).
- **Продукт у референсі, якого клієнт не продає** (глина, sea salt spray тощо): той самий крок і рух, але з найближчим продуктом клієнта за призначенням (за інструкцією з сайту клієнта). Записати заміну в `sources`/internal і в NOTES FOR CM. Якщо відповідника немає → інший референс.
- **Creator skill vs brain:** brain перемагає. Довжина за SOP (30–60 с), фрази з `banned_phrases.md` замінюються, CTA творця (книга, лід-магніт) → CTA з воронки клієнта лише якщо він є в контексті; інакше без CTA. Скелет творця «працюй лише з його базою рілсів» у framework-режимі не застосовується.
- **Caption:** перше речення = хук ≤7 слів (Head of Content 1.5); суть, не переказ; хештеги клієнта.
- **Carousel-референс:** переглядів немає, тому віральність вирішує CM. До рішення пост не йде в календар (`cm_viral_ok` у записі референсу).
- **Скриншоти браузера** копіювати в `clients/<slug>/work/media/<code>/`.
- `banned_terms` для перевірки = список «Не можна» з `client_rules.md`.

## 4. Перевірка
1. Записати пост як один item у `clients/<slug>/calendar/single/<id>.json` (формат `calendar_items.json`, поля з `qa_calendar.py`) і запустити
   `python3 -I $CS/cs-two-week-calendar/scripts/qa_calendar.py clients/<slug>/calendar/single/<id>.json clients/<slug>/research/reference_records.json` → exit 0.
2. **Окремий** агент `cs-quality-reviewer` (запускати субагентом, не самоперевіркою) (stage `calendar`, scope «single post <id>») → PASS або виправити (до 2 кіл).

## 5. Віддати CM
- Показати картку: `python3 -I $CS/cs-two-week-calendar/scripts/render_notion.py <item.json> <out.md> --md` → вивести в чат.
- Записати в Notion **лише після «так» CM**, у базу, яку він назве (`$CS/cs-two-week-calendar/references/notion_mapping.md`).
- Для Framework-скриптів окремо назвати творця й скелет (у внутрішньому файлі, не в картці клієнта).
