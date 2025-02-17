# Softdesk API

Softdesk API est une application Django REST conçue pour gérer des projets, leurs tickets (issues), les commentaires et la gestion des contributeurs.  
Ce projet offre une API sécurisée par JWT et un modèle utilisateur customisé, permettant à chacun de gérer ses propres projets de manière simplifiée.

## Table des matières

- [Installation](#installation)
- [Configuration](#configuration)
- [Mise en route](#mise-en-route)
- [Structure de l'application](#structure-de-lapplication)
- [Contribuer](#contribuer)
- [Documentation Complète de l'API](#documentation-complète-de-lapi)

## Installation

1. **Cloner le dépôt**

   ```bash
   git clone <URL_DU_DEPOT>
   cd softdesk-api
   ```

2. **Créer un environnement virtuel**

   ```bash
   python -m venv venv
   # Sous Linux/MacOS :
   source venv/bin/activate
   # Sous Windows :
   venv\Scripts\activate
   ```

3. **Installer les dépendances**

   Le projet utilise [Poetry](https://python-poetry.org/) pour la gestion des dépendances. Pour installer celles-ci, exécutez :

   ```bash
   poetry install
   ```


## Configuration

1. **Variables d'environnement**  
   Créez un fichier `.env` à la racine du projet avec au moins :

   ```
   DJANGO_SECRET_KEY=your_secret_key_here
   DEBUG=True
   DATABASE_URL=sqlite:///db.sqlite3
   ```

2. **Configuration JWT**  
   La configuration JWT se trouve dans `softdesk/settings.py` et inclut notamment :
   - `ACCESS_TOKEN_LIFETIME` : 30 minutes
   - `REFRESH_TOKEN_LIFETIME` : 1 jour
   - `ROTATE_REFRESH_TOKENS` et `BLACKLIST_AFTER_ROTATION` activés
   - `AUTH_HEADER_TYPES` : « Bearer »

## Mise en route

1. **Effectuer les migrations**

   ```bash
   python manage.py migrate
   ```

2. **Créer un superutilisateur (facultatif)**

   ```bash
   python manage.py createsuperuser
   ```

3. **Lancer le serveur de développement**

   ```bash
   python manage.py runserver
   ```

   Vous pourrez accéder à l'administration Django via [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) et à l'API via [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

## Structure de l'application

Le projet est organisé en plusieurs applications :

- **users** : Gère l'authentification, l'inscription et l'ensemble des opérations liées aux utilisateurs via un modèle personnalisé.
- **api** : Gère les projets, les tickets (issues), les commentaires et la gestion des contributeurs.

## Documentation Complète de l'API

Pour la liste complète des endpoints ainsi que des exemples de corps de requête, reportez-vous au fichier [documentation_API.md](documentation_API.md).

---
