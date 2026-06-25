# Dashboard FP&A | Financial Performance Analysis

## Visão Geral

Projeto desenvolvido para demonstrar a construção de uma solução completa de Business Intelligence utilizando Python, Power BI e conceitos de FP&A (Financial Planning & Analysis).

O objetivo é transformar dados transacionais em informações estratégicas para apoio à tomada de decisão executiva.

---

## Objetivos do Projeto

* Construir pipeline ETL para tratamento dos dados
* Criar indicadores financeiros e operacionais
* Simular metas orçamentárias (Budget)
* Desenvolver modelo dimensional
* Construir dashboard executivo interativo
* Aplicar boas práticas de Data Analytics

---

## Dashboard Executivo

### Principais KPIs

| Indicador      | Valor      |
| -------------- | ---------- |
| Receita Total  | R$ 127,9 M |
| Lucro Líquido  | R$ 17,7 M  |
| EBITDA         | R$ 51,8 M  |
| Margem Líquida | 14,88%     |
| Ticket Médio   | R$ 113,64  |

---

## Funcionalidades

### Aba Executiva

* Receita Total
* Lucro Líquido
* EBITDA
* Margem Líquida
* Ticket Médio
* Receita vs Budget

### Aba Comercial

* Receita por Segmento
* Receita por Produto
* Performance Comercial

### Aba Geográfica

* Receita por País
* Participação por Região

### Aba DRE

* Receita
* Custos
* Lucro
* Margens

---

## Arquitetura

Raw Data
↓
Python ETL
↓
Camada Processada
↓
Modelo Estrela
↓
Power BI
↓
Dashboard Executivo

---

## Tecnologias Utilizadas

* Python
* Pandas
* NumPy
* Power BI
* DAX
* Power Query
* Excel
* Git
* GitHub

---

## KPIs Desenvolvidos

### Financeiros

* Receita Total
* Lucro Líquido
* EBITDA
* Margem Líquida
* Budget vs Realizado

### Comerciais

* Ticket Médio
* Receita por Segmento
* Receita por Produto
* Receita por País

---

## ETL

O pipeline executa:

1. Leitura dos dados
2. Limpeza e tratamento
3. Remoção de duplicidades
4. Tratamento de nulos
5. Criação de métricas
6. Geração da tabela Budget
7. Construção da dimensão calendário
8. Exportação das tabelas analíticas

---

## Estrutura Dimensional

### Fato

FT_VENDAS

### Fatos Auxiliares

FT_BUDGET

### Dimensões

DIM_CALENDARIO

---

## Resultados

O dashboard fornece visão executiva consolidada da operação permitindo:

* Monitoramento de KPIs
* Acompanhamento de metas
* Identificação de desvios
* Comparação Budget vs Realizado
* Análise por segmento
* Análise geográfica

---

## Autor

Hoalys

Analista de Dados | Business Intelligence | Data Analytics | Power BI | Python
