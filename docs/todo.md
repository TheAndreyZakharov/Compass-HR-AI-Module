# docs/todo.md — COMPASS-HR-AI-Module 
Репозиторий: `/Users/andrey/Documents/projects/Compass-HR-AI-Module/`  
Цель: реализовать полноценный AI-модуль внутри ERPNext+Frappe HRMS локально, без платных подписок.

---

## 0) Принципы проекта (фиксируются до начала)
- [ ] Разработка ведётся локально, запуск портала (Frappe/ERPNext/HRMS) — в Docker.
- [ ] ML-часть (ETL, обучение, инференс, FastAPI) — на одном Python (одна версия + одно окружение).
- [ ] Один репозиторий, структура создаётся поэтапно (без лишних папок заранее).
- [ ] Источники данных:
  - карьерные траектории РФ (Zenodo),
  - hh.ru API (вакансии/зарплаты/требования),
  - Stepik API (каталог курсов),
  - локальные резюме (PDF/DOCX/TXT) — опционально, но планируется.
- [ ] Важные требования:
  - рекомендации должны быть объяснимыми (reason codes / примеры),
  - сбор/кэширование данных должен соблюдать rate-limit API,
  - воспроизводимость (фикс версий, lockfile, скрипты запуска).

---

<br>
<br>
<br>
<br>
<br> 
<br>
<br>
<br>
<br>
<br> 


## 1) Подготовка Python

- [x] Удалены все ненужные версии и окружения Python
- [x] Установлен Python 3.11.14

---

## 2) Базовый dev-стек (VS Code + Docker + git)

- [x] Установлен Xcode Command Line Tools
- [x] Установлен Homebrew
- [x] Установлен Docker Desktop (Apple Silicon)
- [x] VS Code Расширения:
- [x] Python (ms-python.python)
- [x] Jupyter (ms-toolsai.jupyter)
- [x] Docker (ms-azuretools.vscode-docker)
- [x] Dev Containers (ms-vscode-remote.remote-containers)
- [x] YAML (redhat.vscode-yaml)
- [x] GitHub Markdown Preview, Markdown Preview Github Styling
- [x] Ruff (charliermarsh.ruff)
- [x] и тд

---

## 3) Инициализация репозитория

- [x] Создан корень проекта
- [x] Инициализирован git:
- [x] Создан `README.md` (минимум)
- [x] Создан `docs/` c отчетами, планом и тд
- [x] Создан `.gitignore` (минимум):


---

## 4) Портал: ERPNext + Frappe HRMS в Docker (локально)

- [x] Создана папка portal
- [x] Скачан frappe_docker - склонирован репозиторий
- [x] Запуск
- [x] Тест портала
- [x] Созданы скрипты
- [x] Доустановлен hrm + корректная переустановка остального
- [x] Корректировка скриптов
- [x] Первичная настройка портала
- [x] Salary Component - basic 
- [x] Salary Structure - RUB Monthly (Base)
- [x] Payroll Period - Period (Base)
<details>
  <summary>Про csv</summary>
  01_departments.csv
  Document Type: Department
  Import Type: Insert New Records
  Загружаешь файл → импорт

  02_designations.csv
  Document Type: Designation
  Import Type: Insert New Records

  03_employee_grades.csv
  Document Type: Employee Grade
  Import Type: Insert New Records

  04_employment_types.csv
  Document Type: Employment Type
  Import Type: Insert New Records

  05_employees.csv
  Document Type: Employee
  Import Type: Insert New Records

  06_salary_structure_assignments.csv
  Document Type: Salary Structure Assignment
  Import Type: Insert New Records

</details>

- [x] Создана тестовая структура компании
- [x] hrms и frappe docker в сабмодулях


---

## 5) Кастомизация портала под COMPASS-HR (DocTypes + UI + права)

