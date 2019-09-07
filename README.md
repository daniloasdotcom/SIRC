# SIRC (Sistema de Interpretação e Recomendação de Calagem)

## F.A.Q
### Em resumo, qual a rotina do programa em desenvolvimento?
1. O programa recebe dados de análises de solo (dados químicos) e dados intrínsecos da área de cultivo
2. A partir desses dados são:
    - Realizados cálculos da necessidade de calagem (esses cálculos respondem ao interessado qual a quantidade de calcário necessária para melhorar as condições químicas - principalmente o pH - do solo em questão)
    - Gerados:
	    - Um relatório indicando quais possíveis amostras não precisam de calagem e deveriam passar por uma observação do técnico
	    - Uma recomendação indicando quanto de calcário aplicar em termos de quantidade por tipo de aplicação

### Em quais situações o programa é útil?
1. O programa acelera a tomada de decisão sobre atividades de calagem e  automatizando as fases de interpretação, recomendação e produção da recomendação
   - É especialmente útil quando interessados (técnicos, gerentes de empreendimentos rurais e produtores rurais) possuem um número elevado de resultados de análise de solo que precisão ser interpretados e posteriormente geradas as recomendações de calagem 

## Construído Com:
1. Linguagem - Python
2. IDE - PyCharm
3. Para interface - Tkinter
 
## Sobre os principais arquivos

### Manual_v1.0.pdf
Arquivo texto explicando como utilizar o programa 
    
### planilha de dados.csv
Planilha com dados de 4 amostras de solos para testar a versão atual do programa

### sirc.py
Integra todos os códigos: de interpretadores, cálculos necessários, produção de relatórios e interface para o usuário

### LICENSE
Licença MIT do projeto

## Agradecimentos

À Weverton Carlos (Yrmão) e Felipe (Felipinho), pelas dicas que me ajudaram nas etapas que levaram ao desenvolvimento deste primeiro projeto.