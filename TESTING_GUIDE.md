# Guia de testes

A suíte pytest cobre o serviço, a API REST e o protocolo MCP sem mudar o comportamento da aplicação. Os dados continuam sendo o mock de `app/service.py`. O adapter do DJEN não entra nesses testes.

Sete desafios estão incompletos de propósito. Cada um tem `TODO(STUDENT)` e `@pytest.mark.skip`. A suíte baseline fica verde até você remover o skip e implementar o que falta. Este guia não traz a solução.

## Categorias

- **Unitário** (`tests/unit/`): chama `app.service` direto. Não sobe HTTP nem o protocolo MCP.
- **Integração** (`tests/integration/`): atravessa uma borda real. REST usa `TestClient`. MCP usa o `Client` oficial do SDK, no mesmo processo, para listar e invocar tools. Esses testes não chamam as funções Python das tools.
- **Smoke** (`mcp_smoke.py`): script manual, fora do pytest. Sobe o servidor por stdio. `test_server.py` continua sendo o smoke HTTP contra um servidor já ligado em `localhost:8000`.

## Comandos

Na raiz do repositório, com o virtualenv ativo:

```bash
python -m pytest
python -m pytest tests/unit
python -m pytest tests/integration
python -m pytest -k intimations
python -m pytest -rs
```

`-rs` mostra o motivo de cada skip. Para um desafio, rode o teste nomeado no final da seção correspondente depois de remover o skip.

`pytest.ini` aponta `testpaths` para `tests/`.

## Fixtures

`tests/conftest.py` tem duas fixtures prontas.

- `no_artificial_delay` é `autouse`. Ela troca `app.service.time.sleep` por uma função vazia. Em produção a busca ainda espera 0,5 s. No pytest, não.
- `golden` lê `tests/data/golden_intimations.json`.

`tests/integration/conftest.py` oferece `client`, um `TestClient` da aplicação FastAPI.

`monkeypatch` é uma fixture embutida do pytest. Use-a para substituir um nome já importado no módulo que a rota chama.

## Mocks

O atraso artificial é o exemplo pronto de mock: `monkeypatch.setattr` no `sleep` do serviço. O teste não precisa de relógio real porque a espera não faz parte da regra de filtro.

Um mock de teste deve substituir a dependência na fronteira que você quer observar. Se a pergunta é "a rota repassa o retorno do serviço?", o alvo é a função que a rota já importou, não uma cópia nova da regra de negócio.

## Asserções

Confira o que o comportamento promete: status HTTP, tamanho da lista, igualdade de um campo, ou o tipo da exceção. `assert` falho mostra o valor recebido. `pytest.raises` falha se a exceção não acontece ou se a mensagem não casa.

`pytest.fail` dentro de um desafio pulado não roda enquanto o skip existir. Se você tirar o skip e não implementar, o teste fica vermelho de propósito.

## Regressão e golden dataset

`tests/data/golden_intimations.json` guarda entradas e saídas determinísticas: busca feliz, tribunal sem resultado, nome em outra caixa, OAB que não casa, datas inválidas e um processo ausente.

Um teste de regressão lê um caso desse arquivo e compara a saída com `expected_case_numbers`. Se alguém mudar o filtro e o resultado deixar de bater com o arquivo, o teste quebra. O arquivo é a expectativa; o teste não redefine a regra na mão.

O caminho feliz `pedro_on_sample_day` já está coberto. Os outros casos de busca são o desafio 3.

## Smoke

`python mcp_smoke.py` prova o transporte stdio de ponta a ponta. Ele não faz parte da suíte pytest e o CI não o executa. Use-o quando quiser ver um processo MCP separado. A suíte de integração cobre o mesmo protocolo por um cliente in-process, mais rápido e sem porta.

## CI/CD

`.github/workflows/pytest.yml` roda em `push` e `pull_request`. O job usa Python 3.11, instala `requirements.txt` e executa `python -m pytest`. Skips contam como suíte verde.

O workflow ainda dispara em qualquer arquivo do repositório. Restringir isso é o desafio 7. Este repositório não publica o workflow daqui; a verificação local é o pytest.

## Desafios

