<<<<<<< HEAD
🚖 TransFlow – Plataforma de Corridas Assíncronas + Dashboard Front-end

Sistema completo para gerenciamento de corridas, processamento assíncrono e painel administrativo com mapa em tempo real.

Inclui:

Backend assíncrono com FastAPI

Processamento de eventos com FastStream + RabbitMQ

Persistência com MongoDB

Saldos e cache com Redis

Dashboard moderno em HTML + JavaScript com Leaflet para visualização das rotas

📌 Arquitetura Geral
┌────────────┐      POST /corridas      ┌───────────────┐
│   Frontend │ ───────────────────────► │    FastAPI    │
└─────┬──────┘                          └────────┬──────┘
      │ Publica evento "corridas.finalizadas"    │
      │                                          ▼
      │                                   ┌───────────────┐
      │                                   │   RabbitMQ    │
      ▼                                   └───────┬───────┘
┌─────────────┐                               Consome evento
│   Leaflet   │                                via FastStream
│  Rotas/Mapa │                                   │
└──────┬──────┘                                   ▼
       │                          ┌──────────────────────────┐
       │                          │   Consumer FastStream    │
       │                          │ Atualiza saldo e grava   │
       │                          │ corrida no MongoDB       │
       │                          └─────────────┬────────────┘
       │                                        ▼
   Visualiza                         ┌──────────────────┐
   corridas, saldos                  │     MongoDB      │
   e rotas no mapa                   └──────────────────┘
                                          Persistência

                                         ┌──────────────┐
                                         │    Redis     │
                                         └──────────────┘
                                         Saldo por motorista

💻 Serviços
app

API feita com FastAPI

Publica eventos no RabbitMQ

Fornece os endpoints REST consumidos pelo front

consumer

Serviço FastStream escutando a fila corridas.finalizadas

Atualiza saldos no Redis

Salva corrida no MongoDB

mongo

Banco NoSQL contendo histórico de corridas

redis

Cache e armazenamento de saldos dos motoristas

rabbitmq

Broker de mensagens para comunicação assíncrona

🌐 Front-end (Dashboard)

O projeto agora inclui um painel em:

HTML + CSS + JavaScript

Leaflet para exibir:

mapa

rotas traçadas automaticamente

pontos de origem/destino

Formulário para cadastrar corridas

Lista de corridas filtrável

Tabela de saldos por motorista

✨ Funcionalidades do Front-end

✔ Traça rota automaticamente ao publicar a corrida
✔ Traça rota manual via atalho T
✔ Seleciona origem e destino clicando no mapa (O e D)
✔ Visualização completa das corridas cadastradas
✔ Atualização de saldos direto do Redis
✔ Filtros por forma de pagamento e motorista

O dashboard consome diretamente os endpoints FastAPI.

🔧 Variáveis de Ambiente

Arquivo .env:

MONGO_URL=mongodb://mongo:27017
MONGO_DB=transflow
MONGO_COLLECTION=corridas

REDIS_URL=redis://redis:6379

RABBIT_URL=amqp://guest:guest@rabbitmq:5672/
RABBIT_QUEUE=corridas.finalizadas

APP_HOST=0.0.0.0
APP_PORT=8000

🚀 Instalação e Execução

Requisitos:
🟢 Docker
🟢 Docker Compose

1️⃣ Subir todo o sistema
docker compose up --build -d

2️⃣ Acessos
Serviço	URL
FastAPI	http://localhost:8000/docs

Front-end (HTML estático)	abra o arquivo dashboard.html no navegador
RabbitMQ Management	http://localhost:15672
 (guest/guest)
MongoDB	Porta 27017
Redis	Porta 6379
🔄 Fluxo Completo
1. O front envia:
POST /corridas


Com:

id_corrida

origem

destino

motorista

pagamento

valor

etc.

2. O FastAPI publica o evento:
corridas.finalizadas

3. O consumer recebe o evento

E então:

atualiza saldo no Redis

salva corrida no MongoDB

4. O front acessa:

/corridas → lista todas

/corridas/{forma_pagamento} → filtra

/saldo/{motorista} → saldo atualizado

📡 Endpoints Disponíveis
POST /corridas

Publica evento e retorna OK.

GET /corridas

Lista todas as corridas do MongoDB.

GET /corridas/{forma_pagamento}

Filtra por tipo de pagamento (pix, dinheiro, cartão).

GET /saldo/{motorista}

Retorna saldo somado via Redis.

🧪 Teste Rápido
1️⃣ Publicar corrida:

POST http://localhost:8000/corridas

{
  "id_corrida": "ABC123",
  "passageiro_nome": "Fulano",
  "passageiro_telefone": "12345",
  "motorista_nome": "João",
  "motorista_nota": 4.9,
  "origem": "Maricá, RJ",
  "destino": "Niterói, RJ",
  "valor_corrida": 58.90,
  "forma_pagamento": "pix"
}

2️⃣ Listar corridas:

GET http://localhost:8000/corridas

3️⃣ Ver saldo:

GET http://localhost:8000/saldo/João

4️⃣ Ver no front

Abra a dashboard:

Go Live no VSCode


A rota aparecerá automaticamente no mapa.
