# DOCMIND-API

DOCMIND-API e uma API REST desenvolvida com Django para upload, autenticacao e processamento de documentos. O projeto permite que usuarios autenticados enviem arquivos, tenham seus documentos associados automaticamente a propria conta e iniciem um fluxo de processamento com extracao de texto e divisao do conteudo em chunks.

O objetivo do projeto e servir como base para uma aplicacao de leitura inteligente de documentos, preparando o backend para etapas futuras como busca semantica, embeddings, resumos automaticos e perguntas e respostas com IA.

## Tecnologias

- Python
- Django
- Django REST Framework
- SimpleJWT
- SQLite
- Docker
- Docker Compose

## Funcionalidades

- Autenticacao com JWT.
- Rotas protegidas por usuario autenticado.
- Upload de documentos via API.
- Validacao de tamanho maximo do arquivo.
- Validacao de extensoes permitidas.
- Associacao automatica do documento ao usuario logado.
- Extracao de texto de arquivos `.txt`.
- Controle de status do processamento.
- Divisao do texto extraido em chunks.
- Persistencia dos chunks relacionados ao documento.
- Ambiente containerizado com Docker e Docker Compose.

## Fluxo De Processamento

```txt
Upload do documento
        |
        v
Validacao de tipo e tamanho
        |
        v
Documento salvo com owner=request.user
        |
        v
Status: processing
        |
        v
Extracao de texto
        |
        v
Geracao de chunks
        |
        v
Status: ready
```

Se ocorrer algum erro durante o processamento, o documento recebe o status `failed`.

## Endpoints Principais

### Autenticacao

```txt
POST /api/auth/token/
POST /api/auth/token/refresh/
```

### Documentos

```txt
GET    /api/documents/
POST   /api/documents/
GET    /api/documents/{id}/
PUT    /api/documents/{id}/
PATCH  /api/documents/{id}/
DELETE /api/documents/{id}/
```

A listagem de documentos retorna apenas os documentos do usuario autenticado.

## Exemplo De Autenticacao

```bash
curl -X POST http://localhost:2222/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"seu_usuario\",\"password\":\"sua_senha\"}"
```

Resposta esperada:

```json
{
  "refresh": "token_refresh",
  "access": "token_access"
}
```

## Exemplo De Upload

```bash
curl -X POST http://localhost:2222/api/documents/ \
  -H "Authorization: Bearer seu_access_token" \
  -F "title=Meu documento" \
  -F "file=@documento.txt"
```

Arquivos aceitos:

```txt
.pdf
.txt
.docx
```

Tamanho maximo:

```txt
10 MB
```

No estado atual do projeto, a extracao de texto esta implementada para arquivos `.txt`.

## Rodando Com Docker Compose

Suba a aplicacao com:

```bash
docker compose up
```

Ou, se precisar reconstruir a imagem:

```bash
docker compose up --build
```

A API fica disponivel em:

```txt
http://localhost:2222
```

Exemplo:

```txt
http://localhost:2222/api/documents/
```

Para parar:

```bash
docker compose down
```

## Rodando Localmente

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Rode as migracoes:

```bash
python manage.py migrate
```

Inicie o servidor:

```bash
python manage.py runserver
```

## Estrutura Principal

```txt
DOCMIND-API/
+-- config/
|   +-- settings.py
|   +-- urls.py
+-- documents/
|   +-- models.py
|   +-- serializers.py
|   +-- services.py
|   +-- urls.py
|   +-- views.py
+-- docker-compose.yml
+-- dockerfile
+-- manage.py
+-- requirements.txt
+-- README.md
```

## Modelos Principais

### Document

Representa um arquivo enviado por um usuario.

Campos principais:

- `owner`
- `title`
- `file`
- `text_content`
- `status`
- `created_at`
- `updated_at`

### DocumentChunk

Representa uma parte do texto extraido de um documento.

Campos principais:

- `document`
- `chunk_index`
- `content`
- `created_at`

## Status Do Documento

```txt
uploaded    Documento enviado
processing  Documento em processamento
ready       Documento processado com sucesso
failed      Falha durante o processamento
```

## Proximos Passos

- Expor uma rota especifica para consultar chunks de um documento.
- Implementar extracao de texto para PDF e DOCX.
- Adicionar testes automatizados para upload e processamento.
- Preparar embeddings a partir dos chunks.
- Implementar busca semantica sobre documentos.
- Evoluir para um fluxo de perguntas e respostas com IA.

## Resumo

DOCMIND-API e uma base backend para processamento inteligente de documentos. O projeto ja possui autenticacao JWT, upload protegido, validacao de arquivos, extracao de texto, chunking e execucao com Docker, formando uma fundacao solida para recursos futuros de IA aplicada a documentos.
