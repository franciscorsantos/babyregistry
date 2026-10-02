# 👶 Mathias Filipe - Lista de Presentes & Chá de Bebê Virtual

Bem-vindo à documentação oficial do **Bebê Registry (Mathias Filipe)**!  
Este projeto é uma aplicação web completa desenvolvida com **Python (Flask)**, **SQLAlchemy**, **SQLite**, **Tailwind CSS** e **Mercado Pago (Pix Dinâmico)**, projetada para permitir que convidados presenteiem o bebê, contribuam via vaquinha/cotas e enviem recados de carinho.

---

## 🚀 Funcionalidades Principais

- **🎁 Vitrine Virtual de Presentes**:
  - Exibição em grade elegante (estilo minimalista *warm editorial*).
  - Filtro interativo de itens por categoria (*Passeio, Quarto, Roupas, Alimentação, Higiene, Brinquedos*).
  - Badges de destaque (*Must Have*) e marcação visual de itens 100% presenteados.

- **📊 Vaquinha / Presentes Coletivos (Cotas)**:
  - Múltiplos convidados podem contribuir financeiramente para o mesmo presente de maior valor.
  - Barra de progresso visual em tempo real (% arrecadado, valor acumulado e valor restante).
  - Modal com seleção rápida de cotas (*Restante Total, R$ 50, R$ 100, R$ 200...*) ou valor customizado.

- **⚡ Checkout Transparente via Pix (Mercado Pago)**:
  - Geração instantânea do QR Code Pix oficial e do código *Pix Copia e Cola*.
  - Integração com o SDK oficial do Mercado Pago (`mercadopago`).
  - Fallback automático para modo de demonstração local em ambiente de dev.

- **🔔 Notificação de Pagamento (Webhook & Simulação)**:
  - Atualização em tempo real do status de pagamento (`pending` ➔ `approved`).
  - Atualização automática do status do produto para `presenteado` quando a meta atinge 100%.
  - Endpoint auxiliar de simulação de pagamento para testes imediatos.

- **💌 Mural de Recados de Carinho**:
  - Exibição de mensagens enviadas durante a compra de presentes.
  - Botão Flutuante (*Floating Action Button - FAB*) para envio de recados avulsos.

- **🧾 Recibo / Confirmação Virtual**:
  - Tela de confirmação com QR Code do recibo, resumo da contribuição e mensagem registrada.

---

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.x, Flask, Flask-SQLAlchemy, python-dotenv.
- **Integração de Pagamento**: Mercado Pago SDK (`mercadopago`), `qrcode`, `Pillow`.
- **Banco de Dados**: SQLite3 (gerenciado via SQLAlchemy ORM).
- **Frontend**: HTML5, Jinja2 Templates, Tailwind CSS (via CDN), Vanilla JavaScript.
- **Fontes & Design**: Google Fonts (*Literata* e *Inter*), paleta de cores *Sage* (`#475949`), *Terracotta* (`#7d562d`) e *Offwhite* (`#fbf9f4`).

---

## 📁 Estrutura do Projeto

```text
mfilipe/
│
├── app.py              # Aplicação principal Flask, rotas web, checkout API e webhook
├── config.py           # Configurações do sistema e leitura de variáveis de ambiente
├── models.py           # Modelos ORM (Item, Presente) e propriedades da vaquinha
├── seed.py             # Script de povoamento inicial do banco de dados
├── test_app.py         # Suíte de testes automatizados completa
├── requirements.txt    # Lista de dependências Python
├── .env                # Arquivo de credenciais e variáveis de ambiente
│
├── templates/          # Templates Jinja2
│   ├── base.html       # Layout base, header, footer e inclusão de scripts
│   ├── index.html      # Vitrine de presentes, cards, barra de progresso e modal checkout
│   ├── mural.html      # Mural de recados e modal FAB
│   └── confirmacao.html# Recibo e confirmação do presente
│
└── static/             # Arquivos estáticos
    ├── css/
    │   └── custom.css  # Estilos customizados e regras de acessibilidade
    └── js/
        └── main.js     # Lógica JavaScript do modal, cotas, Pix e toast notifications
```