- [x] Создано Frappe приложение `compass_hr_ai` и добавлено в репозиторий (`portal/custom_app/compass_hr_ai`)
- [x] Подключён bind mount приложения в Docker (`pwd.yml`) для сервисов backend/configurator/queue-long/queue-short/scheduler
- [x] Приложение установлено на сайт (`bench --site frontend install-app compass_hr_ai`) + выполнены миграции
- [x] Включён `developer_mode` (чтобы изменения сохранялись в код приложения)
- [x] Создан Workspace **COMPASS-HR** (отдельная вкладка модуля слева)
- [x] Создан DocType **Compass Employment History** (история ролей/переводов внутри компании)
- [x] Созданы DocTypes модуля (все основные + child tables):  
      Compass Skill, Compass Role Profile, Compass Employee Skill Profile, Compass Career Prediction, Compass Course,  
      Compass Learning Recommendation, Compass Team Plan, Compass Resume + все необходимые child table DocTypes
- [x] Настроены роли модуля: `Compass HR Admin`, `Compass Manager`, `Compass Employee`
- [x] Настроены базовые permissions для DocTypes модуля (admin полный доступ, manager ограниченный, employee — минимальный/по owner где применимо)
- [x] Добавлены UI-кнопки-заглушки в Employee: **Generate Career Plan**, **Refresh Skills from Resume**
- [x] Добавлена UI-кнопка-заглушка в **Compass Team Plan**: **Compute Team Plan**
- [x] Workspace **COMPASS-HR** наполнен секциями/shortcuts на ключевые DocTypes (вкладка больше не пустая)
- [x] Зафиксированы fixtures (Roles + Workspace) и экспортированы в репозиторий (`bench export-fixtures`)
- [x] Подготовлен и проверен импорт демо-seed `seed/07_compass_employment_history.csv` для **Compass Employment History**

---

## 6) ML-часть: структура папок и единое окружение Python (поэтапно)

- [x] Создана папка `ml/` в репозитории
- [x] Создано и используется единое виртуальное окружение `ml/.venv` (Python 3.11.x)
- [x] Обновлены базовые инструменты окружения (`pip`, `setuptools`, `wheel`)
- [x] Создан и зафиксирован `ml/requirements.txt` (базовый набор зависимостей для ETL/ноутбуков/утилит)
- [x] Установлены зависимости из `ml/requirements.txt`
- [x] Зарегистрирован Jupyter kernel `compass-hr` (display name: **Python (compass-hr)**)
- [x] Создан минимальный каркас ML-проекта (`ml/src/compass_hr_ai/__init__.py`, `ml/notebooks/`)
- [x] Добавлен `ml/pyproject.toml` (единые настройки ruff/black/mypy)
- [x] Добавлен smoke-test модуль и проверен запуск (`python -m compass_hr_ai.smoke`)
- [x] VS Code настроен на интерпретатор `ml/.venv/bin/python` и kernel **Python (compass-hr)**
- [x] `ml/.venv` исключён из git (не попадает в коммиты)

---

## 7) Данные: структура и скачивание источников (по мере надобности)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - данные пользователя не тащить в репозиторий; модуль должен работать на их данных (через чтение HRMS)
> - демо-данные держать отдельно и опционально (seed), чтобы “просто потыкаться” было легко
> - кэш внешних API (hh/stepik) хранить локально (disk/volume), никогда не коммитить

### 7.1. Создание структуры `data/` (только когда реально начинается работа с данными)
- [ ] Создать (в корне репозитория):
  <details>
    <summary>Команды</summary>

    cd /Users/andrey/Documents/projects/Compass-HR-AI-Module
    mkdir -p data/raw data/interim data/processed data/cache

  </details>
- [ ] Добавить `data/` в `.gitignore` уже сделано (не коммитить большие данные).

### 7.2. Карьерные траектории РФ (Zenodo)
- [ ] Скачать датасет вручную (из браузера) и положить в `data/raw/rostrud/`:
  <details>
    <summary>Команды</summary>

    mkdir -p data/raw/rostrud

  </details>
  - Страница набора: https://zenodo.org/records/12727876
  - Скачать нужные архивы (например workexp / edu / codebook) и поместить туда.

