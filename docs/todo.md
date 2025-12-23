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
> Цель: получить работающий портал в браузере (localhost), чтобы сразу создавать HR-сущности и UI.

- [x] Создана папка portal
- [x] Скачан frappe_docker - склонирован репозиторий
- [x] Запуск
- [x] Тест портала
- [x] Созданы скрипты


### 4.5. Первичная настройка портала
- [ ] Зайти в ERPNext/HRMS и проверить:
  - [ ] Employees/Сотрудники доступны
  - [ ] Departments/Отделы доступны
  - [ ] Roles/Permissions работают (создаются роли, назначаются пользователям)
- [ ] Создать тестовую структуру компании:
  - [ ] 3–5 отделов (Development, QA, Product, Data, HR)
  - [ ] 10–20 сотрудников с ролями/грейдами/стеком (пока вручную)

---

## 5) Кастомизация портала под COMPASS-HR (DocTypes + UI + права)
> На этом этапе создаются сущности, в которые ML-сервис будет писать результаты.

### 5.1. Создание собственного приложения (custom app) внутри Frappe
- [ ] Создать папку для кастомного приложения в репозитории:
  ```bash
  cd /Users/andrey/Documents/projects/Compass-HR-AI-Module
  mkdir -p portal/custom_app
  ```
- [ ] Принцип: custom app должен храниться в репозитории и устанавливаться в контейнер (подход зависит от dev-режима Frappe; в дальнейшем выбрать один способ):
  - вариант A: монтирование каталога app внутрь контейнера (удобно для разработки),
  - вариант B: разработка через Dev Containers/внутри контейнера и commit в repo.

> TODO: после того как портал стабильно запустится, выбрать конкретный способ разработки кастомного app (с монтированием кода наружу).

### 5.2. Создание DocTypes (минимальный боевой набор)
- [ ] Создать DocTypes (через UI Frappe или через код app):
  - [ ] `Skill`
  - [ ] `RoleProfile`
  - [ ] `EmployeeSkillProfile`
  - [ ] `CareerPrediction`
  - [ ] `CourseCatalog`
  - [ ] `LearningRecommendation`
  - [ ] `TeamPlan`
  - [ ] `Resume` (attachments + метаданные)

- [ ] Сразу определить поля и связи:
  - [ ] `Skill`: name, category, aliases, source, embedding_id
  - [ ] `RoleProfile`: role_name, level, required_skills(child table: skill, weight, min_level), source
  - [ ] `EmployeeSkillProfile`: employee(link), skills(child: skill, level, evidence, updated_at)
  - [ ] `CareerPrediction`: employee, current_role, predictions(child: target_role, probability, explanation_json, timestamp)
  - [ ] `CourseCatalog`: provider, course_id, title, description, url, skills(child), embedding_id
  - [ ] `LearningRecommendation`: employee, target_role, gap(child: skill, delta), courses(child: course_id, score, why_json, link)
  - [ ] `TeamPlan`: department_name, target_roles(child: role_profile, count, priority, deadline), results (internal/upskill/external + ссылки на рекомендации)
  - [ ] `Resume`: employee, file, extracted_text, extracted_skills(child), parsed_at

### 5.3. Роли и права доступа
- [ ] Настроить роли:
  - [ ] HR Admin — полный доступ
  - [ ] Manager — доступ к TeamPlan и сотрудникам своего отдела
  - [ ] Employee — доступ к собственным рекомендациям (read-only)
- [ ] Проверить, что Employee не видит чужие рекомендации.

### 5.4. UI-элементы (кнопки и формы)
- [ ] В карточке сотрудника добавить кнопки:
  - [ ] **Generate Career Plan**
  - [ ] **Refresh Skills from Resume**
- [ ] В форме TeamPlan добавить кнопку:
  - [ ] **Compute Team Plan**

> На этом этапе кнопки пока могут вызывать “заглушки” (или логировать событие), но интерфейс должен быть готов.

---

## 6) ML-часть: структура папок и единое окружение Python (поэтапно)
### 6.1. Создание папки `ml/` и виртуального окружения
- [ ] Создать папку ML:
  ```bash
  cd /Users/andrey/Documents/projects/Compass-HR-AI-Module
  mkdir -p ml
  ```
- [ ] Создать единственное окружение для проекта:
  ```bash
  cd ml
  python3 -m venv .venv
  source .venv/bin/activate
  python -V
  pip -V
  ```
- [ ] Обновить pip/setuptools/wheel:
  ```bash
  pip install -U pip setuptools wheel
  ```

### 6.2. Базовые зависимости (фиксировать постепенно)
- [ ] Создать `ml/requirements.txt` (первый набор — ETL + ноутбуки + базовые утилиты):
  ```bash
  cat > requirements.txt << 'EOF'
  numpy
  pandas
  pyarrow
  scikit-learn
  tqdm
  matplotlib

  jupyter
  ipykernel

  requests
  httpx
  python-dotenv
  pydantic

  ruff
  black
  mypy
  pytest
  pre-commit
  EOF
  ```
- [ ] Установить:
  ```bash
  pip install -r requirements.txt
  python -m ipykernel install --user --name compass-hr --display-name "Python (compass-hr)"
  ```