Faça nesta ordem. Em cada um, apague o `pytest.mark.skip` e o `pytest.fail` quando a implementação estiver pronta.

### 1. Asserções

- Objetivo: travar o catálogo de tribunais, não só o tamanho da lista.
- Arquivo: `tests/unit/test_list_courts.py`
- O que implementar: `test_court_codes_match_catalog`.
- Comportamento esperado: o teste passa e confere código e nome de cada tribunal que `list_courts()` devolve, na ordem do catálogo.
- Comando: `python -m pytest tests/unit/test_list_courts.py::test_court_codes_match_catalog -rs`
- Conceito: asserção.

### 2. Exceções

- Objetivo: garantir que um processo ausente falha de forma explícita.
- Arquivo: `tests/unit/test_validation.py`
- O que implementar: `test_unknown_case_raises_not_found`, usando o caso ausente do golden.
- Comportamento esperado: a chamada levanta `NotFound` e a mensagem identifica o número pedido. Outra exceção, ou uma mensagem genérica, falha o teste.
- Comando: `python -m pytest tests/unit/test_validation.py::test_unknown_case_raises_not_found -rs`
- Conceito: teste de exceção.

### 3. Parametrize e regressão

- Objetivo: repetir a mesma checagem para os casos de busca do golden que ainda não têm teste.
- Arquivo: `tests/unit/test_search_golden.py`
- O que implementar: `test_remaining_golden_cases`, com `@pytest.mark.parametrize` sobre esses casos.
- Comportamento esperado: cada caso parametrizado devolve exatamente os números de processo esperados no JSON. Um caso a mais ou a menos deixa o teste vermelho.
- Comando: `python -m pytest tests/unit/test_search_golden.py::test_remaining_golden_cases -rs`
- Conceito: teste parametrizado e regressão por golden dataset.

### 4. Fixtures

- Objetivo: reutilizar um registro conhecido em vez de montá-lo dentro do teste.
- Arquivos: `tests/unit/conftest.py` e `tests/unit/test_cases.py`
- O que implementar: a fixture `known_case` e o corpo de `test_get_known_case`.
- Comportamento esperado: a fixture fornece um registro da amostra; o teste busca esse processo e o retorno é o mesmo registro.
- Comando: `python -m pytest tests/unit/test_cases.py::test_get_known_case -rs`
- Conceito: fixture.

### 5. Mocks

- Objetivo: provar que a rota HTTP entrega o que o serviço devolve, sem depender do filtro real.
- Arquivo: `tests/integration/test_rest_api.py`
- O que implementar: `test_route_uses_service_result`, com `monkeypatch` em `app.main.search_intimations`.
- Comportamento esperado: `GET /intimations` responde 200 com o retorno falso que você instalou. Se a rota ignorar o mock e ler o dataset, o teste falha.
- Comando: `python -m pytest tests/integration/test_rest_api.py::test_route_uses_service_result -rs`
- Conceito: mock com `monkeypatch`.

### 6. Erro no protocolo MCP

- Objetivo: observar um erro de entrada do outro lado do protocolo, pelo cliente MCP.
- Arquivo: `tests/integration/test_mcp_protocol.py`
- O que implementar: `test_get_intimations_invalid_date_is_error`. Use o `Client`, como os testes que já passam nesse arquivo. Não chame a função Python da tool.
- Comportamento esperado: a invocação com data inválida termina com `is_error` verdadeiro e o texto contém `Invalid date format`.
- Comando: `python -m pytest tests/integration/test_mcp_protocol.py::test_get_intimations_invalid_date_is_error -rs`
- Conceito: teste de integração do protocolo e erro controlado.

### 7. GitHub Actions

- Objetivo: o workflow de pytest deixar de rodar em mudanças que não afetam a aplicação nem os testes.
- Arquivo: `.github/workflows/pytest.yml`
- O que implementar: um filtro `paths` em `push` e em `pull_request`.
- Comportamento esperado: os dois triggers continuam presentes. O job só é agendado quando a mudança toca `app/`, `tests/`, `requirements.txt` ou o próprio workflow. `python -m pytest` local segue verde.
- Comando: revise o YAML e rode `python -m pytest`. O GitHub não é executado a partir desta máquina.
- Conceito: CI disparado por caminho.
