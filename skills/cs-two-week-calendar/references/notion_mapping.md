# Notion: канонічна схема календаря (база `Week 1`, затверджено 2026-10-13)

Еталон: «<Client> Content calendar» → база `Week 1` (лише читати; **ніколи не змінювати чужі календарі**).
Новий клієнт: база з тією ж схемою в його Notion Hub (створює команда або скіл після дозволу CM).

## Properties
| Property | Тип | Що писати | Заборонено |
|---|---|---|---|
| `Name` | title | Тема поста коротко, як назвав би CM («Natural shampoo isn't supposed to foam») | AI-заголовки, однакові «сильні» назви, що суперечать джерелу |
| `Week day` | select | Monday…Sunday | дати |
| `Status` | select | `Script ready` (рішення 2026-10-13) | інші статуси без вказівки CM |
| `Type` | multi_select | одне з `Talking head` / `Expert video` / `BTS` / `Carousel` (`YouTube` для long-form). **Рішення 2026-10-13:** у клієнтів, у стратегії яких є каруселі, база має опцію `Carousel` (у новій базі створюється разом зі схемою; в наявній CM додає опцію або погоджує, щоб її додав Claude) | змішувати з Format |
| `Format` | multi_select | одна з 3–4 категорій зі стратегії (the client: Proof / Objection handling / Connection / Education) | нові категорії |
| `Platforms` | multi_select | з cadence стратегії (the client: TT, і ці ж відео в IG → `TT` + `IG`) | — |
| `Reference` | url | URL референсу з research (`reference_records.json`) | URL, якого немає в research |
| `Source` | multi_select | Походження ідеї, лише якщо CM задав правило. В еталоні порожньо → **лишати порожнім** | — |
| `Instructions ` | url | (з пробілом у назві) порожньо, якщо CM не дав посилання | — |
| `Publishing date` | date | **завжди порожньо** | будь-яка дата |
| `Edited video` | url | **порожньо** до editing | — |

## Тіло сторінки (Notion enhanced markdown, як у реальних сторінках еталона)
```
<callout icon="🎯" color="gray_bg">
	**Reference:** [@account, 273K views](https://…)
	**React to this video:** [https://…](https://…)          ← тільки Expert video
</callout>
## **NOTES FOR THE CLIENT**
<конкретні кроки: що зняти / показати / сказати; без внутрішніх приміток>
## SCRIPT                                                  ← тільки Talking head (і Re-record)
<готовий до запису текст>
## ON-SCREEN TEXT                                          ← BTS (замість SCRIPT)
## SLIDES                                                  ← Carousel (Slide 1 … Slide N)
## CAPTION
<caption + хештеги за патерном клієнта>
```
- `Reference` callout: `@<акаунт>, <перегляди скорочено>` з research (наприклад, `696.9K views`). Цифра тільки з research.
- У тілі **немає**: пояснень «чому обрали», стратегії, слів «AI/Claude/скіл», статусів QA, внутрішніх ID. Це йде в `calendar/internal_qa_report.md`.

## Запис (Notion MCP)
1. `notion-fetch` бази → `collection://…` і схема; звірити properties з таблицею вище. Розбіжність → стоп і питання CM.
2. Створити **1 тестову сторінку** → показати CM посилання → «так» → решта.
3. Запис порціями по одному дню (`Week day`), щоб CM/Head of Content переглядали день за днем.
4. Не дублювати: перед створенням пошукати сторінку з тим самим `Name` + `Week day`. Затверджені сторінки (`Client: approved`, `QA: Approved`) не перезаписувати.
