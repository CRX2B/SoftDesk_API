# Softdesk API

Softdesk API est une application Django REST conçue pour gérer des projets, leurs tickets (issues), les commentaires et la gestion des contributeurs. Le projet utilise une authentification sécurisée via JWT (djangorestframework-simplejwt) et dispose d'un modèle utilisateur personnalisé respectant les exigences RGPD.

## Table des matières

- [Installation](#installation)
- [Configuration](#configuration)
- [Mise en route](#mise-en-route)
- [Structure de l'application](#structure-de-lapplication)
- [Endpoints de l'API](#endpoints-de-lapi)
  - [Authentification et Utilisateurs](#authentification-et-utilisateurs)
  - [Projets](#projets)
  - [Issues](#issues)
  - [Commentaires](#commentaires)
  - [Contributeurs](#contributeurs)
- [Tests et Collection Postman](#tests-et-collection-postman)
- [Technologies](#technologies)
- [Contribuer](#contribuer)
- [Licence](#licence)

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

   *Sinon*, si un fichier `requirements.txt` est fourni, vous pouvez faire :

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

- **Variables d'environnement**  
  Créez un fichier `.env` à la racine du projet avec au minimum le contenu suivant :

  ```
  DJANGO_SECRET_KEY=your_secret_key_here
  DEBUG=True
  DATABASE_URL=sqlite:///db.sqlite3
  ```

  Les variables de configuration indispensables sont :
  - `SECRET_KEY` : clé secrète pour Django.
  - `DEBUG` : active (True) ou désactive (False) le mode debug.
  - `DATABASE_URL` : URL de connexion à la base de données (par défaut SQLite est utilisé).

- **Configuration JWT**  
  Dans `softdesk/settings.py`, la configuration JWT est définie ainsi :
  - `ACCESS_TOKEN_LIFETIME` : 30 minutes
  - `REFRESH_TOKEN_LIFETIME` : 1 jour
  - `ROTATE_REFRESH_TOKENS` et `BLACKLIST_AFTER_ROTATION` sont activés.
  - `AUTH_HEADER_TYPES` : « Bearer »

- **Modèle Utilisateur Personnalisé**  
  Le modèle défini dans `users/models.py` inclut les champs suivants :  
  - `birth_date` (obligatoire pour les utilisateurs non administrateurs, validé pour avoir au moins 15 ans)  
  - `consent`, `can_be_contacted`, `can_data_be_shared`  
  - D'autres champs standards (username, email, password, etc.)

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

   Vous pouvez accéder à l'administration Django via [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) et à l'API via [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/).

## Structure de l'application

Le projet est organisé en plusieurs applications :

- **users** : Gère l'authentification, l'inscription, et les opérations liées aux utilisateurs via un modèle personnalisé.
  - Endpoints gérés par `UserViewSet` dans `users/views.py`.
  - Sérialisation via `UserSerializer` dans `users/serializers.py`.

- **projects** : Gère les projets, les issues (tickets), les commentaires et la gestion des contributeurs.
  - `ProjectViewSet` : Création, consultation, modification et suppression des projets.
  - `IssueViewSet` : Gestion des tickets liés à un projet.
  - `CommentViewSet` : Gestion des commentaires sur les tickets.
  - `ContributorViewSet` : Gestion des contributeurs d'un projet.
  - Permissions personnalisées dans `projects/permissions.py` (ex. IsAuthorOrReadOnly, IsProjectAuthor).

- **api** : Regroupe les endpoints (via routeurs DRF) pour exposer l'API complète de Softdesk.

## Endpoints de l'API

### Authentification et Utilisateurs

- **Inscription (Register)**
  - **POST** `/api/users/register/`  
    Corps de la requête (JSON) :

    ```json
    {
      "username": "nouvel_utilisateur",
      "email": "nouvel_utilisateur@example.com",
      "password": "motdepasse123",
      "birth_date": "2000-01-01",
      "consent": true,
      "can_be_contacted": false,
      "can_data_be_shared": false
    }
    ```

- **Connexion (Login)**
  - **POST** `/api/token/`  
    Envoi le username et le password pour obtenir un Access Token et un Refresh Token :

    ```json
    {
      "username": "nouvel_utilisateur",
      "password": "motdepasse123"
    }
    ```

- **Actualisation du Token (Refresh)**
  - **POST** `/api/token/refresh/`  
    Corps de la requête :

    ```json
    {
      "refresh": "<refresh_token>"
    }
    ```

- **Vérification du Token (Verify)**
  - **POST** `/api/token/verify/`

- **Détails Utilisateur**
  - **GET** `/api/users/` (Renvoie uniquement les données de l'utilisateur connecté)

### Projets

- **Liste des Projets**
  - **GET** `/api/projects/`  
    Seuls les utilisateurs contributeurs peuvent voir les projets auxquels ils ont accès.

- **Création d'un Projet**
  - **POST** `/api/projects/`  
    Lors de la création, l'utilisateur connecté devient l'auteur et est automatiquement ajouté en tant que contributeur.
    Exemple de corps de requête :

    ```json
    {
      "title": "Nouveau projet",
      "description": "Description du projet",
      "type": "Backend"
    }
    ```

- **Détails, Mise à jour et Suppression**
  - **GET / PUT / DELETE** `/api/projects/<project_id>/`

  > **Note :** Seul l'auteur du projet peut modifier ou supprimer le projet.

### Issues

- **Liste des Tickets (Issues)**
  - **GET** `/api/issues/`  
    Filtré sur les projets auxquels l'utilisateur contribue.

- **Création d'un Ticket**
  - **POST** `/api/issues/`  
    Exemple de corps de requête :

    ```json
    {
      "title": "Bug sur la feature X",
      "description": "Description détaillée du bug",
      "tag": "Bug",              // ou "Task", "Amélioration"
      "priority": "Haute",
      "status": "À faire",
      "project": "<project_id>",
      "assignee": "<user_id>"
    }
    ```

- **Détails, Mise à jour et Suppression d'un Ticket**
  - **GET / PUT / DELETE** `/api/issues/<issue_id>/`

> **Important :** Seuls les contributeurs du projet peuvent créer ou consulter les issues.

### Commentaires

- **Liste des Commentaires**
  - **GET** `/api/comments/`  
    Seuls les commentaires associés à des tickets des projets auxquels l'utilisateur contribue sont accessibles.

- **Création d'un Commentaire**
  - **POST** `/api/comments/`  
    Exemple de corps de requête :

    ```json
    {
      "content": "Ceci est un commentaire sur le ticket.",
      "issue": "<issue_id>"
    }
    ```

- **Détails, Mise à jour et Suppression d'un Commentaire**
  - **GET / PUT / DELETE** `/api/comments/<comment_id>/`

### Contributeurs

- **Liste des Contributeurs**
  - **GET** `/api/contributors/`  
    Seuls les contributeurs des projets dont l'utilisateur est auteur sont listés.

- **Ajout d'un Contributeur**
  - **POST** `/api/contributors/`  
    Seul l'auteur d'un projet peut ajouter un contributeur. Exemple de corps de requête :

    ```json
    {
      "project": "<project_id>",
      "user": "<user_id>"
    }
    ```

- **Mise à jour et Suppression d'un Contributeur**
  - **PUT / DELETE** `/api/contributors/<contributor_id>/`

  > **Note :** Les permissions (via IsProjectAuthor) assurent que seul l'auteur du projet peut gérer les contributeurs.

## Technologies

- **Backend** : Django, Django REST Framework
- **Authentification** : JWT via djangorestframework-simplejwt
- **Gestion des dépendances** : Poetry (ou pip)
- **Environnement** : python-dotenv pour la gestion des variables d'environnement

---
