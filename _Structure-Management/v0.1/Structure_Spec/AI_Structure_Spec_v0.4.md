# Спецификация: Гибридная структура данных "Человек-ИИ" (v0.4)

Для обеспечения беспрепятственного сотрудничества между людьми и ИИ-агентами (Antigravity, Cursor, Windsurf, Copilot), все данные в Структуре Управления Galt должны следовать этим рекомендациям.

## 1. Принцип "Приватно по умолчанию" (Private by Default)

**ГЛАВНОЕ ПРАВИЛО:** Любой новый файл считается **скрытым** для ИИ-агентов, пока человек явно не разрешит доступ. Это создает безопасное пространство для черновиков и экспериментов.

### Механизм
Агенты должны игнорировать файл, ЕСЛИ:
1.  В файле **отсутствует** YAML Frontmatter (метаданные).
2.  В метаданных явно не указано `ai_access: true`.
3.  Статус документа равен `draft` (черновик) или `experiment` (эксперимент).

## 2. Стандарты файлов (Markdown)

Чтобы файл стал видимым для ИИ (для анализа, контекста или редактирования), человек должен добавить метаданные.

```yaml
---
id: unique-slug
type: policy
status: draft | approved
owner: [Role]
ai_access: true   <-- ТОЛЬКО С ЭТИМ ФЛАГОМ АГЕНТ ЧИТАЕТ ФАЙЛ
ai_permissions:
  edit: false
---
```

## 3. Концепция "Цепочка Контекста" (Context Chain)

Чтобы **любой** новый ИИ-агент следовал правилам, мы используем принцип **принудительной инициализации контекста**.

## 4. Корневые Правила (Root Rules)

### Файл `.cursorrules` (Для Cursor AI)

```markdown
# Galt Management System Rules

YOU ARE AN AI AGENT WORKING IN THE GALT MANAGEMENT SYSTEM.

PRIME DIRECTIVE: **DO NOT READ OR ANALYZE FILES WITHOUT EXPLICIT PERMISSION.**

1.  **CHECK VISIBILITY**:
    -   Does the file have a YAML header?
    -   Does it have `ai_access: true`?
    -   IF NO to either -> IGNORE THIS FILE. Treat it as blank/non-existent.

2.  **CONTEXT FIRST**: Before creating ANY file, read `_AI_CONTEXT.md` in the target directory.
3.  **OWNERSHIP PROTOCOL**: Determine Author (Git) and Owner (Context).
```

## 5. Стандарты директорий (`_AI_CONTEXT.md`)

Каждая значимая папка ДОЛЖНА содержать файл `_AI_CONTEXT.md`.

**Шаблон:**

```markdown
# Контекст: [Имя папки]
## Назначение
[Описание]
## Владельцы (Default Owners)
- **Role**: CMO
## Инструкция по умолчанию
"Все новые файлы в этой папке считаются черновиками. Не индексировать их содержимое, пока пользователь не изменит статус на `review`."
```

## 6. Алгоритм действий Агента (The Protocol)

Любой агент, подключаемый к системе, должен следовать алгоритму:

1.  **INIT**: Прочитать `.cursorrules`.
2.  **SCAN**: Проверить файл на наличие `ai_access: true`.
3.  **SKIP**: Если флага нет — пропустить.
4.  **LOAD**: Если флаг есть — загрузить контекст и выполнить задачу.
