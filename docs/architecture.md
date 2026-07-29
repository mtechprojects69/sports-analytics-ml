# Arquitetura de Dados

## Landing

Cloud Storage

Formato original

JSON

CSV

Parquet

Estrutura

landing/

statsbomb/

football-data/

clubelo/

---
## Mapeamento das Camadas

| Camada Conceitual | Implementação Física |
|-------------------|----------------------|
| Landing | Cloud Storage |
| Bronze | BigQuery - dev_raw |
| Silver | BigQuery - dev_core |
| Gold | BigQuery - dev_marts |

> Neste projeto utilizamos a nomenclatura Bronze, Silver e Gold para representar as camadas da arquitetura Medallion. No BigQuery, essas camadas são implementadas fisicamente nos datasets `dev_raw`, `dev_core` e `dev_marts`.

---

## Bronze

BigQuery

Uma entidade = uma tabela

Exemplo

bronze_statsbomb_competitions

bronze_statsbomb_matches

bronze_statsbomb_events

bronze_statsbomb_lineups

---

## Silver

Modelo normalizado.

Exemplo

silver_competitions

silver_matches

silver_teams

silver_players

silver_events

silver_lineups

---

## Gold

Modelo analítico.

Exemplo

gold_match_features

gold_team_features

gold_player_features

gold_predictions

gold_dashboard_metrics

---

# Padrões

Todas as tabelas devem possuir:

created_at

updated_at

source

ingestion_date

---

# Estratégia de Particionamento

Match Date

Ingestion Date

---

# Estratégia de Clusterização

competition_id

season_id

match_id

team_id