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

- **api** : Gère les projets, les issues (tickets), les commentaires et la gestion des contributeurs.
  - `ProjectViewSet` : Création, consultation, modification et suppression des projets.
  - `IssueViewSet` : Gestion des tickets liés à un projet.
  - `CommentViewSet` : Gestion des commentaires sur les tickets.
  - `ContributorViewSet` : Gestion des contributeurs d'un projet.
  - Permissions personnalisées dans `projects/permissions.py` (ex. IsAuthorOrReadOnly, IsProjectAuthor).

## Endpoints de l'API

### Authentification et Utilisateurs

- **Inscription**
  - **POST** `/api/users/register/`  
    Crée un nouveau compte utilisateur.

- **Connexion**
  - **POST** `/api/users/login/`  
    Récupère les tokens d'accès et de rafraîchissement pour l'authentification.

### Projets

- **Liste des Projets**
  - **GET** `/api/projects/`  
    Récupère la liste des projets auxquels l'utilisateur contribue.

- **Détails d'un Projet**
  - **GET** `/api/projects/<project_id>/`  
    Récupère les informations détaillées du projet spécifié.

- **Liste des Issues d'un Projet**
  - **GET** `/api/projects/<project_id>/issues/`  
    Récupère la liste des tickets (issues) associés au projet spécifié.

### Issues

- **Création d'un Ticket**
  - **POST** `/api/projects/<project_id>/issues/`  
    Crée un ticket pour un projet auquel l'utilisateur contribue.

- **Détails, Mise à jour et Suppression d'un Ticket**
  - **GET / PUT / DELETE** `/api/projects/<project_id>/issues/<issue_id>/`

- **Liste des Commentaires pour une Issue**
  - **GET** `/api/projects/<project_id>/issues/<issue_id>/comments/`  
    Récupère la liste de tous les commentaires associés au ticket spécifié.

### Commentaires

- **Liste des Commentaires**
  - **GET** `/api/projects/<project_id>/comments/`  
    Récupère la liste des commentaires pour les tickets des projets auxquels l'utilisateur contribue.

- **Création d'un Commentaire**
  - **POST** `/api/projects/<project_id>/comments/`  
    Exemple de corps de requête :

    ```json
    {
      "content": "Ceci est un commentaire sur le ticket.",
      "issue": "<issue_id>"
    }
    ```

- **Détails, Mise à jour et Suppression d'un Commentaire**
  - **GET / PUT / DELETE** `/api/projects/<project_id>/comments/<comment_id>/`

### Contributeurs

- **Liste des Contributeurs**
  - **GET** `/api/projects/<project_id>/contributors/`  
    Récupère la liste des contributeurs pour le projet spécifié.

- **Ajout d'un Contributeur**
  - **POST** `/api/projects/<project_id>/contributors/`  
    Seul l'auteur d'un projet peut ajouter un contributeur. Exemple de corps de requête :

    ```json
    {
      "user": "<user_username>"
    }
    ```

- **Mise à jour et Suppression d'un Contributeur**
  - **PUT / DELETE** `/api/projects/<project_id>/contributors/<contributor_id>/`

## Technologies

- **Backend** : Django, Django REST Framework
- **Authentification** : JWT via djangorestframework-simplejwt
- **Gestion des dépendances** : Poetry
- **Environnement** : python-dotenv pour la gestion des variables d'environnement

---
