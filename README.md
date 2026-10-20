# ContentSCALE OS (Claude Code plugin)

Один процес для Content Manager: **Unpacking-дзвінок → Client Context → Content Research → Strategy (Canva) → двотижневий календар у Notion**, плюс окремі пости будь-якого формату.
Автопілот виконує етапи сам, перевіряє кожен (скрипти + незалежний агент якості за стандартами Head of Content) і зупиняється лише на рішеннях людини.

## Встановлення з ZIP (без плагіна)
1. Скачати ZIP: на сторінці репозиторію **Code → Download ZIP** або напряму:
   https://github.com/dpechenchis-design/contentscale-os-public/archive/refs/heads/main.zip
2. Розпакувати (з'явиться папка `contentscale-os-public-main` у Downloads).
3. Відкрити Claude Code і написати:
   > Встанови ContentSCALE: запусти `sh ~/Downloads/contentscale-os-public-main/install.sh`
   Claude скопіює скіли в `~/.claude/skills`, агента якості в `~/.claude/agents`, команди `/contentscale` і `/cs-status` в `~/.claude/commands` і налаштує інструменти. Скіли з такими самими назвами, які вже були, збережуться в `~/.claude/skills/.backup-<дата>/`.
4. Один раз поставити відео-інструменти: `brew install yt-dlp ffmpeg`.
5. Підключити конектори Claude: **Fathom, Notion, Canva** і **Claude in Chrome** (Instagram збирається через Chrome, де CM залогінений в Instagram). SortFeed Pro — запасний варіант.
6. Перезапустити Claude Code.

**Оновлення:** скачати свіжий ZIP і знову попросити Claude запустити `install.sh`.

Альтернатива — як плагін: `/plugin marketplace add dpechenchis-design/contentscale-os-public`, потім `/plugin install contentscale@contentscale`. Обидва способи одночасно не ставити.

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

Ця публічна версія не містить клієнтських даних: імена, ID і приклади замінені на нейтральні. Дані клієнтів зберігаються лише локально в папці `clients/` у CM.