---

## ⚙️ Configuração e Instalação

### 1. Pré-requisitos
- Python 3.10 ou superior instalado.
- Gerenciador de pacotes `pip`.

### 2. Clonar ou Acessar a Pasta do Projeto
```bash
cd c:\Users\Francisco R Santos\Documents\projetos_web\mfilipe
```

### 3. Criar e Ativar o Ambiente Virtual (`venv`)
```bash
# No Windows (PowerShell):
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 4. Instalar as Dependências
```bash
pip install -r requirements.txt
```

---

## 🗝️ Configuração do Arquivo `.env`

Crie ou edite o arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SECRET_KEY=sua_chave_secreta_aqui
MERCADO_PAGO_ACCESS_TOKEN=APP_USR-seu-access-token-do-mercado-pago
WEBHOOK_URL=https://seu-dominio.com/webhook
```

> **Nota para Testes Locais com Mercado Pago**:  
> Se estiver rodando localmente (`localhost`), use o **ngrok** para expor a porta `5000`:
> ```bash
> ngrok http 5000
> ```
> Copie a URL HTTPS gerada (ex: `https://xxxx.ngrok-free.dev/webhook`) e defina na variável `WEBHOOK_URL`.

---

## 🏃 Executando a Aplicação

### 1. Inicializar o Banco de Dados e Servidor
```bash
python app.py
```
A aplicação estará acessível em **`http://127.0.0.1:5000`**.  
*O banco de dados SQLite (`bebe_registry.db`) será criado e populado automaticamente na primeira execução via `seed.py`.*

---

## 🧪 Executando os Testes Automatizados

O projeto conta com uma suíte de testes em `test_app.py` que testa o fluxo completo de vitrine, checkout com contribuição parcial (vaquinha), acúmulo de metas e mural.

Para executar os testes:
```bash
python test_app.py
```

### Resultado Esperado:
```text
SDK do Mercado Pago inicializado com sucesso.
Itens cadastrados com sucesso!
--- 1. Testando Rota Principal (Vitrine /) ---
[OK] Rota principal (/) funcionando!

--- 2. Testando Rota do Mural de Recados (/mural) ---
[OK] Rota /mural funcionando!

--- 3. Testando API de Checkout com Contribuição Parcial (Vaquinha) ---
[OK] Cota 1 de R$ 27.50 aprovada! Progresso: 50% (Restam R$ 27.50)
[OK] Cota 2 aprovada! Item atingiu 100% e atualizou status para 'presenteado'!

--- 4. Testando Rota de Confirmação (/confirmacao/<id>) ---
[OK] Tela de confirmação/recibo gerada perfeitamente!

--- 5. Testando Envio de Recado Avulso no Mural (/api/mural/mensagem) ---
[OK] Recado avulso adicionado com sucesso!

SUCESSO: TODOS OS TESTES DA VAQUINHA / COTAS PASSARAM COM SUCESSO ABSOLUTO!
```

---

## 📌 Principais Endpoints da API

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/` | Vitrine de presentes com filtro por categoria |
| `GET` | `/mural` | Exibição das mensagens aprovadas do mural |
| `GET` | `/confirmacao/<presente_id>` | Recibo do presente / mensagem de confirmação |
| `POST` | `/api/checkout/<item_id>` | Cria presente pendente, calcula cota e gera Pix MP |
| `POST` | `/api/simulate-payment/<presente_id>` | Simula a aprovação imediata do pagamento |
| `POST` | `/api/mural/mensagem` | Adiciona um recado avulso via modal FAB |
| `POST` | `/webhook` | Recebe notificações de status de pagamento do Mercado Pago |

---

## 📄 Licença
Este projeto foi desenvolvido com amor para o Chá de Bebê do **Mathias Filipe** (2026). Todos os direitos reservados.
