<!-- ЛОГОТИП ПРОЕКТА -->
<br />
<div align="center">
  
  ![aura text](https://github.com/user-attachments/assets/ebc56c38-c7c3-499a-b68b-28cfcdd4ab6d)
  
  <a style="text-decoration:none">
    <img src="https://img.shields.io/github/downloads/rohankishore/Aura-Text/total.svg"/>
  </a>  <a href='https://ko-fi.com/V7V7QZ7GS' target='_blank'><img height='10' style='border:0px;height:22px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=3' border='1' alt='Buy Me a Coffee at ko-fi.com' /></a>
      
  <p align="center">
    IDE, созданная полностью на Python
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/wiki"><strong>Изучить документацию »</strong></a>   
    <br />
    <br />
    <a href="https://github.com/rohankishore/Aura-Text/issues">Сообщить об ошибке</a>
    ·   
    <a href="https://github.com/rohankishore/Aura-Text/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">Запросить функцию</a>
    
  *Aura Text также портируется на macOS пользователем [matthewyang204](https://github.com/matthewyang204). Посмотрите репозиторий [здесь](https://github.com/matthewyang204/Aura-Text-Mac)*
  
  </p>
</div>    
<br>
<hr>
<!-- ОГЛАВЛЕНИЕ -->
<details>
  <summary>Оглавление</summary>
  <ol>
    <li>
      <a href="#-о-проекте">О проекте</a>
    </li>
    <li>
      <a href="#-начало-работы">Начало работы</a>
      <ul>
        <li><a href="#требования">Требования</a></li>
        <li><a href="#установка">Установка</a></li>
      </ul>
    </li>
    <li><a href="#разработка">Разработка</a></li>
    <li><a href="#дорожная-карта">Дорожная карта</a></li>
    <li><a href="#-вклад">Вклад</a></li>
    <li><a href="#-лицензия">Лицензия</a></li>
    <li><a href="#-контакт">Контакт</a></li>
  </ol>
</details>
<!-- ПЕРЕКЛЮЧАТЕЛЬ ЯЗЫКА -->
<details>
  <summary>Просмотреть README на:</summary>
  <ol>
    <li>    
      <a href="README_HN.md">हिन्दी 🇮🇳</a>
    </li>
    <li>
      <a href="README_DE.md">Deutsch</a>
    </li>
    <li><a href="README_ES.md">Español</a></li>
    <li><a href="README_TA.md">தமிழ் 🇮🇳</a></li>
    <li><a href="README_FR.md">Français</a></li>
    <li><a href="README_JA.md">日本語</a></li>
    <li><a href="README_PT.md">Português</a></li>
    <li><a><strong>Русский</strong></a></li>
    <li><a href="ZH-CN/README_ZH-CN.md">简体中文</a></li>
  </ol>
</details>
<br>
<hr>
<!-- О ПРОЕКТЕ -->
## 📖 О проекте

<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/17399995-7032-4d90-957e-5cef278ceb6e" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/7eb477ed-1469-4303-bce2-8124efcd8114" />
<img width="1920" height="1100" alt="image" src="https://github.com/user-attachments/assets/c65eace4-8cc5-4390-bc9c-97d17c31c17c" />

Aura Text — это отличный текстовый/кодовый редактор, предлагающий широкий спектр необходимых инструментов. Созданный с использованием PyQt6 и Python, он использует мощь и гибкость этих технологий.
С Aura Text пользователи получают доступ к универсальной и мощной среде редактирования. Будь то небольшой скрипт или сложный проект, Aura Text оснащает вас всеми необходимыми функциями для оптимизации рабочего процесса. От подсветки синтаксиса и автодополнения кода до умных отступов и продвинутого терминала, Aura Text обеспечивает эффективный и приятный опыт кодирования при минимальной нагрузке на ваш ПК.

<br>

***Основные особенности Aura Text:***
- Редактирование файлов
- Поддержка до 30 языков
- Автодополнение
- Линтинг кода для Python (БЕТА)
- Git Clone, Commit и Push с интерактивным ребейсом и графами
- Палитра команд для быстрого выполнения задач
- Пользовательские строки заголовка
- Редактор Markdown с разделённой панелью
- Терминал с историей
- Консоль Python
- Поддержка плагинов
- Расширенная тематизация, включая поддержку Material Theming
- Чрезвычайно настраиваемый
  
<!-- НАЧАЛО РАБОТЫ -->
## 🏃 Начало работы

Давайте настроим Aura Text на вашем ПК!

### Требования
- Windows 10 x64 или новее
- Python 3.9 или новее
- Установка Python bootstrap с pip
- (Рекомендуется) Новый venv, созданный с помощью `python -m venv venv` и активированный с помощью `venv\Scripts\activate`
- Содержимое `requirements.txt`, установленное через `pip install -r requirements.txt`
- (При создании установщика) Inno Setup 6.4.3 или новее
  
### Установка

Вы можете загрузить готовый установщик из раздела Releases или собрать его самостоятельно.

#### Создание установщика

1. Клонируйте репозиторий или загрузите архив
2. Установите все требования
3. `python build.py` для компиляции программы
4. Откройте скрипт Inno Setup `.iss` и скомпилируйте через Ctrl+F9 или `Build > Compile` — установщик находится в папке `Output`

##### Использование установщика

Просто запустите файл `.exe`.

### Тестирование

Для тех, кто хочет запустить без установки в целях тестирования.
Используйте `pythonw main.py` для запуска без логов в терминале, или `python main.py` для отладки.

<br>

## 🧑🏻‍💻 Разработка 

![Alt](https://repobeats.axiom.co/api/embed/c478f91eea3690c7415f891646a2a15a62b4fb20.svg "Repobeats analytics image")
<br>

## 🛣️ Дорожная карта

- <strike> Создать строку состояния внизу с функциями, похожими на PyCharm или другие IDE </strike>
- <strike> Пользовательская тематизация </strike>
- <strike> Эмуляция клавиш </strike>
- <strike> Разделённое редактирование </strike>
- Менеджер проектов
- <strike> Линтинг кода Python </strike>
<b> и многое, многое другое... </b>

<!-- ВКЛАД -->
## 🛂 Вклад

Вклад — это то, что делает сообщество открытого исходного кода таким удивительным местом для обучения, вдохновения и творчества. Любой ваш вклад **очень ценится**.
Если у вас есть предложение, которое улучшит это, пожалуйста, сделайте fork репозитория и создайте pull request. Вы также можете просто открыть issue с тегом «enhancement».
Не забудьте поставить звезду проекту! Спасибо ещё раз!

1. Сделайте fork проекта
2. Создайте ветку функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

### Участники
<a href="https://github.com/rohankishore/Aura-Text/graphs/contributors">
  <img class="dark-light" src="https://contrib.rocks/image?repo=rohankishore/Aura-Text&anon=0&columns=25&max=100&r=true" />
</a>

<br>

<!-- ЛИЦЕНЗИЯ -->
## 🪪 Лицензия

Распространяется под лицензией MIT. Дополнительную информацию см. в `LICENSE.txt`.

## Спонсорство GitAds
[![Sponsored by GitAds](https://gitads.dev/v1/ad-serve?source=rohankishore/aura-text@github)](https://gitads.dev/v1/ad-track?source=rohankishore/aura-text@github)
