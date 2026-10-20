# Brain ContentSCALE: що знає система

Одна база знань для всіх етапів і всіх CM. Кожен етап і агент якості читають потрібні файли звідси, а не з пам'яті чи чату.
Пріоритет при конфлікті: **слова CM у цьому діалозі → `clients/<slug>/client_rules.md` → `team_decisions.md` → решта brain → загальні знання.**

| Файл | Що в ньому | Коли читати |
|---|---|---|
| `team_decisions.md` | Затверджені рішення команди (Notion, Canva, Types, cadence, правило 2×, перезйомки, скетчі) | Завжди на старті роботи з клієнтом |
| `quality_bar.md` | Як виглядає «добре»: еталони (досьє, стратегія, картка календаря), топ-правила Head of Content, що вважається браком | Перед кожним результатом і перед перевіркою якості |
| `feedback_patterns.md` | Повний корпус фідбеку Head of Content: хуки, скрипти, captions, стратегія, процес, тон | Скрипти, captions, календар, перевірка якості |
| `banned_phrases.md` | Заборонені фрази й кліше рівня агенції | Будь-який клієнтський текст |
| `creator_skills_sop.md` | SOP: як користуватися creator skills (load client → pick creator → generate → slot QC) | Коли скрипт пишеться за фреймворком, а не з референсу 1:1 |
| `assets.md` | ID і посилання: майстер стратегії й резерви, еталонне досьє, схема Notion, тестові бази | Етапи 1, 3, 4 |
| `onboarding_brief_template.md` | Онбординг-бриф: перелік матеріалів, правило 5 джерел, параметри, Client Working Model і її вплив на етапи | Етап 1, до старту роботи |
| `client_rules_template.md` | Шаблон `clients/<slug>/client_rules.md` | Створити на етапі 1; поповнювати після кожної відповіді CM |

Creator skills (dan-martell, personalbrandlaunch, jamesconole, nameisjoao, jun-yuh, roninxsocials, sharransrivatsaa-carousel, hormozi-leads), `sharrans-ai-slop` і `humanizer-ru` уже входять у плагін. Окремо їх встановлювати не треба (крок 1 SOP про `git clone` для плагіна не потрібен).

## Як brain поповнюється
- Нове рішення CM або Head of Content, що стосується **всіх** клієнтів → дописати в `team_decisions.md` (дата, хто вирішив) і запропонувати оновлення плагіна.
- Рішення про **одного** клієнта → `clients/<slug>/client_rules.md`.
- Нова помилка, знайдена в перевірці → новий тест у `cs-two-week-calendar/references/regression_tests.md` + правило в `quality_bar.md`.
