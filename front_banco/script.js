/* ================= JavaScript (Integração com FastAPI) ================= */
const API_URL = "https://digital-banking-simulation-back-banco.onrender.com";

function showMsg(elementId, text, isError = false) {
    const el = document.getElementById(elementId);
    if (!el) return; // Evita erro se o elemento não existir na página atual
    el.style.display = 'block';
    el.textContent = text;
    el.className = isError ? 'alert error' : 'alert success';
    setTimeout(() => el.style.display = 'none', 5000);
}

// Rota: Função local de Logout (Sair)
function logout() {
    document.getElementById('dashboard-section').style.display = 'none';
    document.getElementById('login-section').style.display = 'block';
    
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    
    const transfMsg = document.getElementById('transf-msg');
    if (transfMsg) transfMsg.style.display = 'none';
}

// Rota: POST /usuarios/ (Cadastro)
async function registrar() {
    const nome = document.getElementById('reg-username').value.trim();
    const senha = document.getElementById('reg-password').value.trim();

    if (!nome || !senha) {
        showMsg('reg-msg', 'Preencha todos os campos. Espaços vazios não são aceitos.', true);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/usuarios/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, senha })
        });
        const data = await response.json();
        
        if (response.ok) {
            showMsg('reg-msg', 'Conta criada com sucesso! Redirecionando para login...');
            // Aguarda 2 segundos e redireciona o usuário para a página inicial (index.html)
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        } else {
            showMsg('reg-msg', data.detail, true);
        }
    } catch (error) {
        showMsg('reg-msg', 'Erro de conexão com o servidor.', true);
    }
}

// Rota: POST /login/
async function login() {
    const nome = document.getElementById('username').value.trim();
    const senha = document.getElementById('password').value.trim();

    if (!nome || !senha) {
        showMsg('login-msg', 'Informe usuário e senha.', true);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, senha })
        });
        const data = await response.json();

        if (response.ok) {
            // Esconde Login e Mostra Dashboard
            document.getElementById('login-section').style.display = 'none';
            document.getElementById('dashboard-section').style.display = 'grid';

            // Preenche dados do Dashboard
            document.getElementById('nome-usuario-logado').textContent = nome;
            document.getElementById('numero-conta-texto').textContent = data.conta_id;
            document.getElementById('valor-saldo-texto').textContent = parseFloat(data.saldo).toFixed(2);
        } else {
            showMsg('login-msg', data.detail, true);
        }
    } catch (error) {
        showMsg('login-msg', 'Erro de conexão com o servidor.', true);
    }
}

// Rota: POST /transferencias/
async function transferir() {
    const conta_origem_id = parseInt(document.getElementById('numero-conta-texto').textContent);
    const conta_destino_id = parseInt(document.getElementById('transf-destino').value);
    const valor = parseFloat(document.getElementById('transf-valor').value);

    if (isNaN(conta_origem_id) || isNaN(conta_destino_id) || isNaN(valor) || valor <= 0) {
        showMsg('transf-msg', 'Preencha os campos de destino e valor corretamente.', true);
        return;
    }

    if (conta_origem_id === conta_destino_id) {
        showMsg('transf-msg', 'Você não pode transferir para a própria conta.', true);
        return;
    }

    try {
        const response = await fetch(`${API_URL}/transferencias/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ conta_origem_id, conta_destino_id, valor })
        });
        const data = await response.json();
        
        if (response.ok) {
            showMsg('transf-msg', data.mensagem);
            
            document.getElementById('transf-destino').value = '';
            document.getElementById('transf-valor').value = '';
            
            const saldoAtual = parseFloat(document.getElementById('valor-saldo-texto').textContent);
            document.getElementById('valor-saldo-texto').textContent = (saldoAtual - valor).toFixed(2);
            
        } else {
            showMsg('transf-msg', data.detail, true);
        }
    } catch (error) {
        showMsg('transf-msg', 'Erro de conexão.', true);
    }
}