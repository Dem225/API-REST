# API REST — documentation du projet

API FastAPI + SQLAlchemy (async) + PostgreSQL (Neon), avec authentification JWT.

---

## 1. Présentation

| Élément | Détail |
|---|---|
| Framework | FastAPI |
| Base de données | PostgreSQL sur Neon |
| ORM | SQLAlchemy (moteur asynchrone, driver `asyncpg`) |
| Authentification | OAuth2 + tokens JWT signés (HS256) |
| Hachage des mots de passe | bcrypt (passlib) |
| Gestion des dépendances | `uv` (`pyproject.toml`, `uv.lock`) |
| Déploiement | Docker et FastAPI Cloud (via GitHub) |

---

## 2. Structure du dépôt

```
.
├── main.py               # Application FastAPI + startup (création des tables)
├── jwt.py                # Création / vérification des tokens JWT
├── db/database.py        # Moteur SQLAlchemy async, session, init_db()
├── model/                # Modèles SQLAlchemy (user.py, task.py)
├── schemas/              # Schémas Pydantic (validation des requêtes)
├── routes/               # Routeurs FastAPI (auth.py, Task.py)
├── services/             # Logique métier (auth.py, Task.py, dependance.py)
├── src/api_rest/         # Paquet Python du projet
├── exercices/            # Supports de cours Docker
├── .env.example          # Modèle de configuration (sans secrets)
├── .gitignore            # Exclut .env, dumps, clés, etc.
├── .dockerignore         # Exclut .env et .git du build Docker
├── Dockerfile            # Image de l'API
├── compose.yaml          # Notes Docker Compose
├── pyproject.toml        # Dépendances et métadonnées
└── redmin.md             # Ce fichier
```

---

## 3. Installation et démarrage en local

### 3.1 Configuration

```powershell
Copy-Item .env.example .env
```

Remplir les deux variables dans `.env` :

```dotenv
SQLALCHEMY_DATABASE_URL="postgresql://UTILISATEUR:MOT_DE_PASSE@HOTE:5432/BASE"
JWT_SECRET_KEY="cle-aleatoire-longue"
```

- `SQLALCHEMY_DATABASE_URL` : chaîne fournie par Neon. Le code force automatiquement le driver `asyncpg` et normalise les paramètres SSL (`sslmode`, `channel_binding`). Tu peux donc coller l'URL telle quelle.
- `JWT_SECRET_KEY` : génère une nouvelle clé avec :

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

### 3.2 Lancement

```powershell
uv sync
uv run fastapi run main.py --host 0.0.0.0
```

Documentation interactive : http://127.0.0.1:8000/docs

### 3.3 Test rapide de la base

```powershell
uv run python -c "import asyncio; from sqlalchemy import text; from db.database import engine; async def m():
    async with engine.connect() as c: print((await c.execute(text('SELECT 1'))).scalar_one())
asyncio.run(m())"
```

---

## 4. Docker

```powershell
docker build -t api-rest .
docker run --env-file .env -p 8000:8000 api-rest
```

`.dockerignore` garantit que `.env` et `.git` ne rentrent pas dans l'image.

---

## 5. Endpoints principaux

| Méthode | Route | Description |
|---|---|---|
| `POST` | `/auth/inscriptions` | Créer un utilisateur |
| `POST` | `/auth/connexion` | Obtenir un token JWT (OAuth2 password) |
| — | `/tasks/...` | CRUD des tâches (voir `routes/Task.py`) |
| `GET` | `/docs` | Documentation Swagger |

Les routes protégées utilisent `OAuth2PasswordBearer` et `services/dependance.py` pour décoder le token.

---

## 6. Sécurité

- **Ne jamais committer `.env`** : il est exclu par `.gitignore` et `.dockerignore`.
- Les secrets ne sont pas dans le code : `jwt.py` et `db/database.py` lisent les variables d'environnement et lèvent une erreur explicite si elles manquent.
- Si un secret a déjà été exposé : **le révoquer / le rotationner d'abord**. Retirer le fichier de Git ne suffit pas.
- L'historique Git a été réécrit pour supprimer l'ancien `.env` et l'ancienne clé JWT. Les collaborateurs doivent re-cloner le dépôt.
- Activer sur GitHub : *Settings → Code security and analysis → Secret scanning / Push protection*.

---

## 7. Déploiement FastAPI Cloud

Le déploiement est déclenché automatiquement par un push sur `main`.

1. Dashboard → app `api-rest` → **Environment Variables**.
2. Ajouter `SQLALCHEMY_DATABASE_URL` et `JWT_SECRET_KEY`, avec l'interrupteur **Secret** activé.
3. Bouton **Save and Redeploy**.

L'option **Import** permet de coller directement le contenu du `.env` (les guillemets sont retirés automatiquement).

En cas d'échec du contrôle GitHub :

- Ouvrir le check → **Details** → onglets **Build** et **Runtime**.
- Vérifier que les deux variables existent et que la base est accessible.
- Vérifier les logs de démarrage (`Application startup complete`, erreurs d'import, etc.).

CLI (après `uv run fastapi cloud login`) :

```powershell
uv run fastapi cloud env list
uv run fastapi cloud logs --no-follow --tail 50
```

---

## 8. Dépannage courant

| Symptôme | Cause probable | Solution |
|---|---|---|
| `RuntimeError: SQLALCHEMY_DATABASE_URL n'est pas défini` | Variable absente | Ajouter la variable dans `.env` ou le dashboard |
| `RuntimeError: JWT_SECRET_KEY n'est pas défini` | Variable absente | Générer une clé et l'ajouter |
| `InvalidPasswordError` | Mot de passe Neon obsolète | Réinitialiser le mot de passe et mettre à jour la variable |
| `connect() got an unexpected keyword argument 'sslmode'` | URL Neon non normalisée | Mise à jour déjà incluse dans `db/database.py` |
| `The asyncio extension requires an async driver` | URL en `postgresql://` | Le code force `postgresql+asyncpg` automatiquement |
| Démarrage ok mais tables absentes | `init_db()` a échoué (veille Neon) | Vérifier les logs ; l'API redémarre et réessaie |

---

## 9. Historique des corrections de sécurité

- Retrait de `.env` de l'index Git et de tout l'historique.
- Remplacement de l'ancienne clé JWT en dur par une variable d'environnement.
- Ajout de `.gitignore`, `.dockerignore` et `.env.example`.
- Normalisation de l'URL Neon pour `asyncpg` et tolérance aux valeurs entre guillemets.
- Démarrage non bloquant si la base est momentanément indisponible.
