
# 🏦 Banco Python - API & Dashboard

Um sistema de simulação bancária full-stack desenvolvido para demonstrar práticas avançadas de desenvolvimento backend e integração fluida com o frontend. O projeto simula operações reais de uma conta bancária, garantindo a integridade dos dados durante transações simultâneas.

## 🚀 Principais Funcionalidades

* **Autenticação e Onboarding:** Criação de usuário e geração automática de conta bancária com saldo inicial.
* **Dashboard Dinâmico:** Interface stateless que captura e exibe dados (ID da conta, saldo em tempo real) automaticamente via token/sessão.
* **Transferências Seguras (PIX):** Sistema de transferência atômica entre contas.
* **Segurança e Concorrência:** Implementação de transações ACID e *row-level locking* (`with_for_update`) no banco de dados para evitar condições de corrida (race conditions) durante as transferências.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, FastAPI, SQLAlchemy (ORM)
* **Banco de Dados:** SQLite (com arquitetura pronta para migração para PostgreSQL)
* **Frontend:** HTML5, CSS3 (Variáveis, Flexbox/Grid), JavaScript (Fetch API)