### 6.3. Настройка VS Code под окружение
- [ ] В VS Code выбрать интерпретатор: `ml/.venv/bin/python`
- [ ] В ноутбуках выбрать kernel: **Python (compass-hr)**

---

## 7) Данные: структура и скачивание источников (по мере надобности)
### 7.1. Создание структуры `data/` (только когда реально начинается работа с данными)
- [ ] Создать (в корне репозитория):
  ```bash
  cd /Users/andrey/Documents/projects/Compass-HR-AI-Module
  mkdir -p data/raw data/interim data/processed data/cache
  ```
- [ ] Добавить `data/` в `.gitignore` уже сделано (не коммитить большие данные).

### 7.2. Карьерные траектории РФ (Zenodo)
- [ ] Скачать датасет вручную (из браузера) и положить в `data/raw/rostrud/`:
  ```bash
  mkdir -p data/raw/rostrud
  ```
  - Страница набора: https://zenodo.org/records/12727876
  - Скачать нужные архивы (например workexp / edu / codebook) и поместить туда.

- [ ] Распаковать (пример):
  ```bash
  cd data/raw/rostrud
  # пример: unzip dataset1.workexp.csv.zip
  unzip -n "*.zip"
  ```

### 7.3. hh.ru API (вакансии/зарплаты)
- [ ] Создать папку кэша:
  ```bash
  mkdir -p data/cache/hh
  ```
- [ ] Принцип: все ответы API сохраняются на диск, повторные запросы — только при явной команде “refresh”.

### 7.4. Stepik API (курсы)
- [ ] Создать папку кэша:
  ```bash
  mkdir -p data/cache/stepik
  ```

---

## 8) ETL-пайплайны (скрипты) — создание папок и файлов строго по этапу
### 8.1. Создать каркас ETL
- [ ] Создать папки:
  ```bash
  cd /Users/andrey/Documents/projects/Compass-HR-AI-Module/ml
  mkdir -p src/compass_hr_ai/{etl,schemas,utils} notebooks
  touch src/compass_hr_ai/__init__.py
  ```

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
### 9.1. Добавить зависимости (когда начинается NLP)
- [ ] В `ml/requirements.txt` добавить и установить:
  ```txt
  torch
  transformers
  sentence-transformers
  spacy
  natasha
  yake
  rapidfuzz
  ```
- [ ] Установить:
  ```bash
  cd ml
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

### 9.2. Векторное хранилище (рекомендуется)
Вариант A (проще локально): Qdrant в Docker.
- [ ] Создать папку и compose:
  ```bash
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
  ```
- [ ] Запустить:
  ```bash
  cd infra/qdrant
  docker compose up -d
  ```

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
### 10.1. Добавить зависимости (когда начинается обучение)
- [ ] В `ml/requirements.txt` добавить:
  ```txt
  pytorch-lightning
  torchmetrics
  ```
- [ ] Установить:
  ```bash
  cd ml
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

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
### 11.1. Зависимости
- [ ] Добавить:
  ```txt
  catboost
  ```
- [ ] Установить:
  ```bash
  cd ml
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

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
### 14.1. Создать папку сервиса и файлы
- [ ] Создать:
  ```bash
  cd /Users/andrey/Documents/projects/Compass-HR-AI-Module/ml
  mkdir -p service
  touch service/main.py
  ```
- [ ] Добавить зависимости:
  ```txt
  fastapi
  uvicorn[standard]
  ```
- [ ] Установить:
  ```bash
  pip install -r requirements.txt
  ```

### 14.2. Реализовать эндпоинты
- [ ] `GET /health`
- [ ] `POST /career/predict-next`
- [ ] `POST /skills/extract`
- [ ] `POST /learning/recommend`
- [ ] `POST /team/plan`
- [ ] `GET /market/salary-range?role=&region=&level=`

### 14.3. Запуск сервиса локально
- [ ] Запуск:
  ```bash
  cd ml
  source .venv/bin/activate
  uvicorn service.main:app --host 0.0.0.0 --port 9000 --reload
  ```
- [ ] Проверка:
  ```bash
  curl http://localhost:9000/health
  ```

---

## 15) Интеграция портала (Frappe) с ML-service
### 15.1. Конфиг адресов и секретов
- [ ] В корне репозитория создать `.env` (не коммитить):
  ```env
  ML_SERVICE_URL=http://host.docker.internal:9000
  ```
  > В Docker на macOS `host.docker.internal` обычно указывает на хост-машину.

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

### 15.3. Фоновые задачи (scheduler)
- [ ] Добавить jobs:
  - nightly: обновить каталог курсов,
  - nightly: обновить рынок (hh) по ключевым ролям,
  - weekly: переиндексация эмбеддингов (если нужно).

---

## 16) Резюме (локальные файлы): извлечение текста и навыков
### 16.1. Зависимости для парсинга
- [ ] Добавить:
  ```txt
  pypdf
  python-docx
  ```
- [ ] Установить:
  ```bash
  cd ml
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

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
### 17.1. Unit tests (ML)
- [ ] Создать:
  ```bash
  cd ml
  mkdir -p tests
  ```
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

---

Источники по ссылкам/командам: frappe_docker quick-start и ARM64 инструкции ; Zenodo датасет ; hh.ru API и документация ; Stepik API docs 