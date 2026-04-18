# Base de Conhecimento

## Dados Utilizados

Os arquivos da pasta `data` foram utilizados para fornecer o contexto financeiro do usuário à Anya, permitindo análises precisas e personalizadas:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores (ex: verificar se o cliente já buscou ajuda para renegociar dívidas antes). |
| `perfil_investidor.json` | JSON | Avaliar se o cliente possui alguma reserva de emergência que possa ser usada para abater a dívida. |
| `produtos_financeiros.json` | JSON | Buscar opções de crédito com juros menores (ex: Crédito Pessoal) para substituir dívidas caras (rotativo do cartão). |
| `transacoes.csv` | CSV | Analisar o padrão de gastos do cliente, identificando excessos em categorias como *delivery*, serviços não essenciais e acúmulo de compras parceladas. |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

A estrutura original dos dados mockados foi mantida. No entanto, para fins de processamento da aplicação, garantimos que o arquivo `transacoes.csv` possua uma coluna de "Categoria" (ex: *Delivery*, *Assinaturas*, *Essenciais*) e "Tipo" (ex: *À vista*, *Parcelado*). Isso permite que o código Python agrupe os gastos antes de enviá-los ao LLM, otimizando o uso de tokens e melhorando a assertividade da IA.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os dados são processados localmente utilizando a linguagem **Python** e a biblioteca **Pandas**. Quando o usuário inicia a sessão na interface construída com **Streamlit**, os arquivos CSV e JSON são lidos e carregados em *DataFrames* e dicionários na memória (utilizando o `@st.cache_data` do Streamlit para performance). 

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados não são jogados inteiros no prompt para evitar estouro de limite de tokens e alucinações. A estratégia é **Injeção Dinâmica de Contexto (RAG simplificado)**:
1. O Pandas filtra e sumariza as transações (ex: Total gasto em Delivery no mês).
2. O código Python busca no JSON apenas os produtos de crédito adequados ao perfil.
3. Esse resumo filtrado é injetado dinamicamente no *System Prompt* daquela interação específica, dando à Anya o contexto exato que ela precisa para aconselhar o usuário.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```text
[CONTEXTO DO SISTEMA]
Dados do Cliente:
- Nome: Lucas
- Status: Alerta (Uso do rotativo do cartão de crédito)
- Saldo devedor do Cartão: R$ 2.500,00

Resumo de Transações (Últimos 30 dias):
- Alimentação / Delivery: R$ 650,00
- Assinaturas (Streaming/Jogos): R$ 120,00
- Compras parceladas (Vestuário): R$ 400,00

Produtos Disponíveis para Renegociação:
- Produto: Crédito Pessoal Jovem
- Taxa de Juros: 2.5% a.m. (Ideal para substituir os 15% a.m. do rotativo)
- Condição: Parcelamento em até 24x