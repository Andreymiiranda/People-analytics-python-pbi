# 📊 People Analytics: Gestão e Desempenho de RH

## 📋 Descrição do Projeto
Este projeto apresenta uma solução analítica completa para a área de Recursos Humanos. O objetivo foi desenvolver um pipeline de dados automatizado, realizando a extração e transformação (ETL) de diferentes bases do setor usando **Python**, para finalmente disponibilizar insights estratégicos em um dashboard gerencial no **Power BI**.

As análises cobrem pilares fundamentais do RH, incluindo controle de absenteísmo, gestão de treinamentos corporativos, avaliações de desempenho e eficiência do funil de recrutamento.

## 🛠️ Ferramentas Utilizadas
* **Linguagem de Programação:** Python (Pandas)
* **Visualização de Dados:** Power BI
* **Estrutura de Dados:** Arquivos CSV modelados em tabelas Fato e Dimensão.

## ⚙️ Processo de ETL (Desenvolvido 100% em Python)
Todo o pipeline de processamento e limpeza de dados foi arquitetado e desenvolvido do zero por mim, utilizando a biblioteca **Pandas**. O script `main.py` é o núcleo do projeto, responsável por automatizar a preparação das bases de dados brutas antes de chegarem ao Power BI. 

O fluxo de engenharia de dados construído consiste em:
1. **Extração (Extract):** * Leitura automatizada dos arquivos CSV originais: `funcionarios.csv`, `treinamentos.csv`, `absenteismo.csv`, `avaliacoes_desempenho.csv` e `recrutamento_vagas.csv`.
2. **Transformação (Transform):** * **Sanear Dados:** Identificação e tratamento de valores nulos, remoção de duplicatas e correção de tipagem de dados (datas, valores financeiros, textos).
   * **Regras de Negócio:** Criação de colunas calculadas e padronização de categorias (ex: consolidando o status de conclusão dos treinamentos e calculando o custo/hora).
   * **Modelagem Relacional:** Cruzamento de tabelas (Merges/Joins) para integrar o histórico de cada funcionário com suas respectivas métricas.
3. **Carga (Load):** * Geração de arquivos finais consolidados, estruturados perfeitamente para otimizar a performance de modelagem no Power BI. Inclui também um `dicionario_de_dados.csv` documentando as regras.

> 💡 **Destaque Técnico:** A automação desse processo em Python garante escalabilidade. Quando o RH gerar novas planilhas nos meses seguintes, basta rodar o `main.py` para que os dados sejam higienizados e o dashboard seja atualizado perfeitamente.

## 📈 Dashboard e Insights (Power BI)
O modelo estruturado pelo Python foi conectado ao Power BI para a criação do painel analítico. O relatório permite o cruzamento de dados entre diferentes áreas do RH.

**(Exemplo de Visões e KPIs):**
* Monitoramento da taxa de conclusão dos cursos (Concluído, Não Concluído, Em Andamento).
* Distribuição de engajamento por categoria (Técnico, Comportamental, Obrigatório).
* Média de horas de treinamento investidas por colaborador e custo total.
* Total de colaboradores ativos, assim como, número de contratações são alguns insights presentes no dashboard.

> ** [Clique aqui para acessar o Dashboard Interativo no Power BI](https://app.powerbi.com/groups/me/reports/35ee9395-21bd-4953-908b-bc797529192a/6b1108e0fc9cda4c84ad?experience=power-bi))**

## 🚀 Como Executar o Projeto
1. Clone este repositório:
  ```bash
   git clone https://github.com/Andreymiiranda/People-analytics-python-pbi.git
