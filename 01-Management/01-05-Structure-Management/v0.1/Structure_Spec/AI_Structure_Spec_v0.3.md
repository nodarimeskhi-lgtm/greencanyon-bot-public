# Спецификация: Гибридная структура данных "Человек-ИИ" (v0.3)

Для обеспечения беспрепятственного сотрудничества между людьми и ИИ-агентами (Antigravity, Cursor, Windsurf, Copilot), все данные в Структуре Управления Galt должны следовать этим рекомендациям.

## 1. Концепция "Цепочка Контекста" (Context Chain)

Чтобы **любой** новый ИИ-агент следовал правилам, мы используем принцип **принудительной инициализации контекста**. Агент не должен угадывать правила; он должен получить их в своем системном промпте.

### Почему это работает?
Большинство современных агентов (Cursor, GitHub Copilot) запрограммированы искать конфигурационные файлы в корне проекта перед началом работы. Мы используем это поведение.

## 2. Корневые Правила (Root Rules)

В корневой папке `Galt/` (или `Management/`) создаются "маяки" для разных типов агентов.

### Файл `.cursorrules` (Для Cursor AI и аналогов)
Этот файл автоматически считывается Cursor AI и добавляется в системный промпт.

```markdown
# Galt Management System Rules

YOU ARE AN AI AGENT WORKING IN THE GALT MANAGEMENT SYSTEM.
YOU MUST FOLLOW THESE PRIME DIRECTIVES:

1.  **CONTEXT FIRST**: Before creating or editing ANY file, you MUST read the `_AI_CONTEXT.md` file in the target directory (and its parent).
2.  **METADATA MANDATORY**: Every Markdown file MUST have YAML frontmatter.
3.  **OWNERSHIP PROTOCOL**:
    -   Determine Author from Git User.
    -   Determine Owner from `_AI_CONTEXT.md`.
4.  **NO HALLUCINATIONS**: Do not invent policies. If a rule is missing in `_AI_CONTEXT.md`, ASK the user.
```

### Файл `AI_GUIDELINES.md` (Для универсальных LLM / ChatGPT)
Читаемый человеком и машиной манифест.

## 3. Стандарты директорий (`_AI_CONTEXT.md`)

Каждая значимая папка ДОЛЖНА содержать файл `_AI_CONTEXT.md`.

**Шаблон:**

```markdown
# Контекст: [Имя папки]
## Назначение
[Описание]
## Владельцы (Default Owners)
- **Codeowner**: @marketing-team
- **Role**: CMO
## Специфичные правила
- Не использовать сокращения в именах файлов.
- Все бюджеты только в XLSX.
```

## 4. Алгоритм действий Агента (The Protocol)

Любой агент, подключаемый к системе, должен следовать алгоритму:

1.  **INIT**: Прочитать `.cursorrules` (или `AI_GUIDELINES.md`).
2.  **LOCATE**: Определить целевую папку для задачи.
3.  **LOAD**: Прочитать `_AI_CONTEXT.md` в этой папке.
4.  **EXECUTE**: Выполнить задачу, соблюдая ограничения из шага 3.
5.  **VALIDATE**: Проверить, что созданный файл имеет корректный YAML Frontmatter.

## 5. Алгоритм определения Владельца и Автора

Система использует гибридный подход:

### Атрибут `author` (Создатель)
*   Источник: Git History (`git config user.email`).

### Атрибут `owner` (Ответственный)
*   Источник: Каскадное наследование из `_AI_CONTEXT.md`.

## 6. Нетекстовые файлы

Использовать `manifest.yaml` для маппинга бинарных файлов.
