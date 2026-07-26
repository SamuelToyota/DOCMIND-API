# DOCMIND-API

DOCMIND-API e uma API REST desenvolvida com Django para upload, autenticacao e processamento de documentos. O projeto permite que usuarios autenticados enviem arquivos, tenham seus documentos associados automaticamente a propria conta e iniciem um fluxo de processamento com extracao de texto, divisao do conteudo em chunks e consulta desses chunks pela API.

O objetivo do projeto e servir como base para uma aplicacao de leitura inteligente de documentos, preparando o backend para etapas futuras como busca semantica, embeddings, resumos automaticos e perguntas e respostas com IA.

## Tecnologias

- Python
- Django
- Django REST Framework
- SimpleJWT
- SQLite

## Funcionalidades

- Autenticacao com JWT.
- Rotas protegidas por usuario autenticado.
- Upload de documentos via API.
- Validacao de tamanho maximo do arquivo.
- Validacao de extensoes permitidas.
- Associacao automatica do documento ao usuario logado.
- Extracao de texto de arquivos `.txt`.
- Extracao de texto de PDFs com texto selecionavel.
- Extracao de texto de arquivos `.docx`.
- Controle de status do processamento.
- Divisao do texto extraido em chunks.
- Persistencia dos chunks relacionados ao documento.
- Consulta dos chunks de um documento pela API.

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
GET    /api/documents/{id}/chunks/
PUT    /api/documents/{id}/
PATCH  /api/documents/{id}/
DELETE /api/documents/{id}/
```

A listagem de documentos retorna apenas os documentos do usuario autenticado.

## Exemplo De Autenticacao

```bash
curl -X POST http://localhost:8000/api/auth/token/ \
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
curl -X POST http://localhost:8000/api/documents/ \
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

No estado atual do projeto, a extracao de texto esta implementada para arquivos `.txt`, PDFs com texto selecionavel e arquivos `.docx`.

Observacao: PDFs escaneados como imagem ainda nao passam por OCR, entao podem retornar pouco ou nenhum texto.

## Como Executar

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

A API fica disponivel em:

```txt
http://localhost:8000
```

Exemplo:

```txt
http://localhost:8000/api/documents/
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
- `error_message`
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

- Adicionar testes automatizados para upload e processamento.
- Melhorar tratamento de arquivos sem texto extraivel.
- Evitar recriacao duplicada de chunks em fluxos futuros de reprocessamento.
- Preparar embeddings a partir dos chunks.
- Implementar busca semantica sobre documentos.
- Evoluir para um fluxo de perguntas e respostas com IA.

## Resumo

DOCMIND-API e uma base backend para processamento inteligente de documentos. O projeto ja possui autenticacao JWT, upload protegido, validacao de arquivos, extracao de texto de TXT, PDF e DOCX, chunking e consulta de chunks, formando uma fundacao solida para recursos futuros de IA aplicada a documentos.
