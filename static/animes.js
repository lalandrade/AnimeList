document.addEventListener("DOMContentLoaded", () => {
    carregarAnimes();

    document.getElementById("formAnime")
        .addEventListener("submit", salvarAnime);

    document.getElementById("inputCapa")
        .addEventListener("change", previewImagem);
});

/* =========================
   LISTAR
========================= */
function carregarAnimes() {
    fetch("/animes")
        .then(res => res.json())
        .then(animes => {
            const container = document.getElementById("anime-cards");
            container.innerHTML = "";

            if (animes.length === 0) {
                container.innerHTML = "<p>Nenhum anime cadastrado </p>";
                return;
            }

            animes.forEach(anime => {
                const card = document.createElement("div");
                card.className = "card";

                card.innerHTML = `
                    <img src="${anime.imagem || '/static/naruto.jpg'}">
                    <h4>${anime.nome}</h4>
                    <p>EP ${anime.eps_assistidos} / ${anime.total_eps}</p>

                    <div class="card-actions">
                        <button onclick="editarAnime(${anime.id})">✏️</button>
                        <button onclick="removerAnime(${anime.id})">🗑️</button>
                    </div>
                `;

                container.appendChild(card);
            });
        });
}

/* =========================
   SALVAR / EDITAR
========================= */
function salvarAnime(e) {
    e.preventDefault();

    const dados = {
        nome: nome.value,
        descricao: descricao.value,
        status: status.value,
        eps_assistidos: eps_assistidos.value || 0,
        total_eps: total_eps.value || 0,
        imagem: previewCapa.src || null
    };

    const form = document.getElementById("formAnime");
    const id = form.dataset.id;

    const url = id ? `/animes/${id}` : "/animes";
    const method = id ? "PUT" : "POST";

    fetch(url, {
        method: method,
        headers: {
            "Content-Type": "application/json"
        },
        credentials: "include",
        body: JSON.stringify(dados)
    })
    .then(res => {
        if (res.status === 401) {
            alert("⚠️ Você precisa fazer login para adicionar anime");
            throw new Error("Não autenticado");
        }

        if (!res.ok) {
            throw new Error("Erro ao salvar anime");
        }

        return res.json();
    })
    .then(() => {
        alert("✅ Anime salvo com sucesso!");
        fecharModalAnime();
        carregarAnimes();
    })
    .catch(err => {
        if (err.message !== "Não autenticado") {
            alert("❌ Erro ao salvar anime");
        }
    });
}


/* =========================
   EDITAR
========================= */
function editarAnime(id) {
    fetch(`/animes/${id}`)
        .then(res => res.json())
        .then(anime => {
            nome.value = anime.nome;
            descricao.value = anime.descricao;
            status.value = anime.status;
            eps_assistidos.value = anime.eps_assistidos;
            total_eps.value = anime.total_eps;

            if (anime.imagem) {
                previewCapa.src = anime.imagem;
                previewCapa.style.display = "block";
                textoUpload.style.display = "none";
            }

            document.getElementById("formAnime").dataset.id = id;
            abrirModalAnime();
        });
}

/* =========================
   REMOVER
========================= */
function removerAnime(id) {
    if (!confirm("Deseja remover este anime?")) return;

    fetch(`/animes/${id}`, { method: "DELETE" })
        .then(() => carregarAnimes());
}

/* =========================
   MODAL
========================= */
function abrirModalAnime() {
    modalAnime.style.display = "flex";
}

function fecharModalAnime() {
    modalAnime.style.display = "none";
    formAnime.reset();
    previewCapa.style.display = "none";
    textoUpload.style.display = "block";
}

/* =========================
   PREVIEW IMAGEM
========================= */
function previewImagem() {
    const file = this.files[0];
    if (!file) return;

    // 🔴 LIMITE DE 1MB
    if (file.size > 1024 * 1024) {
        alert("❌ Escolha uma imagem menor que 1MB");
        this.value = ""; // limpa o input
        return;
    }

    const reader = new FileReader();
    reader.onload = e => {
        previewCapa.src = e.target.result;
        previewCapa.style.display = "block";
        textoUpload.style.display = "none";
    };
    reader.readAsDataURL(file);
}

