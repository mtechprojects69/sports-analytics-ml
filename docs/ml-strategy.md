# Estratégia de Machine Learning

## Objetivo

Construir modelos capazes de prever resultados de partidas de futebol utilizando dados históricos e engenharia de features.

---

# MVP

## Modelo 1

Classificação

Saída

Home Win

Draw

Away Win

---

## Modelo 2

Regressão

Saída

Expected Home Goals

Expected Away Goals

---

## Modelo 3

Predição de Placar

Saída

2x1

1x0

3x2

---


# Fontes

StatsBomb

Football-Data

ClubElo

---

# Feature Store

Todas as features serão produzidas na camada Gold.

Exemplos

Forma

Elo

xG

Últimos confrontos

Dias de descanso

Média de gols

Posse

Pressão

Cartões

Finalizações

Escalação

---

# Avaliação

Classificação

Accuracy

Precision

Recall

F1

LogLoss

ROC-AUC

---

Regressão

RMSE

MAE

R²

---

# Versionamento

Todos os modelos deverão possuir:

Model Version

Training Date

Training Dataset Version

Feature Version

---

# Deployment

Model Registry

Prediction API

Batch Prediction

Online Prediction