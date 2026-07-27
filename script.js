/* ================= JavaScript (Integração com FastAPI) ================= */
const API_URL = "http://127.0.0.1:8000";

function showMsg(elementId, text, isError = false) {
    const el = document.getElementById(elementId);
    el.style.display = 'block';
    el.textContent = text;
    el.className = isError ? 'alert error' : 'alert success';
    setTimeout(() => el.style.display = 'none', 5000);
}

// Rota: Função local de Logout (Sair)
function logout() {
    // 1. Esconde o painel (dashboard) e mostra a tela de login
    document.getElementById('dashboard-section').style.display = 'none';
    document.getElementById('auth-section').style.display = 'block';
    
    // 2. Limpa os campos de digitação
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
    document.getElementById('titular-nome').value = '';
    
    // 3. Limpa todas as mensagens de alerta que ficaram na tela
    document.getElementById('auth-msg').style.display = 'none';
    document.getElementById('conta-msg').style.display = 'none';
    document.getElementById('saldo-msg').style.display = 'none';
    document.getElementById('transf-msg').style.display = 'none';
}

// Rota: POST /usuarios/
async function registrar() {
    const nome = document.getElementById('username').value;
    const senha = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/usuarios/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, senha })
        });
        const data = await response.json();
        
        if (response.ok) {
            showMsg('auth-msg', 'Conta bancária e acesso criados com sucesso! Agora faça login.');
        } else {
            showMsg('auth-msg', data.detail, true);
        }
    } catch (error) {
        showMsg('auth-msg', 'Erro de conexão com o servidor.', true);
    }
}

// Rota: POST /login/
async function login() {
    const nome = document.getElementById('username').value;
    const senha = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_URL}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome, senha })
        });
        const data = await response.json();

        if (response.ok) {
            // 1. Esconde a tela de login e mostra o painel
            document.getElementById('auth-section').style.display = 'none';
            document.getElementById('dashboard-section').style.display = 'grid';

            // 2. Preenche o Cabeçalho com o nome
            document.getElementById('nome-usuario-logado').textContent = nome;
            
            // 3. Preenche a tela com os dados vindos do backend
            document.getElementById('numero-conta-texto').textContent = data.conta_id;
            
            // Transforma o número em formato de dinheiro (duas casas decimais)
            document.getElementById('valor-saldo-texto').textContent = parseFloat(data.saldo).toFixed(2);

        } else {
            showMsg('auth-msg', data.detail, true);
        }
    } catch (error) {
        showMsg('auth-msg', 'Erro de conexão com o servidor.', true);
    }
}

// Rota: POST /contas/
async function criarConta() {
    const nome_titular = document.getElementById('titular-nome').value;
    const saldo = parseFloat(document.getElementById('titular-saldo').value);

    try {
        const response = await fetch(`${API_URL}/contas/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nome_titular, saldo })
        });
        const data = await response.json();
        if (response.ok) showMsg('conta-msg', `Conta criada! ID: ${data.id}`);
        else showMsg('conta-msg', 'Erro ao criar conta', true);
    } catch (error) {
        showMsg('conta-msg', 'Erro de conexão.', true);
    }
}

// Rota: GET /contas/{id}/saldo
async function consultarSaldo() {
    const id = document.getElementById('consulta-id').value;

    try {
        const response = await fetch(`${API_URL}/contas/${id}/saldo`);
        const data = await response.json();
        if (response.ok) showMsg('saldo-msg', `${data.nome_titular} - Saldo: R$ ${data.saldo}`);
        else showMsg('saldo-msg', data.detail, true);
    } catch (error) {
        showMsg('saldo-msg', 'Erro de conexão.', true);
    }
}

// Rota: POST /transferencias/
async function transferir() {
    // Pega o ID da origem automaticamente do texto que está no painel (inserido no momento do login)
    const conta_origem_id = parseInt(document.getElementById('numero-conta-texto').textContent);
    
    const conta_destino_id = parseInt(document.getElementById('transf-destino').value);
    const valor = parseFloat(document.getElementById('transf-valor').value);

    // Validação básica de tela
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
            
            // Limpa os campos após o sucesso
            document.getElementById('transf-destino').value = '';
            document.getElementById('transf-valor').value = '';
            
            // Opcional: Atualizar o saldo na tela subtraindo o valor transferido
            const saldoAtual = parseFloat(document.getElementById('valor-saldo-texto').textContent);
            document.getElementById('valor-saldo-texto').textContent = (saldoAtual - valor).toFixed(2);
            
        } else {
            showMsg('transf-msg', data.detail, true);
        }
    } catch (error) {
        showMsg('transf-msg', 'Erro de conexão.', true);
    }
}