- [ ] Распаковать (пример):
  <details>
    <summary>Команды</summary>

    cd data/raw/rostrud
    # пример: unzip dataset1.workexp.csv.zip
    unzip -n "*.zip"

  </details>

### 7.3. hh.ru API (вакансии/зарплаты)
- [ ] Создать папку кэша:
  <details>
    <summary>Команды</summary>

    mkdir -p data/cache/hh

  </details>
- [ ] Принцип: все ответы API сохраняются на диск, повторные запросы — только при явной команде “refresh”.

### 7.4. Stepik API (курсы)
- [ ] Создать папку кэша:
  <details>
    <summary>Команды</summary>

    mkdir -p data/cache/stepik

  </details>

---

## 8) ETL-пайплайны (скрипты) — создание папок и файлов строго по этапу

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - ETL должен быть воспроизводимым (одна команда → один результат), чтобы можно было собрать демо-артефакты
> - результаты ETL для демо не хранить в git; публиковать как “demo data pack” отдельно (архив/release) или генерировать локально
> - предусмотреть режим “demo small”: маленький срез данных для быстрого старта у пользователей

### 8.1. Создать каркас ETL
- [ ] Создать папки:
  <details>
    <summary>Команды</summary>

    cd /Users/andrey/Documents/projects/Compass-HR-AI-Module/ml
    mkdir -p src/compass_hr_ai/{etl,schemas,utils} notebooks
    touch src/compass_hr_ai/__init__.py

  </details>

### 8.2. ETL: карьерные траектории (role normalization + sequences)
- [ ] Создать файл:
  - `ml/src/compass_hr_ai/etl/rostrud_ingest.py`
- [ ] Реализовать шаги:
  - [ ] чтение `workexp.csv` и ключевых полей,
  - [ ] нормализация названий должностей (lowercase, очистка, словарь синонимов),
  - [ ] построение справочника ролей `role_id`,
  - [ ] формирование последовательностей (кандидат → упорядоченный список ролей со временем),
  - [ ] сохранение в `data/processed/trajectories.parquet`.

### 8.3. ETL: hh (vacancies ingest + parsing)
- [ ] Создать файлы:
  - `ml/src/compass_hr_ai/etl/hh_fetch.py`
  - `ml/src/compass_hr_ai/etl/hh_parse.py`
- [ ] Реализовать:
  - [ ] запрос вакансий по роли/региону/опыту,
  - [ ] кэширование JSON в `data/cache/hh/`,
  - [ ] парсинг зарплат (from/to/currency), признаков, текста требований,
  - [ ] сохранение в `data/processed/hh_vacancies.parquet`.

### 8.4. ETL: Stepik (course catalog ingest)
- [ ] Создать файлы:
  - `ml/src/compass_hr_ai/etl/stepik_fetch.py`
  - `ml/src/compass_hr_ai/etl/stepik_parse.py`
- [ ] Реализовать:
  - [ ] сбор курсов по ключевым словам/тегам,
  - [ ] кэширование JSON в `data/cache/stepik/`,
  - [ ] сохранение `data/processed/courses.parquet`.

---

## 9) NLP слой: эмбеддинги + извлечение навыков (сразу “нормальная версия”)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - модель эмбеддингов и все индексы должны подниматься одинаково (фикс версии, фикс конфиги)
> - хранение эмбеддингов: отдельный vector store (например Qdrant) в Docker для демо
> - снапшоты/дампы индекса — опциональные артефакты (demo pack), не хранить в git

### 9.1. Добавить зависимости (когда начинается NLP)
- [ ] В `ml/requirements.txt` добавить и установить:
  <details>
    <summary>Зависимости</summary>

    torch
    transformers
    sentence-transformers
    spacy
    natasha
    yake
    rapidfuzz

  </details>
- [ ] Установить:
  <details>
    <summary>Команды</summary>

    cd ml
    source .venv/bin/activate
    pip install -r requirements.txt

  </details>

