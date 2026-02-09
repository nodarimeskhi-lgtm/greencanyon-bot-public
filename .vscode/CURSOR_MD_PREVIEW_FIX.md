# Обходной путь: ошибка «Unable to open» в Markdown Preview

## Причина

В Cursor известен баг: **Markdown Preview** (и другие кастомные редакторы) не могут открыть файл, пока он не был открыт **хотя бы раз в обычном текстовом редакторе**. Документ инициализируется «лениво», и при первом открытии сразу в preview возникает: *Assertion Failed: Argument is `undefined` or `null`*.

Подробнее: [Assertion error when using custom editors (forum.cursor.com)](https://forum.cursor.com/t/assertion-error-when-using-custom-editors-incl-markdown-preview-editors/148578).

## Что сделать один раз (по каждому проблемному файлу)

1. В проводнике Cursor **правый клик** по `.md` файлу.
2. Выбрать **Open With…** → **Text Editor**.
3. Файл откроется в виде кода; можно сразу закрыть вкладку.
4. После этого этот файл можно открывать в **Markdown Preview** — ошибка не повторится.

Ничего сохранять или принимать в diff не нужно: достаточно одного открытия в Text Editor.

## Дополнительно

- В `settings.json` добавлено `"office-viewer.autoOpen": false` — если установлен Office Viewer, это снижает конфликты с preview.
- Если ошибка остаётся: отключите расширение **Office Viewer** (Ctrl+Shift+X → Office Viewer → Disable) и проверьте открытие .md снова.
