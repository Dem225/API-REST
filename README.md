# API REST

API FastAPI + SQLAlchemy (async) avec PostgreSQL / Neon.

## Démarrage

1. Copie `.env.example` vers `.env` :

   ```powershell
   Copy-Item .env.example .env
   ```

2. Remplis les deux variables dans `.env` :
   - `SQLALCHEMY_DATABASE_URL` : chaîne de connexion fournie par Neon (avec le mot de passe à jour).
   - `JWT_SECRET_KEY` : clé aléatoire générée avec
     `python -c "import secrets; print(secrets.token_urlsafe(48))"`.

3. Installe les dépendances et lance le serveur :

   ```powershell
   uv sync
   uv run fastapi run main.py --host 0.0.0.0
   ```

## Docker

```powershell
docker build -t api-rest .
docker run --env-file .env -p 8000:8000 api-rest
```

## Sécurité

- `.env` est ignoré par Git **et** par Docker (`.dockerignore`) : ne jamais le committer.
- Ne réutilise jamais une clé ou un mot de passe ayant été exposé : révoque-le d'abord.
- En production (FastAPI Cloud), renseigne les mêmes variables dans *Settings → Environment variables*.