### 9.2. Векторное хранилище (рекомендуется)
Вариант A (проще локально): Qdrant в Docker.
- [ ] Создать папку и compose:
  <details>
    <summary>Команды</summary>

    cd /Users/andrey/Documents/projects/Compass-HR-AI-Module
    mkdir -p infra/qdrant
    cat > infra/qdrant/docker-compose.yml << 'EOF'
    services:
      qdrant:
        image: qdrant/qdrant:latest
        ports:
          - "6333:6333"
        volumes:
          - ./storage:/qdrant/storage
    EOF

  </details>
- [ ] Запустить:
  <details>
    <summary>Команды</summary>

    cd infra/qdrant
    docker compose up -d

  </details>

### 9.3. Эмбеддинги текстов (вакансии/курсы/резюме)
- [ ] Создать модуль:
  - `ml/src/compass_hr_ai/nlp/embeddings.py`
- [ ] Реализовать:
  - [ ] выбор модели эмбеддингов (рус/мультиязычная),
  - [ ] батчевую генерацию эмбеддингов для:
    - вакансий (hh),
    - курсов (Stepik),
    - профилей ролей,
    - текстов резюме,
  - [ ] сохранение эмбеддингов в Qdrant (id → vector).

### 9.4. Извлечение навыков (NER/Keyphrase + нормализация)
- [ ] Создать модуль:
  - `ml/src/compass_hr_ai/nlp/skills_extract.py`
- [ ] Реализовать:
  - [ ] keyphrase extraction (YAKE/KeyBERT),
  - [ ] NER/морфология (Natasha) для русских текстов,
  - [ ] нормализация (rapidfuzz + aliases + словарь),
  - [ ] маппинг в `Skill` (skill_id).

**Целевые ориентиры качества извлечения навыков:**
- [ ] ручная разметка 100 текстов (вакансии/резюме),
- [ ] precision >= 0.75, recall >= 0.55 (ориентиры; зависят от домена),
- [ ] доля “непопавших в словарь” навыков <= 20% после нормализации.

---

## 10) Модель карьерных траекторий (sequence model)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - обученные веса и маппинги ролей хранить как “model pack” (архив) отдельно от git
> - обеспечить “demo weights” маленького размера, чтобы пользователь мог быстро запустить и увидеть результат
> - обеспечить совместимость версий: весам соответствует конкретная версия кода и схемы features

### 10.1. Добавить зависимости (когда начинается обучение)
- [ ] В `ml/requirements.txt` добавить:
  <details>
    <summary>Зависимости</summary>

    pytorch-lightning
    torchmetrics

  </details>
- [ ] Установить:
  <details>
    <summary>Команды</summary>

    cd ml
    source .venv/bin/activate
    pip install -r requirements.txt

  </details>

### 10.2. Подготовка датасета под sequence model
- [ ] Создать модуль:
  - `ml/src/compass_hr_ai/models/career_dataset.py`
- [ ] Реализовать:
  - [ ] токенизация роли (role_id),
  - [ ] формирование последовательностей фиксированной длины,
  - [ ] train/val/test split по времени,
  - [ ] сохранение метаданных (vocab, mapping role_id).

### 10.3. Обучение модели (Transformer/GRU/LSTM)
- [ ] Создать:
  - `ml/src/compass_hr_ai/models/career_model.py`
  - `ml/src/compass_hr_ai/train/train_career.py`
- [ ] Обучить и сохранить артефакты в `models/career/`.

**Целевые метрики для next-role prediction (ориентиры):**
- [ ] Hit@5: >= 0.30–0.45 (зависит от степени нормализации ролей и числа классов),
- [ ] MRR: >= 0.12–0.25,
- [ ] nDCG@10: >= 0.25–0.45,
- [ ] стабильность по подгруппам (IT роли отдельно): не хуже среднего более чем на 20%.

### 10.4. Объяснимость (обязательная часть)
- [ ] Реализовать reason-codes:
  - [ ] “похожие траектории” (nearest neighbors по embedding траектории),
  - [ ] “частые переходы” из графа переходов (статистика),
  - [ ] “нехватающие навыки” (skill-gap) как объяснение.

