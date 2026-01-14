document.addEventListener("DOMContentLoaded", () => {
    carregarAnimes();
});

/* =========================
   LISTAR ANIMES
========================= */
function carregarAnimes() {
    fetch("/animes")
        .then(res => res.json())
        .then(animes => {
            const container = document.getElementById("anime-cards");
            container.innerHTML = "";

            if (animes.length === 0) {
                container.innerHTML = "<p>Nenhum anime cadastrado 😢</p>";
                return;
            }

            animes.forEach(anime => {
                const card = document.createElement("div");
                card.className = "card";

                card.innerHTML = `
                    <img src="${anime.imagem || '/static/placeholder.jpg'}">
                    <h4>${anime.nome}</h4>
                    <p>EP ${anime.eps_assistidos} / ${anime.total_eps}</p>
                `;

                container.appendChild(card);
            });
        });
}

/* =========================
   MODAL
========================= */
function abrirModalAnime() {
    document.getElementById("modalAnime").style.display = "flex";
}

function fecharModalAnime() {
    document.getElementById("modalAnime").style.display = "none";
    window.location.href = "/painel";
}

/* =========================
   SALVAR ANIME
========================= */
document.getElementById("formAnime").addEventListener("submit", function (e) {
    e.preventDefault();

    const dados = {
        nome: document.getElementById("nome").value,
        descricao: document.getElementById("descricao").value,
        status: document.getElementById("status").value,
        eps_assistidos: document.getElementById("eps_assistidos").value,
        total_eps: document.getElementById("total_eps").value,
        imagem: document.getElementById("previewCapa").src
    };

    fetch("/animes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados)
    })
    .then(res => res.json())
    .then(() => {
        alert("Anime salvo com sucesso!");
        window.location.href = "/painel";
    });
});

/* =========================
   PREVIEW DA IMAGEM
========================= */
document.getElementById("inputCapa").addEventListener("change", function () {
    const file = this.files[0];
    const preview = document.getElementById("previewCapa");
    const texto = document.getElementById("textoUpload");

    if (file) {
        const reader = new FileReader();
        reader.onload = e => {
            preview.src = e.target.result;
            preview.style.display = "block";
            texto.style.display = "none";
        };
        reader.readAsDataURL(file);
    }
});
function fecharModalAnime() {
    // fecha o modal
    document.getElementById("modalAnime").style.display = "none";

    // volta para o painel
    window.location.href = "/painel.html";
}

