# Sports Analytics Platform

## Visão

Construir uma plataforma SaaS para análise de dados esportivos, iniciando pelo futebol, capaz de ingerir dados de múltiplas fontes, processá-los, disponibilizá-los para BI e oferecer funcionalidades analíticas para clubes, analistas, scouts e entusiastas.

---

# Objetivos

- Arquitetura Cloud Native
- Custos baixos durante o MVP
- Escalabilidade
- Dados auditáveis
- Código desacoplado da infraestrutura
- Fácil colaboração entre desenvolvedores

---

# Stack Tecnológica

## Linguagem

Python 3.13

## Cloud

Google Cloud Platform

## Data Lake

Cloud Storage

## Data Warehouse

BigQuery

## Transformações

dbt

## Versionamento

Git + GitHub

## BI

Looker Studio

## Aplicação

Streamlit

## Orquestração (futura)

Dagster

---

# Princípios

- Landing sempre imutável
- JSON como formato bruto
- Parquet como formato otimizado
- BigQuery como Data Warehouse principal
- dbt para todas as transformações
- Código desacoplado do GCP
- Infraestrutura como detalhe de implementação

---

# Roadmap

Sprint 1
Infraestrutura básica

Sprint 2
Primeira ingestão

Sprint 3
Modelo Bronze

Sprint 4
Modelo Silver

Sprint 5
Modelo Gold

Sprint 6
Dashboard MVP

Sprint 7
Deploy MVP

Sprint 8
Primeiros usuários