---

## 11) Модель зарплаты / стоимости найма (CatBoost)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - внешние запросы (hh) должны быть кэшируемыми и управляемыми (чтобы пользователь не словил лимиты)
> - для демо допустим “замороженный” датасет вакансий (demo pack), чтобы без API ключей/лимитов работало

### 11.1. Зависимости
- [ ] Добавить:
  <details>
    <summary>Зависимости</summary>

    catboost

  </details>
- [ ] Установить:
  <details>
    <summary>Команды</summary>

    cd ml
    source .venv/bin/activate
    pip install -r requirements.txt

  </details>

### 11.2. Датасет зарплат
- [ ] Создать:
  - `ml/src/compass_hr_ai/models/salary_dataset.py`
- [ ] Реализовать признаки:
  - регион, роль, опыт, формат занятости,
  - текстовые фичи (мешок навыков/топ-N skills),
  - агрегаты по работодателю (если доступны публично).

### 11.3. Обучение CatBoost
- [ ] Создать:
  - `ml/src/compass_hr_ai/models/salary_model.py`
  - `ml/src/compass_hr_ai/train/train_salary.py`
- [ ] Сохранить артефакты в `models/salary/`.

**Целевые метрики (ориентиры):**
- [ ] MAE по salary_mid: <= 15–25% от медианы по выбранному сегменту,
- [ ] контроль ошибок по регионам: не хуже среднего более чем на 30%,
- [ ] адекватные диапазоны (квантили/интервалы) для TeamPlan.

---

## 12) Рекомендательная логика: сотрудник → роль → курсы

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - все рекомендации должны быть объяснимыми (почему этот курс/роль)
> - результаты сохранять в DocTypes модуля, чтобы можно было смотреть историю и откатываться
> - учитывать “изоляцию”: профиль сотрудника для ML берётся из снимка/копии, а не правит HRMS данные

### 12.1. Skill-gap
- [ ] Реализовать модуль:
  - `ml/src/compass_hr_ai/reco/skill_gap.py`
- [ ] Вход:
  - EmployeeSkillProfile + RoleProfile
- [ ] Выход:
  - список (skill_id, delta/priority)

### 12.2. Рекомендация курсов
- [ ] Реализовать:
  - `ml/src/compass_hr_ai/reco/course_ranker.py`
- [ ] Использовать:
  - семантическую близость (эмбеддинги),
  - покрытие “gap skills”,
  - фильтры (язык, длительность, уровень).

**Ориентиры качества (offline):**
- [ ] валидация на 30–50 кейсах: не менее 1–3 релевантных курсов в топ-5.

---

## 13) Планирование нового отдела (TeamPlan): внутренние / upskill / внешний найм

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - TeamPlan должен работать как отдельный “песочничный” объект внутри модуля (не создавать реальные Department/Employee изменения)
> - результаты TeamPlan сохранять отдельно (в DocTypes модуля), чтобы модуль был “надстройкой”, а не “редактором базы”
> - предусмотреть демо-режим: если внутренних данных мало, уметь работать на демо seed

### 13.1. Логика TeamPlan
- [ ] Реализовать:
  - `ml/src/compass_hr_ai/team/team_planner.py`
- [ ] Вход:
  - роли, количество, приоритеты, сроки,
  - список сотрудников + их текущие роли/навыки,
  - бюджетные ограничения (опционально).
- [ ] Выход:
  - internal assignments,
  - upskill plans (gap+courses+ETA),
  - external hiring (salary range + key skills + hh query).

### 13.2. Оптимизация назначения
- [ ] Реализовать простую оптимизацию:
  - штраф за “забрать ключевого сотрудника”,
  - минимизация внешнего бюджета,
  - минимизация суммарного skill-gap.

---

## 14) FastAPI ML-service (инференс + интеграция)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - ML-service должен иметь docker-режим (для демо “в один клик”) и python-режим (для разработки)
> - фиксировать контракт API (версии) и валидировать схемы вход/выход (pydantic)
> - добавить конфиг “где лежат модели” и “где лежат индексы” (через env)
> - добавить скрипт скачивания model pack (если модели не в репо)


