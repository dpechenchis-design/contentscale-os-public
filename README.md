# ContentSCALE OS (Claude Code plugin)

Один процес для Content Manager: **Unpacking-дзвінок → Client Context → Content Research → Strategy (Canva) → двотижневий календар у Notion**, плюс окремі пости будь-якого формату.
Автопілот виконує етапи сам, перевіряє кожен (скрипти + незалежний агент якості за стандартами Head of Content) і зупиняється лише на рішеннях людини.

## Встановлення (один раз на комп'ютері)
1. У Claude Code:
   ```
   /plugin marketplace add dpechenchis-design/contentscale-os-public
   /plugin install contentscale@contentscale
   ```
   Scope: **user**.
2. Інструменти (безкоштовні):
   ```
   brew install yt-dlp ffmpeg
   ```
   потім у Claude: «запусти setup ContentSCALE» (створює `~/.contentscale-venv` з openpyxl і faster-whisper).
3. Конектори Claude: **Fathom, Notion, Canva**, а також **Claude in Chrome** (Instagram збирається через Chrome, де CM залогінений в Instagram). SortFeed Pro — запасний варіант.

## Як працювати
- `/contentscale <клієнт>` — почати або продовжити клієнта.
- `/cs-status <slug>` — на якому етапі клієнт і що далі.
- Інструкція для CM: `skills/cs-pipeline/references/runbook.md`.

## Що всередині
| Частина | Що це |
|---|---|
| `skills/cs-pipeline` | Автопілот, статус клієнта, runbook, **brain/** (рішення команди, quality bar, правила Head of Content, заборонені фрази, SOP) |
| `skills/cs-client-context` | Етап 1: факти з Unpacking з джерелами, Working Model, досьє, перевірка цитат |
| `skills/cs-content-research` | Етап 2: TikTok автоматично (yt-dlp), Instagram через браузер, правило 2×, Type за кадрами, транскрипти локально (Whisper) |
| `skills/cs-content-strategy` | Етап 3: стратегія в Canva з майстра (з резервами) |
| `skills/cs-two-week-calendar` | Етап 4: календар у Notion, format guides, 18 regression-тестів |
| `skills/cs-post-writer` | Один пост: Talking head, BTS, Carousel, Expert video, caption |
| `agents/cs-quality-reviewer` | Незалежна перевірка кожного результату перед CM |
| creator skills, `sharrans-ai-slop`, `humanizer-ru` | Залежності, вже включені |

## Оновлення
`/plugin update contentscale`.

Ця публічна версія не містить клієнтських даних: імена, ID і приклади замінені на нейтральні. Дані клієнтів зберігаються лише локально в папці `clients/` у CM.
