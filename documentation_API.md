# Documentation Complète de l'API Softdesk

Cette documentation fournit tous les endpoints de l'API ainsi que des exemples de corps de requête pour faciliter l'intégration.

## Table des matières

- [Authentification et Utilisateurs](#authentification-et-utilisateurs)
- [Projets](#projets)
- [Issues](#issues)
- [Commentaires](#commentaires)
- [Contributeurs](#contributeurs)
- [Gestion du Compte Utilisateur](#gestion-du-compte-utilisateur)

---

## Authentification et Utilisateurs

### Inscription
- **POST** `/api/register/`  
  Crée un nouveau compte utilisateur.

  **Exemple de corps de requête :**
  ```json
  {
    "username": "exemple_user",
    "email": "user@example.com",
    "birth_date": "2000-01-01",
    "consent": true,
    "can_be_contacted": false,
    "can_data_be_shared": false,
    "password": "motdepasse123"
  }
  ```

### Connexion
- **POST** `/api/login/`  
  Récupère les tokens d'accès et de rafraîchissement pour l'authentification.

- **POST** `/api/token/refresh/`  
  Rafraîchit le token d'accès.

- **POST** `/api/token/verify/`  
  Vérifie la validité d'un token.

---

## Projets

### Création d'un Projet
- **POST** `/api/projects/`  
  Crée un projet pour lequel l'utilisateur devient automatiquement contributeur.

  **Exemple de corps de requête :**
  ```json
  {
    "title": "Nouveau projet",
    "description": "Description détaillée du projet",
    "type": "Backend"
  }
  ```

### Liste des Projets
- **GET** `/api/projects/`  
  Récupère la liste des projets auxquels l'utilisateur contribue.

### Détails d'un Projet
- **GET** `/api/projects/<project_id>/`  
  Récupère les informations détaillées du projet spécifié.

### Liste des Issues d'un Projet
- **GET** `/api/projects/<project_id>/issues/`  
  Récupère la liste des tickets (issues) associés au projet spécifié.

---

## Issues

### Création d'un Ticket
- **POST** `/api/projects/<project_id>/issues/`  
  Crée un ticket pour un projet auquel l'utilisateur contribue.

  **Exemple de corps de requête :**
  ```json
  {
    "title": "Bug critique",
    "description": "Description du problème rencontré",
    "priority": "High"  // Exemple, à adapter selon vos champs
  }
  ```

### Détails, Mise à jour et Suppression d'un Ticket
- **GET / PUT / DELETE** `/api/projects/<project_id>/issues/<issue_id>/`

### Liste des Commentaires pour une Issue
- **GET** `/api/projects/<project_id>/issues/<issue_id>/comments/`  
  Récupère tous les commentaires associés à l'issue.

---

## Commentaires

### Création d'un Commentaire
- **POST** `/api/projects/<project_id>/comments/`  
  Crée un commentaire sur un ticket spécifique.

  **Exemple de corps de requête :**
  ```json
  {
    "content": "Ceci est un commentaire sur le ticket.",
    "issue": "<issue_id>"
  }
  ```

### Détails, Mise à jour et Suppression d'un Commentaire
- **GET / PUT / DELETE** `/api/projects/<project_id>/comments/<comment_id>/`

---

## Contributeurs

### Liste des Contributeurs
- **GET** `/api/projects/<project_id>/contributors/`  
  Récupère la liste des contributeurs d'un projet.

### Ajout d'un Contributeur
- **POST** `/api/projects/<project_id>/contributors/`  
  Seul l'auteur du projet peut ajouter un contributeur.

  **Exemple de corps de requête :**
  ```json
  {
    "user": "<user_username>"
  }
  ```

### Mise à jour et Suppression d'un Contributeur
- **PUT / DELETE** `/api/projects/<project_id>/contributors/<contributor_id>/`

---

## Gestion du Compte Utilisateur

### Consulter ses informations
- **GET** `/api/users/me/`
  Récupère les informations de l'utilisateur connecté

### Mettre à jour ses informations
- **PUT/PATCH** `/api/users/me/`
  Met à jour les informations de l'utilisateur

  **Exemple de corps de requête :**
  ```json
  {
    "email": "nouveau@email.com",
    "can_be_contacted": true,
    "can_data_be_shared": false
  }
  ```

### Supprimer son compte
- **DELETE** `/api/users/me/`
  Supprime le compte de l'utilisateur (anonymisation des données) 