> ⚠️ Для реализации модом надо в этом пункте сделать:
> - ML должен быть упакован как сервис (FastAPI) с предсказуемым запуском (docker compose или python run)
> - веса/индексы/эмбеддинги не хранить в git; доставлять через “model pack” (архив) или release assets
> - предусмотреть два режима: demo (маленькие артефакты) и full (большие артефакты)


### 14.1. Создать папку сервиса и файлы
- [ ] Создать:
  <details>
    <summary>Команды</summary>

    cd /Users/andrey/Documents/projects/Compass-HR-AI-Module/ml
    mkdir -p service
    touch service/main.py

  </details>
- [ ] Добавить зависимости:
  <details>
    <summary>Зависимости</summary>

    fastapi
    uvicorn[standard]

  </details>
- [ ] Установить:
  <details>
    <summary>Команды</summary>

    pip install -r requirements.txt

  </details>

### 14.2. Реализовать эндпоинты
- [ ] `GET /health`
- [ ] `POST /career/predict-next`
- [ ] `POST /skills/extract`
- [ ] `POST /learning/recommend`
- [ ] `POST /team/plan`
- [ ] `GET /market/salary-range?role=&region=&level=`

### 14.3. Запуск сервиса локально
- [ ] Запуск:
  <details>
    <summary>Команды</summary>

    cd ml
    source .venv/bin/activate
    uvicorn service.main:app --host 0.0.0.0 --port 9000 --reload

  </details>
- [ ] Проверка:
  <details>
    <summary>Команды</summary>

    curl http://localhost:9000/health

  </details>

---

## 15) Интеграция портала (Frappe) с ML-service

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - интеграцию реализовать внутри Frappe app (server methods + UI), чтобы установка была “как мод”
> - хранить результаты инференса в DocTypes модуля и показывать их в отдельном workspace “COMPASS-HR”
> - обеспечить два режима установки:
>   - режим A: установка app в существующий ERPNext/HRMS (без демо-данных)
>   - режим B: demo stack (docker compose), чтобы “просто потыкаться”

### 15.1. Конфиг адресов и секретов
- [ ] В корне репозитория создать `.env` (не коммитить):
  <details>
    <summary>Пример</summary>

    ML_SERVICE_URL=http://host.docker.internal:9000

  </details>
  > В Docker на macOS `host.docker.internal` обычно указывает на хост-машину.

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - для demo stack использовать сетевое имя сервиса внутри docker network (например `http://ml:9000`)
> - для режима установки в чужую систему оставить возможность `host.docker.internal` или внешний URL
> - хранить конфиги в env, не в коде

### 15.2. Вызовы из Frappe по кнопке
- [ ] Реализовать серверные методы (Frappe whitelisted methods):
  - `generate_career_plan(employee_id)`
  - `compute_team_plan(team_plan_id)`
  - `refresh_skills_from_resume(employee_id)`

- [ ] Реализовать запись результатов в DocTypes:
  - CareerPrediction
  - LearningRecommendation
  - TeamPlan (результаты)
  - EmployeeSkillProfile

> ⚠️ Для реализации “изоляции и вакуума” надо в этом пункте сделать:
> - server methods должны брать входные данные из снимков (read-only копий) и/или из HRMS только на чтение
> - любые “обновления” должны быть обновлениями снимков и результатов модуля, а не изменениями HRMS карточек

### 15.2.1. Строгие правила видимости (обязательно)
- [ ] Реализовать row-level access:
  - [ ] Compass Employee видит только записи, где employee == текущий пользователь (CareerPrediction / LearningRecommendation / Resume / EmployeeSkillProfile)
  - [ ] Compass Manager видит только сотрудников своего отдела / подчинённых (TeamPlan + рекомендации по своим сотрудникам)
  - [ ] Compass HR Admin видит всё
- [ ] Реализация не через “галочки”, а через:
  - [ ] permission_query_conditions (Python)
  - [ ] и/или проверки в whitelisted methods + server-side validate
