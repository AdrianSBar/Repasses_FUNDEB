# Previsão de séries temporais dos recursos do FUNDEB
<img src="https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb/fundeb-home/@@collective.cover.banner/e0c58aa7-955e-4d4b-a99a-a6bfaaf50a18/@@images/81160181-a1d1-4a84-a467-2061f366a939.jpeg">

- Para quem não conhece, o FUNDEB (Fundo de Manutenção e Desenvolvimento da Educação Básica e de Valorização dos Profissionais da Educação) é um fundo criado pelo governo federal brasileiro para financiar a manutenção e desenvolvimento da educação básica pública no Brasil, além de valorizar os profissionais da educação. Os recursos são repassados todos os meses às esferas estaduais e municipais e são compostos por recursos provenientes de impostos dos estados, distrito federal, municípios e do governo federal, destinados ao financiamento da educação infantil, fundamental e média do setor público, incluindo a educação de jovens e adultos. Para mais informações, consulte clicando [Aqui...](https://www.gov.br/fnde/pt-br/acesso-a-informacao/acoes-e-programas/financiamento/fundeb)

## Introdução
- Este é um projeto de ciência de dados, de ponta a ponta, voltado aos dados históricos de repasses de recursos financeiros ao FUNDEB, contemplando desde a Extração dos dados (via web scrapping) até a implementação do produto final (dashboards com previsão dos próximos 12 meses).

---

## 1. Metodologia
- O projeto em sí se baseará na metodologia **ASUM-DM (Analytics Solutions Unified Method for Data Mining)** é uma metodologia que moderniza e expande o CRISP-DM usada em projetos de ciência de dados e mineração de dados, incorporando práticas ágeis e mais foco em produção e reuso.

---

## 2. Tecnologias e ferramentas
- Resumidamente, o projeto foi desenvolvido em Python com Jupyter Notebook dentro do Visual Studio Code (Editor) contando com o pacote Anaconda para administrar o ambiente de desenvolvimento, sendo que este projeto foi controlado e versionado através do Git e github.
- As bibliotecas bases utilizadas no python foram selenium para web scraping, pandas e numpy para processamento dos dados, steamlit para dashboards e sckitlearn para previsões.
- ...
---

## 3. Pipeline da solução
### **a. Planejamento Inicial e Preparação**
   - **Definição do Projeto:**  
     - Objetivo: Prever os repasses do FUNDEB nos próximos 12 meses e disponibilizar visualizações interativas para apoio à tomada de decisão.  
     - Stakeholders: Secretarias estaduais/municipais de educação, gestores públicos e analistas financeiros.
     - Requisitos:  
       - Precisão das previsões (ex.: RMSE < 10%).  
       - Atualização automática das previsões com novos dados.
       - Interface intuitiva para exibir repasses e previsões.

   - **Definição de Escopo e Entregáveis:**  
     - Pipeline automatizado para coleta e processamento de dados.
     - Protótipo inicial do dashboard com dados históricos.
     - Modelo preditivo funcional.

   - **Plano de Comunicação:**  
     - Como se trata de um projeto de portfólio individual, não há plano de comunicação.


### **b. Entendimento do Negócio**
   - **Questões Críticas:**  
     - Como os repasses variam entre regiões e períodos?
        - Desigualdades socioeconômicas:
          Regiões com menor arrecadação de impostos (como Norte e Nordeste) recebem maior complementação da União para atingir o valor mínimo anual por aluno (VAA).
          Estados e municípios mais ricos (como Sudeste e Sul) dependem menos dos recursos federais, pois conseguem atingir o VAA com suas próprias receitas.
        - Número de matrículas e modalidades de ensino:
          O FUNDEB distribui recursos com base no número de alunos matriculados, ponderados por "custos" diferenciados (ex.: educação infantil, ensino integral, educação especial).
          Regiões com maior demanda por modalidades de ensino de custo elevado (como zonas rurais ou comunidades quilombolas) recebem mais recursos.
        - Dinâmica demográfica:
          Áreas com crescimento populacional acelerado (ex.: periferias urbanas) podem ter aumento de matrículas, elevando os repasses ao longo do tempo.
     - Quais variáveis têm maior impacto nos repasses (PIB, população, índices educacionais, etc.)?  
     - Como apresentar essas informações de forma intuitiva para diferentes públicos?  

   - **Objetivos Técnicos:**  
     - Desenvolver previsões usando modelos de séries temporais ou aprendizado de máquina.  
     - Construir pipelines escaláveis para ingestão e transformação de dados.


### **c. Entendimento e Exploração dos Dados**
   - **Coleta de Dados:**  
     - Implementar web scraping para portais governamentais de transparência.  
     - Explorar outras fontes de dados relevantes, como PIB estadual, IDEB e população.
   - **Análise Exploratória:**
     - Identificar padrões sazonais, tendências históricas e possíveis anomalias nos repasses.  
     - Visualizar correlações entre variáveis (ex.: repasses e PIB).
   - **Avaliação de Qualidade dos Dados:**  
     - Verificar se há valores ausentes, inconsistências ou duplicatas.  
     - Garantir que os dados históricos estejam completos e confiáveis.


### **d. Preparação dos Dados**
   - **Limpeza:**  
     - Tratar dados ausentes ou inconsistentes.  
     - Corrigir erros comuns, como formatos ou unidades inconsistentes.
   - **Transformação:**  
     - Criar variáveis derivadas: sazonalidade, crescimento percentual, valor per capita.  
     - Normalizar e padronizar os dados para modelos de aprendizado de máquina.
   - **Pipeline Automatizado:**
     - Construir scripts para automação de scraping, transformação e armazenamento dos dados.
     - Garantir versionamento dos dados para rastreamento.


### **e. Modelagem**
   - **Seleção de Modelos:**  
     - Modelos de séries temporais: ARIMA, SARIMA ou Prophet.  
     - Modelos de aprendizado de máquina: Random Forest, Gradient Boosting (XGBoost) ou Redes Neurais (LSTM).  
   - **Teste de Algoritmos:**  
     - Dividir os dados em conjuntos de treino, validação e teste.  
     - Comparar diferentes modelos com base em métricas de erro (ex.: RMSE, MAE).
   - **Iterações e Melhorias:**  
     - Refinar hiperparâmetros usando técnicas como Grid Search ou Random Search.


### **f. Validação**
   - **Métricas de Desempenho:**  
     - Avaliar o modelo em relação aos objetivos técnicos.  
     - Testar previsões com dados novos e medir a precisão.  
   - **Validação com Stakeholders:**  
     - Comparar previsões com a experiência de especialistas do setor público.  
     - Ajustar modelos conforme o feedback.
   - **Validação Ética e Legal:**  
     - Garantir que o uso dos dados cumpre com a LGPD e outras regulamentações.


### **g. Implantação e Integração**
   - **Automatização do Pipeline:**
     - Criar um pipeline que integre:
       - Coleta de dados (scraping).
       - Processamento e limpeza.
       - Treinamento e previsão do modelo.
   - **Criação do Dashboard:**  
     - Usar ferramentas como Power BI, Tableau ou Streamlit para:
       - Visualizar repasses históricos e previstos por estado/município.  
       - Mostrar sazonalidade e tendências.  
     - Integrar gráficos interativos, filtros e previsões futuras.  


### **h. Monitoramento e Manutenção**
   - **Manutenção do Modelo:**  
     - Monitorar a precisão do modelo e realizar retrainings periódicos.  
     - Incorporar novos dados para manter o modelo atualizado.  
   - **Atualização dos Dashboards:**  
     - Garantir que as visualizações refletem dados e previsões mais recentes.  
     - Testar a interface para melhorar a experiência do usuário.  
   - **Feedback Contínuo:**  
     - Reunir feedback regular dos stakeholders para ajustes e melhorias no projeto.


## 5. Principais insights


## 7. Resultados (Financeiros ou não)


## 8. Próximas etapas


## 9. Execute esse projeto na sua maquina local


## 10. Link dos dados
https://www.tesourotransparente.gov.br/publicacoes/transferencias-ao-fundo-de-manutencao-e-desenvolvimento-da-educacao-basica-fundeb/2024/114?ano_selecionado=2024


## 11. Contate-me
Linkedin: 

Github: 

Gmail: adrian.sbar07@gmail.com

---