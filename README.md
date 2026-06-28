# Frappe HR Forge

Frappe HR Forge is a local ERPNext/Frappe HRMS development project prepared for building custom HR modules.

The repository contains a working local portal foundation, a custom Frappe application, HR-focused DocTypes, workspace configuration, role and permission setup, demo seed data, and a Python 3.11 ML/data scaffold for future recommendation, planning and analytics features.

The project started as a prepared base for a larger HR module inside ERPNext and Frappe HRMS. It is not a finished product yet. It is a structured development foundation that can be extended into a full HR planning, career recommendation, skills analysis and team planning module.

## Repository purpose

The purpose of this repository is to provide a local development base for extending ERPNext and Frappe HRMS with custom HR functionality.

Current focus:

- local ERPNext/Frappe HRMS portal in Docker;
- custom Frappe app connected to the portal;
- dedicated HR workspace;
- custom HR DocTypes;
- module roles and permissions;
- demo company structure and seed data;
- Python 3.11 ML environment;
- reproducible ETL pipeline structure;
- cached external data source layout;
- roadmap for future HR recommendations and planning logic.

The repository is intentionally structured as a development foundation. The AI/ML recommendation features are planned and partially scaffolded, but not fully implemented yet.

## Current status

Implemented:

- local project root and git repository;
- basic documentation structure;
- Docker-based ERPNext/Frappe HRMS portal;
- Frappe HRMS installation and initial portal setup;
- salary component, salary structure and payroll period base setup;
- demo company structure;
- custom Frappe app `compass_hr_ai`;
- bind mount of the custom app into the Docker portal stack;
- installation of the app into the Frappe site;
- developer mode;
- dedicated workspace inside the portal;
- custom HR DocTypes;
- child table DocTypes;
- custom roles;
- base permissions;
- UI placeholder buttons in Employee and Team Plan forms;
- fixtures for roles and workspace;
- demo seed CSV for employment history;
- Python 3.11 ML environment;
- `ml/requirements.txt`;
- Jupyter kernel;
- ML package scaffold;
- Ruff/Black/Mypy configuration;
- data folders for raw, interim, processed and cache layers;
- Rostrud/Zenodo data ingestion scaffold;
- hh.ru cached ETL scaffold;
- Stepik cached ETL scaffold;
- demo parquet artifacts generated locally;
- ETL smoke test.

Paused or planned:

- NLP embeddings;
- Qdrant vector store;
- skill extraction;
- career trajectory sequence model;
- salary model;
- course recommendation logic;
- team planning logic;
- FastAPI ML service;
- portal-to-ML integration;
- row-level access logic;
- resume parsing;
- integration tests;
- full documentation set;
- demo stack packaging.

## What is already prepared in Frappe

The custom Frappe application is located in:

    portal/custom_app/compass_hr_ai

The application has been connected to the Docker portal through bind mounts and installed into the Frappe site.

Prepared portal elements include:

- dedicated workspace;
- module roles;
- module permissions;
- custom DocTypes;
- child table DocTypes;
- placeholder UI actions;
- exported fixtures;
- demo employment history seed.

Main custom DocTypes include:

- Compass Employment History;
- Compass Skill;
- Compass Role Profile;
- Compass Employee Skill Profile;
- Compass Career Prediction;
- Compass Course;
- Compass Learning Recommendation;
- Compass Team Plan;
- Compass Resume.

Prepared roles include:

- Compass HR Admin;
- Compass Manager;
- Compass Employee.

The current Frappe layer is ready for further implementation of server methods, permission logic, ML-service calls and result persistence.

## Planned HR module behavior

The future module is intended to work as an additional layer over ERPNext/Frappe HRMS.

Planned behavior:

- read HRMS employee and organization data;
- keep module-specific snapshots and analysis results in custom DocTypes;
- generate career predictions;
- extract and normalize employee skills;
- recommend learning paths;
- estimate salary ranges;
- build team plans;
- separate internal assignment, upskilling and external hiring options;
- store explanations and reason codes;
- preserve recommendation history.

The module should not directly rewrite core HRMS data as part of ML inference. Results should be stored in module-specific DocTypes.

## ML and data scaffold

The ML part is located in:

    ml/

Current ML preparation includes:

- Python 3.11 virtual environment;
- requirements file;
- Jupyter kernel;
- importable Python package;
- ETL module structure;
- schema module structure;
- utility module structure;
- smoke test;
- local data folders;
- cached data source layout.

Data folders:

    data/raw
    data/interim
    data/processed
    data/cache

External data sources planned or partially prepared:

- Rostrud / Zenodo career trajectory dataset;
- hh.ru vacancies API;
- Stepik course catalog API;
- local resumes in PDF, DOCX or TXT format.

Large datasets, API caches, processed artifacts, indexes and future model weights are intended to stay out of git.

## ETL status

Prepared ETL work includes:

