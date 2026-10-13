# ContentSCALE OS (Claude Code plugin)

Один процес для Content Manager: **Unpacking-дзвінок → Client Context → Content Research → Strategy (Canva) → двотижневий календар у Notion**.
Автопілот виконує етапи сам, перевіряє кожен (скрипти + незалежний агент якості за стандартами Head of Content) і зупиняється лише на рішеннях людини.

## Встановлення (один раз на комп'ютері)
1. У терміналі Claude Code:
   ```
   /plugin install contentscale --marketplace dpechenchis-design/contentscale-os-public
   ```
   `y`, щоб додати marketplace → scope **user**. Репозиторій приватний: потрібен доступ до нього в GitHub.
2. Python-середовище й інструменти:
   ```
   brew install yt-dlp ffmpeg
   ```
   потім у Claude: «запусти setup ContentSCALE» (або `sh <папка плагіна>/skills/cs-pipeline/scripts/setup.sh`).
3. Конектори Claude: **Fathom, Notion, Canva**. У Chrome: **SortFeed Pro**.

## Як працювати
- `/contentscale <клієнт>` — почати або продовжити клієнта.
- `/cs-status <slug>` — на якому етапі клієнт і що далі.
- Інструкція для CM: `skills/cs-pipeline/references/runbook.md`.

## Що всередині
| Частина | Що це |
|---|---|
| `skills/cs-pipeline` | Автопілот, статус клієнта, runbook, **brain/** (рішення команди, quality bar, правила Head of Content, заборонені фрази, SOP, ресурси) |
| `skills/cs-client-context` | Етап 1: факти з Unpacking з джерелами, Working Model, досьє, перевірка цитат |
| `skills/cs-content-research` | Етап 2: експорти SortFeed → канонічна research-таблиця, правило 2×, Type за кадрами, транскрипти |
| `skills/cs-content-strategy` | Етап 3: стратегія за структурою reference у Canva з майстра (з резервами) |
| `skills/cs-two-week-calendar` | Етап 4: календар у Notion, format guides, 18 regression-тестів |
| `agents/cs-quality-reviewer` | Незалежна перевірка кожного результату перед CM |
| creator skills, `sharrans-ai-slop`, `humanizer-ru` | Залежності, вже включені |

## Оновлення
`/plugin update contentscale` після нових комітів. Зміни правил для всіх клієнтів вносяться в `skills/cs-pipeline/brain/team_decisions.md`.

> Приватний репозиторій: містить внутрішні правила й приклади клієнтських даних. Не робити публічним.
