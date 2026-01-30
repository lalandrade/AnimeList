// ====================================
// VALIDAÇÃO E MÁSCARA DE CPF
// ====================================

const cpfInput = document.getElementById('cpf');
const erroCpf = document.getElementById('erro-cpf');
const form = document.getElementById('form-cadastro');

// Aplica máscara no CPF enquanto digita
cpfInput.addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, ''); // Remove tudo que não é número
    
    // Limita a 11 dígitos
    value = value.substring(0, 11);
    
    // Aplica a máscara 000.000.000-00
    if (value.length > 9) {
        value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    } else if (value.length > 6) {
        value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
    } else if (value.length > 3) {
        value = value.replace(/(\d{3})(\d{1,3})/, '$1.$2');
    }
    
    e.target.value = value;
    
    // VALIDAÇÃO EM TEMPO REAL
    const cpfSemMascara = value.replace(/\D/g, '');
    
    if (cpfSemMascara.length > 0 && cpfSemMascara.length < 11) {
        // CPF incompleto
        erroCpf.textContent = 'CPF incompleto. Digite os 11 dígitos.';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
    } else if (cpfSemMascara.length === 11) {
        // CPF completo - valida
        if (!validarCPF(cpfSemMascara)) {
            erroCpf.textContent = 'CPF inválido';
            erroCpf.style.color = '#f87171';
            cpfInput.style.borderColor = '#ef4444';
        } else {
            // CPF válido!
            erroCpf.textContent = '✓ CPF válido';
            erroCpf.style.color = '#86efac';
            cpfInput.style.borderColor = '#22c55e';
        }
    } else {
        // Campo vazio - limpa mensagens
        erroCpf.textContent = '';
        cpfInput.style.borderColor = '';
    }
});

// Validação quando sai do campo (blur)
cpfInput.addEventListener('blur', function() {
    const cpf = cpfInput.value.replace(/\D/g, '');
    
    if (cpf.length > 0 && cpf.length < 11) {
        erroCpf.textContent = 'CPF incompleto. Digite os 11 dígitos.';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
    }
});

// Valida CPF antes de enviar o formulário
form.addEventListener('submit', function(e) {
    const cpf = cpfInput.value.replace(/\D/g, ''); // Remove pontos e traço
    
    if (cpf.length === 0) {
        e.preventDefault();
        erroCpf.textContent = 'CPF é obrigatório';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
        cpfInput.focus();
        return false;
    }
    
    if (cpf.length !== 11) {
        e.preventDefault();
        erroCpf.textContent = 'CPF deve ter exatamente 11 dígitos';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
        cpfInput.focus();
        return false;
    }
    
    // Validação adicional: CPF válido (algoritmo oficial)
    if (!validarCPF(cpf)) {
        e.preventDefault();
        erroCpf.textContent = 'CPF inválido';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
        cpfInput.focus();
        return false;
    }
    
    // Limpa mensagem de erro se estiver tudo certo
    erroCpf.textContent = '';
    cpfInput.style.borderColor = '';
});

// Remove erro quando o usuário começa a digitar novamente
cpfInput.addEventListener('focus', function() {
    // Só limpa se o campo estiver vazio
    if (cpfInput.value.length === 0) {
        erroCpf.textContent = '';
        cpfInput.style.borderColor = '';
    }
});

// ====================================
// FUNÇÃO DE VALIDAÇÃO DE CPF (OFICIAL)
// ====================================
function validarCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    
    if (cpf.length !== 11) return false;
    
    // Verifica se todos os dígitos são iguais (ex: 111.111.111-11)
    if (/^(\d)\1{10}$/.test(cpf)) return false;
    
    // Validação do primeiro dígito verificador
    let soma = 0;
    for (let i = 0; i < 9; i++) {
        soma += parseInt(cpf.charAt(i)) * (10 - i);
    }
    let resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(9))) return false;
    
    // Validação do segundo dígito verificador
    soma = 0;
    for (let i = 0; i < 10; i++) {
        soma += parseInt(cpf.charAt(i)) * (11 - i);
    }
    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.charAt(10))) return false;
    
    return true;
}

//
//CPFs VÁLIDOS PARA TESTE:

//111.444.777-35
//123.456.789-09
//529.982.247-25
//853.513.468-93
//362.817.281-06
//191.726.485-17
//745.209.748-51
//401.231.654-02
//078.543.219-64
//987.654.321-00