- [ ] Документы должны иметь явную привязку к Employee (поле employee) и правильный owner/created_by (если нужно)
- [ ] Добавить mapping User -> Employee (как определяем “чей employee”)
  - [ ] использовать стандартное поле в Employee (User ID) или сделать своё связующее поле/таблицу
  - [ ] (то есть этот пункт для того чтобы конкретный пользователь видел только своё)

### 15.3. Фоновые задачи (scheduler)
- [ ] Добавить jobs:
  - nightly: обновить каталог курсов,
  - nightly: обновить рынок (hh) по ключевым ролям,
  - weekly: переиндексация эмбеддингов (если нужно).

> ⚠️ Для реализации “изоляции и вакуума” надо в этом пункте сделать:
> - nightly job: обновлять снимки сотрудников (копии профилей) и пересчитывать рекомендации без изменения HRMS
> - добавить ручные кнопки “Refresh snapshot / Recompute” для контроля
> - хранить историю пересчётов (timestamped results) в DocTypes модуля

---

## 16) Резюме (локальные файлы): извлечение текста и навыков

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - загрузки резюме хранить как attachments и метаданные в DocTypes модуля
> - не менять HRMS записи, только обогащать профиль модуля (EmployeeSkillProfile / snapshots)

### 16.1. Зависимости для парсинга
- [ ] Добавить:
  <details>
    <summary>Зависимости</summary>

    pypdf
    python-docx

  </details>
- [ ] Установить:
  <details>
    <summary>Команды</summary>

    cd ml
    source .venv/bin/activate
    pip install -r requirements.txt

  </details>

### 16.2. Пайплайн резюме
- [ ] Реализовать:
  - `ml/src/compass_hr_ai/nlp/resume_parse.py`
- [ ] Логика:
  - PDF → pypdf → text
  - DOCX → python-docx → text
  - TXT → read
  - text → skills_extract → Skill IDs
  - обновление EmployeeSkillProfile

---

## 17) Тестирование и контроль качества

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - добавить “smoke demo”: один скрипт поднимает demo stack и проверяет ключевые URL/эндпоинты
> - тестировать миграции DocTypes модуля (установка/обновление/удаление)
> - тестировать режим A (установка в существующий сайт) отдельно от режима B (demo stack)

### 17.1. Unit tests (ML)
- [ ] Создать:
  <details>
    <summary>Команды</summary>

    cd ml
    mkdir -p tests

  </details>
- [ ] Покрыть тестами:
  - нормализацию должностей,
  - разбор зарплат hh,
  - извлечение навыков,
  - skill-gap,
  - сериализацию ответов API.

### 17.2. Интеграционные тесты (портал ↔ ML)
- [ ] Проверки:
  - кнопка в карточке сотрудника → создаёт CareerPrediction + LearningRecommendation,
  - TeamPlan → создаёт результаты internal/upskill/external,
  - Resume upload → обновляет EmployeeSkillProfile.

### 17.3. Smoke tests (end-to-end)
- [ ] Подготовить 3 демонстрационных сценария:
  1) сотрудник → следующая роль → курсы,
  2) сотрудник с резюме → обновление навыков → обновление рекомендаций,
  3) новый отдел → план закрытия ролей + бюджет hh.

---

## 18) Документация (минимум для готового продукта)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - описать два режима установки: A (install app) и B (demo stack)
> - описать что модуль не изменяет HRMS/ERPNext данные (работает поверх/через копии)
> - описать где взять model pack и как его положить в нужную папку

- [ ] `docs/architecture.md`:
  - компоненты, потоки данных, форматы идентификаторов
- [ ] `docs/api_contract.md`:
  - схемы запросов/ответов FastAPI
- [ ] `docs/data_sources.md`:
  - ссылки на Zenodo/hh/Stepik, правила кэширования, rate limits
- [ ] `docs/model_cards.md`:
  - описание моделей, метрики, ограничения, риски bias
- [ ] `docs/demo_scenarios.md`:
  - пошагово как воспроизвести 3 ключевых кейса

