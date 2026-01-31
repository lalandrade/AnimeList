const cpfInput = document.getElementById('cpf');
const erroCpf = document.getElementById('erro-cpf');
const form = document.getElementById('form-cadastro');

// Máscara de CPF
cpfInput.addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, '');
    value = value.substring(0, 11);

    if (value.length > 9) {
        value = value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    } else if (value.length > 6) {
        value = value.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
    } else if (value.length > 3) {
        value = value.replace(/(\d{3})(\d{1,3})/, '$1.$2');
    }

    e.target.value = value;

    const cpfSemMascara = value.replace(/\D/g, '');

    // Feedback simples
    if (cpfSemMascara.length > 0 && cpfSemMascara.length < 11) {
        erroCpf.textContent = 'CPF incompleto';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
    } else if (cpfSemMascara.length === 11) {
        erroCpf.textContent = '✓ CPF OK';
        erroCpf.style.color = '#22c55e';
        cpfInput.style.borderColor = '#22c55e';
    } else {
        erroCpf.textContent = '';
        cpfInput.style.borderColor = '';
    }
});

// Validação ao enviar
form.addEventListener('submit', function (e) {
    const cpf = cpfInput.value.replace(/\D/g, '');

    if (cpf.length === 0) {
        e.preventDefault();
        erroCpf.textContent = 'CPF é obrigatório';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
        cpfInput.focus();
        return;
    }

    if (cpf.length !== 11) {
        e.preventDefault();
        erroCpf.textContent = 'CPF deve ter 11 dígitos';
        erroCpf.style.color = '#f87171';
        cpfInput.style.borderColor = '#ef4444';
        cpfInput.focus();
    }
});
