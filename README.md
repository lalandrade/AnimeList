O **AnimeList** é uma aplicação web desenvolvida com **Flask** e **MySQL** que permite aos usuários organizar e gerenciar uma lista de animes de forma simples e prática.

## Para que serve o AnimeList?
O sistema serve para que o usuário possa:
- Cadastrar uma conta e fazer login
- Acessar um painel inicial
- Organizar animes nas categorias:
  - Assistindo
  - Concluídos
  - Favoritos
- Controlar seu perfil dentro do sistema

Além disso, o sistema possui uma **área administrativa**, onde usuários com perfil **admin** podem:
- Visualizar todos os usuários cadastrados
- Editar dados dos usuários (exceto CPF)
- Excluir usuários do sistema

## Tecnologias utilizadas
- Python (Flask)
- MySQL
- HTML, CSS e JavaScript
- bcrypt (criptografia de senhas)

## Como executar o projeto
1. Instale as dependências:
```bash
pip install -r requirements.txt
