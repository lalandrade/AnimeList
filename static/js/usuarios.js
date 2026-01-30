function preencherFormulario(botao) {
    const usuario = JSON.parse(botao.dataset.usuario);

    document.getElementById("id").value = usuario.id;
    document.getElementById("nome").value = usuario.nome;
    document.getElementById("email").value = usuario.email;
    document.getElementById("idade").value = usuario.idade;
}

/* EXCLUIR */
function excluirUsuario(id) {
    if (!confirm("Deseja excluir este usuário?")) return;

    fetch(`/usuarios/${id}`, {
        method: "DELETE"
    })
    .then(() => {
        document.getElementById(`linha-${id}`).remove();
    });
}

/* ATUALIZAR */
document.getElementById("form-atualizar-usuario").addEventListener("submit", function (e) {
    e.preventDefault();

    const id = document.getElementById("id").value; // 🔥 AQUI

    const dados = {
        id: id,
        nome: document.getElementById("nome").value,
        email: document.getElementById("email").value,
        idade: document.getElementById("idade").value
    };

    fetch(`/usuarios/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dados)
    })
    .then(res => res.json())
    .then(resposta => {
        alert(resposta.mensagem || resposta.erro);
        location.reload();
    })
    .catch(() => {
        alert("Erro ao atualizar usuário");
    });
});




