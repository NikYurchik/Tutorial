Many people have a folder on their desktop called something like "Disassemble". As a rule, hands never manage to disassemble this folder.

This is a script that will parse this folder. To do this, the application checks the file extension (the last characters in the file name, usually after a dot) and, depending on the extension, decides to which category to assign this file.

The script accepts one or two arguments when running — the name of the folder it will parse and the name of the folder where the parse result will be saved. If the second argument is not specified or coincides with the first, then the result will be saved in the same folder that will be parsed. The result will initially be stored in an intermediate folder, and when the analysis is finished, the primary folder will be deleted, and the intermediate folder will be renamed to the primary one.

The script goes through the folder to any nesting depth and sorts all files into groups:
- image ('JPEG', 'PNG', 'JPG', 'SVG');
- video files ('AVI', 'MP4', 'MOV', 'MKV');
- documents ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
- music ('MP3', 'OGG', 'WAV', 'AMR');
- archives ('ZIP', 'GZ', 'TAR');
- unknown extensions.

As a result, all files will be renamed using the normalize function. File extensions do not change.
The normalize function:
Transliterates the Cyrillic alphabet into Latin. After transliteration, uppercase letters remain uppercase and lowercase letters remain lowercase.
All other characters except Latin letters and numbers are changed to '_'.

As a result of processing:
- images are transferred to the images folder;
- documents are transferred to the documents folder;
- audio files are transferred to audio;
- video files to video;
- archives are unpacked and their contents are transferred to the archives folder in a subfolder named the same as the archive, but without the extension at the end;
- files whose extensions are unknown are transferred directly to the destination folder;
- empty folders are deleted.
-------------------------------------------------------------------------------------------------------------------------------------------
У багатьох на робочому столі є папка, яка називається якось ніби "Розібрати". Як правило, розібрати цю папку руки ніколи так і не доходять.

Це скрипт, який розбере цю папку. Для цього додаток перевіряє розширення файлу (останні символи у імені файлу, як правило, після крапки) і, залежно від розширення, приймає рішення, до якої категорії віднести цей файл.

Скрипт приймає один або два аргументі при запуску — це ім'я папки, яку він буде розбирати, та ім'я папки, в яку буде зберігатися результат розбору. Якщо другий аргумент не заданий або співпадає з першим, то результат буде збережений в тій самій папці, що буде розбиратися. Результат спочатку буде зберігатися в проміжній папці, а по закінчкнню розбору первинна папка буде видалена, а проміжня перейменована в первинну.

Скрипт проходить папку на будь-яку глибину вкладеності та сортує всі файли по групам:
- зображення ('JPEG', 'PNG', 'JPG', 'SVG');
- відео файли ('AVI', 'MP4', 'MOV', 'MKV');
- документи ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
- музика ('MP3', 'OGG', 'WAV', 'AMR');
- архіви ('ZIP', 'GZ', 'TAR');
- невідомі розширення.

В результатах роботи всі файли будуть перейменовані з застосуванням функції normalize. Розширеня файлів при цьому не змінюются.
Функція normalize:
Проводить транслітерацію кирилічного алфавіту на латинський. Після транслітерації великі літери залишаються великими, а маленькі — маленькими.
Всі інші символи крім латинських літер та цифр змінюються на '_'.

В результаті обробки:
- зображення переносяться до папки images;
- документи переносяться до папки documents;
- аудіо файли переносяться до audio;
- відео файли до video;
- архіви розпаковуються та їх вміст переноситься до папки archives у підпапку, названу так само, як і архів, але без розширення у кінці;
- файли, розширення яких невідомі, переносяться безпосередньо до папки призначення;
- порожні папки видаляються.
