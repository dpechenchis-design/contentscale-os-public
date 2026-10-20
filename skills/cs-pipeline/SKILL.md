---
name: cs-pipeline
description: >
  ContentSCALE OS — єдиний процес від готового Unpacking-дзвінка до двотижневого контент-календаря в Notion.
  Автопілот: сам визначає етап клієнта, виконує етапи (context → research → strategy → calendar), після
  кожного запускає автоматичні перевірки й незалежного агента якості, і зупиняється лише на рішеннях людини.
  Містить «мозок» команди (рішення, правила Head of Content, еталони якості, SOP). Використовуй, коли кажуть:
  новий клієнт, запусти пайплайн, contentscale, продовжи клієнта, що далі по клієнту, статус клієнта,
  онбординг після unpacking, зроби все для клієнта, cs-pipeline.
---

# ContentSCALE OS: автопілот

> **Шляхи.** `$CS` = папка зі скілами плагіна ContentSCALE = батьківська папка для «Base directory for this skill», яку Claude показує під час завантаження скіла. У командах підставляй повний шлях замість `$CS`. Python для скриптів, яким потрібні бібліотеки: `~/.contentscale-venv/bin/python` (створює `sh $CS/cs-pipeline/scripts/setup.sh`).

**Мета:** CM каже «клієнт X» → система робить усе, що може зробити сама, якісно й перевірено. CM приходить лише туди, де потрібна людина.
**Не входить:** дзвінки, Unpacking, створення Notion Hub, editing, публікація.

## 0. Старт кожної сесії
1. `brain/README.md` → прочитати `brain/team_decisions.md`, `brain/quality_bar.md`.
2. Визначити клієнта (`clients/<slug>/`, slug латиницею через дефіс). Немає папки → `mkdir -p clients/<slug>/sources`.
3. `python3 -I $CS/cs-pipeline/scripts/pipeline_status.py clients/<slug>`: показує етап, блокери й **NEXT**.
4. Прочитати `clients/<slug>/client_rules.md` (якщо є).
5. Коротко показати CM статус (3–5 рядків) і одразу продовжити роботу з NEXT, не чекаючи «можна?», якщо наступний крок не є gate.

## 1. Цикл автопілота (для кожного етапу)
```
виконати етап (скіл етапу) ─► автоматична QA-перевірка етапу (скрипт) ─► агент cs-quality-reviewer
      ▲                                                                       │
      └──────────── виправити FIXES (до 2 кіл) ◄───────── VERDICT: FIX ◄──────┘
                                                                              │ PASS
                                                       GATE: показати CM коротко + питання
                                                       CM «так» → pipeline_status.py --approve <gate>
```
- Етап виконувати за інструкцією скіла етапу. Великі етапи (досьє, стратегія в Canva, день календаря) можна віддати субагенту `general-purpose` з повним посиланням на SKILL.md етапу, правилами клієнта й brain. Результат перевіряєш ти.
- **Агент якості:** субагент `cs-quality-reviewer` (з плагіна або з `~/.claude/agents` після встановлення з ZIP) з параметрами `stage`, `client_dir`, `scope`, `brain_dir = $CS/cs-pipeline/brain`. Він лише читає й звітує.
- Після 2 кіл FIX без PASS → показати CM, що лишилося, з готовими варіантами. Не приховувати.
- Gate ніколи не вважається пройденим без явного «так» CM у чаті. Погодження записується: `pipeline_status.py clients/<slug> --approve <gate> --note "<що саме погоджено>"`.

## 2. Етапи і gate'и
| # | Скіл | Що робить сам | Gate (людина) | `--approve` |
|---|---|---|---|---|
| 1 | `cs-client-context` | транскрипт із Fathom, факти з джерелами, Working Model, відгуки, досьє, verify | досьє + критичні питання | `dossier` |
| 2 | `cs-content-research` | акаунти й підписники, правило 2×, канонічна таблиця, Type за кадрами, транскрипти | **TikTok і Instagram збираються автоматично (Instagram через Chrome CM); SortFeed — запасний варіант**; AI-конкуренти approve/reject; огляд таблиці | `competitors`, `research` |
| 3 | `cs-content-strategy` | fact map, текст, AI-slop, check, копія майстра в Canva, фото | cadence/Types, якщо їх немає; прев'ю Canva → commit | `strategy` (+ `--set strategy_design_id=…`) |
| 4 | `cs-two-week-calendar` | план 14 днів, референси, feasibility, тексти за Type, QA, Notion | 1 тестова сторінка; кожен день | `calendar_test_page`, `calendar_w<N>_<Day>` |

## 2a. Поза пайплайном
Один пост, скрипт або caption на запит → `cs-post-writer` (потрібен готовий контекст клієнта).

## 3. Правила клієнта
- `clients/<slug>/client_rules.md` створюється на етапі 1 з `brain/client_rules_template.md`.
- **Кожна відповідь CM про цього клієнта** (cadence, продукти, згоди, Type для специфічних форматів) одразу дописується туди з датою. Правила клієнта перекривають `team_decisions.md`.
- Рішення для всіх клієнтів → запропонувати CM дописати в `brain/team_decisions.md` (це оновлення плагіна).

## 4. Якість (не обговорюється)
1. Факти лише з Unpacking, матеріалів клієнта й відповідей CM. Немає факту → `UNKNOWN` + питання. Нічого не вигадувати.
2. Клієнтський текст: `sharrans-ai-slop` (EN) або `humanizer-ru` (RU), потім повторна перевірка фактів. Без `brain/banned_phrases.md`.
3. Скрипти за референсом 1:1. За фреймворком — лише через creator skills за `brain/creator_skills_sop.md`.
4. Перед кожним gate: QA-скрипт етапу exit 0 + агент якості PASS.
5. Клієнтські документи без внутрішнього: усе внутрішнє йде в `qa_log.md` / `internal_qa_report.md`.
6. Чужі календарі й затверджені стратегії лише читати. Працювати в копіях.

## 5. Що завжди робить людина
- Бути залогіненим в Instagram у своєму Chrome (Claude читає публічні профілі через браузер). SortFeed — лише запасний варіант.
- Погодження gate'ів і `Approved?` у research-таблиці.
- Відповіді на критичні питання.
- Дрібні ручні правки, які коннектори не вміють: шрифт у Canva, жирний після мітки (Claude називає такі місця).

## 6. Довідники
- Runbook для CM: `references/runbook.md`.
- Мозок: `brain/` (рішення, якість, правила Head of Content, SOP, ресурси).
- Структура папки клієнта:
  `sources/` · `context/` · `research/` · `strategy/` · `calendar/` · `work/` · `client_rules.md` · `pipeline_state.json`.
- Одноразове налаштування: `sh $CS/cs-pipeline/scripts/setup.sh`; конектори Fathom, Notion, Canva; SortFeed Pro у Chrome.