- Rostrud / Zenodo work experience ingestion;
- demo-small processing mode;
- cleaned work experience parquet output;
- career trajectory parquet output;
- normalized roles parquet output;
- input CSV inspection mode;
- hh.ru vacancy fetch with local cache;
- hh.ru vacancy parse into processed parquet;
- Stepik course search fetch with local cache;
- Stepik course parse into processed parquet;
- ETL smoke test.

The ETL layer is designed for reproducibility and local development. Repeated API calls should use cache where possible to avoid unnecessary network requests and rate-limit issues.

## Planned NLP layer

The planned NLP layer should add:

- multilingual or Russian-compatible text embeddings;
- vector storage, likely Qdrant;
- vacancy embeddings;
- course embeddings;
- role profile embeddings;
- resume embeddings;
- skill extraction from vacancies and resumes;
- skill normalization;
- alias matching;
- mapping extracted skills into Compass Skill records.

Planned tools may include:

- sentence-transformers;
- transformers;
- torch;
- Natasha;
- YAKE;
- rapidfuzz;
- Qdrant.

This part is not completed yet.

## Planned career model

The planned career model should predict possible next roles from career trajectories.

Planned tasks:

- role tokenization;
- sequence dataset generation;
- train/validation/test split;
- Transformer, GRU or LSTM model;
- next-role prediction;
- top-N recommendations;
- reason codes;
- similar trajectory explanations;
- frequent transition explanations;
- skill-gap explanations.

Model weights and mappings should be stored as a separate model pack, not committed directly to git.

## Planned salary model

The planned salary model should estimate salary ranges or hiring cost ranges.

Planned inputs:

- region;
- role;
- experience level;
- employment format;
- extracted skills;
- vacancy text features;
- employer aggregates where available.

The intended model type is CatBoost or another tabular model suitable for salary-range estimation.

## Planned recommendation logic

The future recommendation layer should connect employees, target roles and courses.

Planned pipeline:

    Employee profile
          ↓
    Skill profile snapshot
          ↓
    Target role profile
          ↓
    Skill-gap calculation
          ↓
    Course ranking
          ↓
    Learning recommendation with explanations

Recommendations should explain why a role or course was suggested.

## Planned TeamPlan logic

The future TeamPlan feature should work as a planning sandbox inside the module.

It should help compare:

- internal assignment;
- upskilling existing employees;
- external hiring;
- estimated salary range;
- required skills;
- expected gaps;
- recommended learning actions.

TeamPlan should store results in module-specific DocTypes instead of changing real Department or Employee data.

## Planned ML service

The planned ML service should expose a FastAPI interface.

Expected endpoints:

    GET /health
    POST /career/predict-next
    POST /skills/extract
    POST /learning/recommend
    POST /team/plan
    GET /market/salary-range

The portal should call this service through configured URLs and write returned results into the custom Frappe DocTypes.

## Planned portal integration

Future Frappe integration should implement whitelisted server methods such as:

    generate_career_plan(employee_id)
    compute_team_plan(team_plan_id)
    refresh_skills_from_resume(employee_id)

Expected result storage:

- Career Prediction;
- Learning Recommendation;
- Team Plan results;
- Employee Skill Profile;
- Resume-derived skill snapshots.

The integration should include server-side permission checks and row-level visibility rules.

## Local development notes

The project is intended for local development.

Main local components:

- Frappe/ERPNext/HRMS portal in Docker;
- custom Frappe app under `portal/custom_app`;
- ML code under `ml/`;
- local datasets and caches under `data/`;
- documentation under `docs/`.

The local Python version used for the ML scaffold is Python 3.11.14.

The ML virtual environment is stored locally in:

    ml/.venv

It is excluded from git.

## Project structure

    Frappe-HR-Forge/
    ├── data/
    │   ├── raw/
    │   ├── interim/
    │   ├── processed/
    │   └── cache/
    ├── docs/
    │   └── todo.md
    ├── ml/
    │   ├── notebooks/
    │   ├── requirements.txt
    │   ├── pyproject.toml
    │   └── src/
    │       └── compass_hr_ai/
    │           ├── etl/
    │           ├── schemas/
    │           └── utils/
    ├── portal/
    │   ├── custom_app/
    │   │   └── compass_hr_ai/
    │   └── frappe_docker/
    ├── seed/
    │   └── demo CSV files
    └── README.md

## Development roadmap

Major remaining work:

- complete NLP layer;
- add vector store;
- implement skill extraction;
- train career trajectory model;
- train salary-range model;
- implement recommendation ranking;
- implement TeamPlan planner;
- expose ML service through FastAPI;
- connect portal buttons to ML service;
- implement row-level access rules;
- add resume parsing;
- add tests;
- write architecture and API documentation;
- prepare demo stack scripts.

## Notes

Frappe HR Forge is a development base for future custom HR functionality on top of ERPNext and Frappe HRMS.

It currently provides the portal foundation, custom app structure, DocTypes, roles, permissions, demo data, ML environment and ETL scaffold. The advanced ML recommendation and planning features are planned next steps rather than finished production functionality.