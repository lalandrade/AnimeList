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
    fetch("/animes", { credentials: "include" })
        .then(res => res.json())
        .then(animes => {
            const container = document.getElementById("anime-cards");
            container.innerHTML = "";

            if (animes.length === 0) {
                container.innerHTML = "<p>Nenhum anime cadastrado</p>";
                return;
            }

            animes.forEach(anime => {

                const card = document.createElement("div");
                card.className = "card";

                card.innerHTML = `
                    <img src="${anime.imagem}">

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

    const statusSelect = document.getElementById("status");

    const dados = {
        nome: document.getElementById("nome").value,
        descricao: document.getElementById("descricao").value,
        status: statusSelect.value,
        eps_assistidos: document.getElementById("eps_assistidos").value || 0,
        total_eps: document.getElementById("total_eps").value || 0,
        imagem: previewCapa.src || null
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
        alert("✅ Anime salvo com sucesso!");
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

            // 🔥 MOSTRAR IMAGEM NO EDITAR
            if (anime.imagem) {
                previewCapa.src = anime.imagem;
                previewCapa.style.display = "block";
                textoUpload.style.display = "none";
            }

            document.getElementById("formAnime").dataset.id = id;
            abrirModalAnime();
        });
}

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
        previewCapa.src = e.target.result;
        previewCapa.style.display = "block";
        textoUpload.style.display = "none";
    };
    reader.readAsDataURL(file);
}