> ⚠️ Для реализации “демо без данных в репо” надо в этом пункте сделать:
> - описать опциональный seed: как загрузить демо-данные (и как их удалить)
> - описать что большие датасеты и кэши не входят в репо и должны скачиваться/генерироваться локально

---

## 19) Контрольный список “готово”
- [ ] Портал (ERPNext+HRMS) стартует локально в Docker и доступен в браузере.
- [ ] DocTypes созданы, права настроены.
- [ ] ML-service стартует на `localhost:9000`, отвечает `/health`.
- [ ] Данные (Zenodo/hh/Stepik) скачаны/собраны и сохранены локально (cache + processed parquet).
- [ ] Модель траекторий обучена, выдаёт top-N следующих ролей + explanation_json.
- [ ] NLP слой извлекает навыки и строит эмбеддинги, курсы подбираются семантически.
- [ ] Salary model выдаёт вилку бюджета по роли/региону.
- [ ] TeamPlan выдаёт: internal / upskill / external + бюджет.
- [ ] Интеграция по кнопкам в портале работает.
- [ ] 3 демо-сценария воспроизводимы.
- [ ] Документация заполнена.

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - подтвердить два режима:
>   - режим A: модуль устанавливается в существующий ERPNext/HRMS сайт одной командой install-app и работает на их данных
>   - режим B: demo stack поднимается одной командой (scripts/compose) и позволяет “потыкаться”
> - подтвердить, что удаление модуля не ломает основной портал и не удаляет HRMS данные

---

## 20) Упаковка “как мод” и релиз (обязательный финальный этап)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - сделать единый механизм версионирования: версия модуля + версия model pack + совместимость
> - вынести большие артефакты (модели/индексы/демо-данные) из git и публиковать отдельно (архив/release assets)
> - добавить скрипты “скачать и развернуть демо-артефакты”

### 20.1. Два режима установки (A / B)
- [ ] Режим A: установка модуля в существующий ERPNext/HRMS (без демо-данных)
  - [ ] описать шаги: поставить Frappe app, выполнить install-app, migrate, настроить ML_SERVICE_URL
- [ ] Режим B: демо-режим (docker stack) “в один клик”
  - [ ] поднятие портала + ml + (qdrant)
  - [ ] опционально: загрузить демо-данные и демо model pack

### 20.2. Скрипты релиза
- [ ] Добавить скрипты:
  - [ ] scripts/demo_up.sh (поднять демо стек)
  - [ ] scripts/demo_seed.sh (опционально загрузить демо данные)
  - [ ] scripts/ml_download_models.sh (скачать model pack)
  - [ ] scripts/smoke_test.sh (проверить, что demo stack работает)

### 20.3. Безопасность данных и ограничения
- [ ] Зафиксировать правило:
  - [ ] модуль не изменяет HRMS/ERPNext данные, работает через read-only чтение и свои DocTypes/снимки
  - [ ] любые изменения делаются только в DocTypes модуля
- [ ] Добавить предупреждения:
  - [ ] не запускать destructive команды (например удаление volume) без осознания последствий
  - [ ] демо-данные опциональны и не входят в репозиторий

---

## 21) README (финал, писать в самом конце)

> ⚠️ Для реализации модом надо в этом пункте сделать:
> - README должен описывать два пути:
>   - “Install as app” (для тех у кого уже есть ERPNext/HRMS)
>   - “Demo in one click” (для тех кто хочет потыкаться)
> - README должен объяснять:
>   - какие данные модуль читает из HRMS (только чтение)
>   - какие данные модуль хранит у себя (DocTypes модуля, снимки, результаты ML)
>   - где взять model pack и как его подключить
>   - как включить/выключить демо-данные
>   - как запустить ML-service (docker/python)
>   - как устроены версии и совместимость (код/модели/индексы)

---

Источники по ссылкам/командам: frappe_docker quick-start и ARM64 инструкции ; Zenodo датасет ; hh.ru API и документация ; Stepik API docs 