
# 🏦 Banco Python - API & Dashboard

Um sistema de simulação bancária full-stack desenvolvido para demonstrar práticas avançadas de desenvolvimento backend e integração fluida com o frontend. O projeto simula operações reais de uma conta bancária, garantindo a integridade dos dados durante transações simultâneas, e está com sua infraestrutura totalmente hospedada em nuvem.

## 🚀 Principais Funcionalidades

* **Autenticação e Onboarding:** Sistema com telas separadas (Login e Cadastro), validação de formulários contra dados em branco e geração automática de conta bancária com saldo inicial.
* **Dashboard Dinâmico:** Interface stateless que captura e exibe dados (ID da conta, saldo em tempo real) perfeitamente integrados à API.
* **Transferências Seguras (PIX):** Sistema de transferência atômica entre contas ativas.
* **Segurança e Concorrência:** Implementação de transações ACID e *row-level locking* (`with_for_update`) no banco de dados para evitar condições de corrida (*race conditions*) durante transferências simultâneas.
* **Suporte Integrado:** Botão de ação flutuante (FAB) integrado com redirecionamento automático para atendimento via WhatsApp.

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, FastAPI, SQLAlchemy (ORM)
* **Banco de Dados:** PostgreSQL (Hospedado no Supabase, utilizando *Connection Pooling*)
* **Frontend:** HTML5, CSS3 (Variáveis, Flexbox/Grid), JavaScript (Fetch API)
* **Deploy / Hospedagem:** Render (API Backend) e Vercel (Páginas Frontend)
