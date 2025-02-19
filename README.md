# Movie Mate

## Descrição
Movie Mate é uma API REST para recomendação de filmes baseada nas avaliações dos usuários. Os usuários podem adicionar filmes, avaliá-los e receber recomendações com base em suas preferências.

## Tecnologias Utilizadas
- Python
- Django
- Django REST Framework (DRF)
- SQLite (pode ser substituído por outro banco de dados)

## Como Rodar o Projeto

### Pré-requisitos
- Python 3.8+
- Virtualenv ou venv
- Django e DRF instalados

### Passos

1. Clone o repositório:
```sh
git clone https://github.com/seuusuario/movie-mate.git
cd movie-mate
```

2. Crie e ative um ambiente virtual:
```sh
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```sh
pip install -r requirements.txt
```

4. Execute as migrações do banco de dados:
```sh
python manage.py migrate
```

5. Crie um superusuário (opcional para testar no admin):
```sh
python manage.py createsuperuser
```

6. Inicie o servidor:
```sh
python manage.py runserver
```

7. Acesse a API em `http://127.0.0.1:8000/api/`

## Endpoints Principais

### Filmes (`/api/movies/`)
- `GET /api/movies/` - Lista todos os filmes
- `POST /api/movies/` - Adiciona um novo filme (requer autenticação)
- `GET /api/movies/{id}/` - Obtém detalhes de um filme específico
- `POST /api/movies/{id}/rate_movie/` - Avalia um filme (nota de 1 a 5)

### Avaliações (`/api/ratings/`)
- `GET /api/ratings/` - Lista todas as avaliações
- `POST /api/ratings/` - Adiciona uma nova avaliação

### Recomendações (`/api/movies/recommendations/`)
- `GET /api/movies/recommendations/` - Retorna filmes recomendados com base nas avaliações do usuário

## Autenticação
- Para criar e avaliar filmes, o usuário deve estar autenticado.
- A autenticação é feita via Django User Model (padrão do Django REST Framework).

## Contribuição
Sinta-se à vontade para contribuir enviando pull requests e abrindo issues no GitHub.

## Licença
Este projeto está sob a licença MIT.

