let imagemAtual = null;

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
function carregarAnimes(status = null) {
    let url = "/animes";

    if (status) {
        url += `?status=${status}`;
    }

    fetch(url, { credentials: "include" })
        .then(res => res.json())
        .then(animes => {
            const container = document.getElementById("anime-cards");
            container.innerHTML = "";

            if (animes.length === 0) {
                container.innerHTML = "<p>Nenhum anime encontrado</p>";
                return;
            }

            animes.forEach(anime => {
                const card = document.createElement("div");
                card.className = "card";

                card.innerHTML = `
                    ${anime.imagem ? `<img src="${anime.imagem}">` : ""}

                    <span class="status-badge ${anime.status}">
                        ${formatarStatus(anime.status)}
                    </span>

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
        nome: document.getElementById("nome").value,
        descricao: document.getElementById("descricao").value,
        status: document.getElementById("status").value,
        eps_assistidos: document.getElementById("eps_assistidos").value || 0,
        total_eps: document.getElementById("total_eps").value || 0,
        imagem: imagemAtual // 🔥 mantém a imagem antiga se não trocar
    };

    const form = document.getElementById("formAnime");
    const id = form.dataset.id;

    const url = id ? `/animes/${id}` : "/animes";
    const method = id ? "PUT" : "POST";

    fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(dados)
    })
    .then(res => {
        if (!res.ok) throw new Error();
        return res.json();
    })
    .then(() => {
        fecharModalAnime();
        carregarAnimes();
    })
    .catch(() => alert("❌ Erro ao salvar anime"));
}

/* =========================
   EDITAR
========================= */
function editarAnime(id) {
    fetch(`/animes/${id}`)
        .then(res => res.json())
        .then(anime => {

            document.getElementById("nome").value = anime.nome;
            document.getElementById("descricao").value = anime.descricao;
            document.getElementById("status").value = anime.status;
            document.getElementById("eps_assistidos").value = anime.eps_assistidos;
            document.getElementById("total_eps").value = anime.total_eps;

            // 🔥 guarda imagem atual
            imagemAtual = anime.imagem;

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
   STATUS
========================= */
function formatarStatus(status) {
    if (status === "assistindo") return "📺 Assistindo";
    if (status === "concluidos") return "✅ Concluído";
    if (status === "favoritos") return "⭐ Favorito";
    return "";
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

    previewCapa.src = "";
    previewCapa.style.display = "none";
    textoUpload.style.display = "block";

    imagemAtual = null; // 🔥 limpa memória
    delete formAnime.dataset.id;
}

/* =========================
   PREVIEW IMAGEM
========================= */
function previewImagem() {
    const file = this.files[0];
    if (!file) return;

    if (file.size > 1024 * 1024) {
        alert("❌ Escolha uma imagem menor que 1MB");
        this.value = "";
        return;
    }

    const reader = new FileReader();
    reader.onload = e => {
        imagemAtual = e.target.result; // 🔥 atualiza imagem
        previewCapa.src = imagemAtual;
        previewCapa.style.display = "block";
        textoUpload.style.display = "none";
    };
    reader.readAsDataURL(file);
}
