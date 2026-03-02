# 📊 People Analytics: Gestão e Desempenho de RH

## 📋 Descrição do Projeto
Este projeto apresenta uma solução analítica completa para a área de Recursos Humanos. O objetivo foi desenvolver um pipeline de dados automatizado, realizando a extração e transformação (ETL) de diferentes bases do setor usando **Python**, para finalmente disponibilizar insights estratégicos em um dashboard gerencial no **Power BI**.

As análises cobrem pilares fundamentais do RH, incluindo controle de absenteísmo, gestão de treinamentos corporativos, avaliações de desempenho e eficiência do funil de recrutamento.

## 🛠️ Ferramentas Utilizadas
* **Linguagem de Programação:** Python (processamento de dados e regras de negócio)
* **Visualização de Dados:** Power BI
* **Estrutura de Dados:** Arquivos CSV divididos em Fatos e Dimensões.

## ⚙️ Arquitetura dos Dados e ETL (Python)
Todo o processo de limpeza, padronização e consolidação dos dados foi roteirizado no script `main.py`. O fluxo processa as seguintes bases brutas:

* **Tabela Dimensão:**
  * `funcionarios.csv`: Cadastro central contendo o perfil demográfico e profissional dos colaboradores.
* **Tabelas Fato:**
  * `treinamentos.csv`: Histórico de capacitações, modalidade (EAD/Presencial), status e custo.
  * `absenteismo.csv`: Registro de faltas, licenças e controle de presença.
  * `avaliacoes_desempenho.csv`: Notas, competências avaliadas e feedbacks das avaliações periódicas.
  * `recrutamento_vagas.csv`: Controle de vagas abertas, tempo de fechamento (SLA) e status das contratações.
* **Documentação:**
  * `dicionario_de_dados.csv`: Mapeamento completo detalhando o significado, tipo de dado e origem de cada coluna utilizada nas tabelas acima.

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
  
