# 🏛️ MCP-DGEN: Brazilian Court Notifications API Wrapper

> **MCP Server for DJEN Integration**  
> A public, LLM-ready interface for accessing Brazilian court notifications (DJEN).  
> Standardizes legal data into structured formats for AI applications.

---

## 📌 Repository Purpose

Este repositório é o primeiro **MCP Server** do mundo vinculado a uma **API pública governamental brasileira**, oferecendo uma camada intermediária entre o DJEN e sistemas automatizados (ex: LLMs, agentes, workflows).

**MCP = Model Context Protocol** → Este repositório é uma implementação prática desse padrão emergente, focado em:

- Uniformizar dados não estruturados do DJEN.
- Tornar a informação facilmente consumível por LLMs.
- Servir como *infraestrutura pública* para automações legais.

---

## 📂 Repositório: Estrutura Esperada

```bash
/mcp-djen-api/
├── README.md
├── openapi.yaml
├── adapter.py               # Core logic: fetch + parse + structure
├── docker-compose.yml
├── CONTRACT_TEMPLATE.md     # Template de proposta de consultoria ($150/h)
├── examples/
│   └── example_response.json
├── diagrams/
│   ├── architecture.png     # Diagrama de arquitetura
│   └── sequence.png         # Diagrama de fluxo da requisição
├── app/
│   ├── main.py              # FastAPI app
│   ├── routes.py
│   └── utils.py
└── Loom_Demo_Transcript_EN.srt # Legenda em inglês do vídeo de demonstração



📘 README.md — Estrutura Sugerida
1. Título
md
Copy
Edit
# Brazilian Court Data for LLMs: Standardized DJEN Endpoint
2. Visão
Explique o propósito com clareza:

🧠 Camada intermediária para sistemas de IA (ex: GPT, Claude) acessarem dados legais do Brasil.

🏛️ Wrapper inteligente da API do DJEN com formato padrão JSON.

🚀 Pensado para agentes autônomos, RAG e automações jurídicas.

3. Exemplo Real
“Este servidor MCP é usado no projeto Intimação Pro, onde reduz de 30 para 3 minutos o trabalho diário de centenas de advogados.”

4. Diagrama de Arquitetura
Inserir imagem diagrams/architecture.png.

Sugestão: API do TJMG → Adapter Layer (Python) → Output JSON padronizado.

5. Input / Output
Exemplo de Requisição:

http
Copy
Edit
GET /intimations?name=FULANO+DE+TAL&oab=123456&date_start=2025-08-06&date_end=2025-08-06
Resposta Padrão (mockada ou real):

json
Copy
Edit
[
  {
    "date": "2025-08-06",
    "court": "TJMG",
    "lawyer_name": "FULANO DE TAL",
    "oab": "123456/MG",
    "case_number": "1234567-89.2024.8.13.0001",
    "type": "TOMAR_CIÊNCIA",
    "summary": "Intimação para ciência de despacho proferido...",
    "url": "https://www.tjmg.jus.br/djen/123"
  }
]
6. Endpoints
GET /intimations: Wrapper da API pública

Query params: name, oab, date_start, date_end

Output: JSON estruturado

7. Deploy
Railway (deploy automático)
Link de exemplo: https://mcp-djen.up.railway.app/intimations?...

Instruções:

Suba no Railway com Dockerfile simples (FastAPI).

Exponha porta 8000.

Adicione variáveis se necessário (limite de requisições, headers).

📽️ Loom Vídeo
Gravar um vídeo explicando:

O problema de acesso ao DJEN

A visão de MCP como camada de infraestrutura

O repositório e seu funcionamento

Como ele é usado no Intimação Pro

Chamado para colaborações ou uso público

📎 CONTRATO DE CONSULTORIA
Arquivo: CONTRACT_TEMPLATE.md

Modelo:

md
Copy
Edit
## Proposta de Consultoria Técnica
**Projeto**: Integração MCP-DJEN  
**Valor**: $150/hora  
**Entregas**:
- Setup de servidor MCP para DJEN
- Parsing + padronização de output
- Deploy e documentação
📈 Expansão Futura
[+] Outras APIs públicas (Receita, SUS, Portal da Transparência)

[+] Adaptação para OpenAI Function Calling

[+] Versões multilíngues do endpoint (EN/PT)

🙌 Colaboração
Interessado em integrar esse MCP Server em sua lawtech, startup ou governo?
Abra uma issue, fork o projeto ou envie um e-mail: contact@pdrobrandao.com

🏁 Conclusão
Este projeto é uma prova viva de que é possível conectar IA com o Estado Brasileiro.
É um primeiro passo rumo a uma infraestrutura civil global para automação jurídica.

📜 Licença
MIT

yaml
Copy
Edit

---

Se quiser, posso montar também o `openapi.yaml`, o `Dockerfile` e o script inicial para `main.py`. Basta pedir.