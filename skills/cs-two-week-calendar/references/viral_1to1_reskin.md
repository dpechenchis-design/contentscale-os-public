# Виральный ход №1: полный 1:1 реског виральной видео (метод + примеры Head of Content)

Правка Head of Content 09.07.2026: для 🟣 ВИРАЛА с референсом — не писать «по мотивам», а брать конкретное
залетевшее видео и переделывать ЕГО ЦЕЛИКОМ один-в-один: тот же скелет, тот же ритм, тот же счётчик
битов, те же типы строк. Меняем ТОЛЬКО переменные под нишу/клиента. Это сильнее генерации из фреймворка,
потому что структура уже доказана просмотрами, и убирает риск «наиграно» (ничего не выдумываем).

## Метод
1. Взять конкретный виральный референс (из выгрузки Sort Feed, со ссылкой и метрикой).
2. Вытянуть ДОСЛОВНЫЙ транскрипт оригинала (vidiq_ig_reel_watch по shortcode / video_transcript).
3. Разобрать его скелет построчно: каждая строка = что за бит (хук-тип, пример, число, CTA).
4. Переписать строка-в-строку, подставляя: нишу, примеры, числа, кодовое слово CTA клиента.
5. НЕ добавлять/убирать биты, не менять порядок, не «улучшать» структуру.

## ФОРМАТ ВЫВОДА (правка Head of Content 09.07.2026): ДВЕ КОЛОНКИ
Всегда выдавать реског таблицей: ЛЕВАЯ колонка = дословный транскрипт оригинала (со ссылкой+метрикой в
шапке), ПРАВАЯ = версия клиента, ВЫРОВНЕННАЯ бит-в-бит (каждый бит = своя строка таблицы, слева и справа
на одном уровне). Так видно, что это 1:1, а не «по мотивам». Как в эталонных примерах Head of Content (Original |
Content SCALE). Markdown-таблица (легко переносится в Notion).

## Гейты (обязательно)
- **Честность:** каждая подставленная заявка = правда для клиента («I've coached over 200 clients» —
  только если реально 200; «$1.5M/month» — если это не так, реског НЕ спасает, меняем на честную цифру).
- **On-topic ICP:** переменные из НИШИ клиента, не тащить чужую тему только потому, что оригинал забавный.
- **Voice-notes гейт:** если тело несёт тезис/мнение — подставляем СЛОВА клиента (из ДНК/voice notes),
  не чужую позицию.
- **ToV поверх:** лексика клиента, но структура/ритм оригинала не трогаются.

## Примеры Head of Content (Original → Content SCALE), эталон реского

### Пример 1 — «which hook is better A/B/C» → под коучей
Original: «Which written hook is better, A, B, or C?… two main types of written hooks I see consistently
working. Type one is super simple, bare bone… type two, hooks that have some personality… Follow for more
social media marketing education.»
Reskin: «Which hook is better, A, B, or C?… two main types of hooks I see consistently BOOKING CALLS…
Type one super simple, direct, no extra words… type two, hooks with personality: a story, a specific
number, a relatable moment, a confession or comparison… Follow for more content strategy for coaches.»
→ скелет 1:1, сменена ниша (viral → booking calls для коучей) и CTA.

### Пример 2 — «100/1k/1M view hook» мета-формат → под фитнес
Original (парфюм/black opium): «Couldn't sleep wanting to compare the three black opiums I own… I've spent
over $10,000 on smelly water, three biggest regrets… I have over 500 bottles of perfume, if I lost them
all and started from scratch these are the ones I'd pick… Who will grow bigger calves?»
Reskin (фитнес): «Couldn't sleep wanting to compare three pre-workouts I've been taking… I've spent over
$10,000 on supplements, three biggest regrets… I've coached over 200 clients, if I started my own
transformation from scratch these are the only things I'd do… Who will lose more fat, cardio every day or
lifts 3× a week?»
→ каждый бит (100/1k/1M) сохранён, переменные сменены на фитнес; числа честные под клиента.

### Пример 3 — «45 minutes to plan a month of content» → под коуч-бизнес + система CS
Original: 5 шагов (posting match → schedule → topics → types → plan month) + CTA «comment HOOK».
Reskin: те же 5 шагов, но язык системы Content SCALE (content commitment: light/consistent/full system;
content pillars = core offer + 3-5 pain points; content mix: attract/nurture/convert + формат и владелец
каждого) + CTA «comment PLAN, done-for-you content plan template for coaches».
→ структура 1:1, наполнение под её оффер и ICP.

## Когда реског vs фреймворк
- Есть конкретный виральный референс → **реског 1:1** (этот файл). Основной ход для 🟣.
- Нет референса → генерация по dan-martell-shortform (Question→Hook→Explain→Illustrate→Lesson→Hook2).
