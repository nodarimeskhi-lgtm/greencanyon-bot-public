---
id: project-deployment-template-v02
type: template
status: approved
ai_access: true
owner: Management
author: @levadiani
classification: internal
summary: "Шаблон инструкций для развертывания нового проекта в структуре Galt (v0.2)."
topics: [project, template, deployment, structure]
language: ru
---

# Шаблон Развертывания Нового Проекта (v0.2)

Эта инструкция предназначена для создания (развертывания) нового проекта в папке `05-Projects` в соответствии со стандартами Galt v0.2.

## 1. Инициализация Папки Проекта

1.  Создайте корневую папку проекта: `05-Projects/[Project-Name]`.
    *   *Правило*: Используйте `PascalCase` или `kebab-case`. Без пробелов.
    *   *Пример*: `05-Projects/Galt-HQ`

2.  Создайте стандартную иерархию подпапок (PMBOK/ISO Lifecycle):

    *   [ ] `1-Management` (Управление)
        *   `1-1-Charter`
        *   `1-2-Schedule`
        *   `1-3-Budget`
        *   `1-4-Risks`
        *   `1-5-Meetings`
        *   `1-6-Correspondence`
        *   `_Drafts`
    *   [ ] `2-Permits-Legal` (ИРД)
        *   `2-1-Land`
        *   `2-2-Permits`
        *   `2-3-Approvals`
        *   `2-4-Project-Contracts`
        *   `_Drafts`
    *   [ ] `3-Design` (Проектирование)
        *   `3-1-Concept`
        *   `3-2-Stage-P`
        *   `3-3-Stage-RD`
        *   `3-4-BIM-Model`
        *   `_Drafts`
    *   [ ] `4-Construction` (Строительство)
        *   `4-1-Site-Log`
        *   `4-2-Photo-Reports`
        *   `4-3-Acts`
        *   `_Drafts`
    *   [ ] `5-Supply` (Снабжение)
        *   `5-1-Requests`
        *   `5-2-Invoices`
        *   `5-3-Logistics`
        *   `_Drafts`
    *   [ ] `9-Archive-[ProjectName]` (Архив)

## 2. Создание Контекста Проекта

В корне папки проекта (`05-Projects/[Project-Name]/`) создайте файл `_AI_CONTEXT.md`.

**Шаблон `_AI_CONTEXT.md`:**

```markdown
# Контекст Проекта: [Название Проекта]

## Обзор
[1-2 абзаца о сути проекта: что строим/делаем, где, для кого, основные цели.]

## Ключевые параметры
*   **Тип**: [Девелопмент / Консалтинг / IT]
*   **Локация**: [Адрес]
*   **Статус**: [Инициация / Проектирование / Строительство]

## Команда (Roles)
*   **PM (РП)**: [ФИО]
*   **Архитектор**: [ФИО]
*   **Заказчик**: [ФИО/Компания]

## Специфичные правила
*   Черновики строго в `./_Drafts`
*   Все официальные документы должны иметь YAML frontmatter.
```

## 3. Создание Устава Проекта (Project Charter)

В папке `1-Management/1-1-Charter/` создайте стартовый документ: `Project-Charter.md`.

**Шаблон `Project-Charter.md`:**

```yaml
---
id: [project-name]-charter
type: policy
status: draft
ai_access: true
owner: Project Manager
author: [Your Name]
classification: internal
summary: "Устав проекта [Название], определяющий цели, вехи и бюджет."
topics: [charter, initiation, goals]
language: ru
---

# Устав Проекта: [Название]

## 1. Цели Проекта
1.  [Цель 1]
2.  [Цель 2]

## 2. Ключевые Вехи (Milestones)
*   [Дата]: Старт проекта
*   [Дата]: Получение РНС
*   [Дата]: Окончание стройки

## 3. Бюджет (Верхнеуровневый)
*   CAPEX: [Сумма]
*   OPEX: [Сумма]
```

## 4. Проверка (Checklist)

*   [ ] Структура папок создана (1-Management ... 9-Archive).
*   [ ] Файл `_AI_CONTEXT.md` в корне проекта заполнен.
*   [ ] Создан Устав (Charter) или карточка проекта.
*   [ ] Проверено отсутствие пробелов в путях.
