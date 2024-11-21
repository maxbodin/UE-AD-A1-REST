# UE-AD-A1-REST

**UE AD FIL A1**

[Tutoriel FLASK API de Helene Coullon - helene.coullon@imt-atlantique.fr](https://helene-coullon.fr/pages/ue-ad-fil-24-25/tuto-flask/)

[Tutoriel OPENAPI de Helene Coullon - helene.coullon@imt-atlantique.fr](https://helene-coullon.fr/pages/ue-ad-fil-24-25/tuto-openapi/)

[Tutoriel FLASK, REST et OPENAPI de Helene Coullon - helene.coullon@imt-atlantique.fr](https://helene-coullon.fr/pages/ue-ad-fil-24-25/tp-rest/)

## Objectifs

- Développer une application de 4 micro-services pour la gestion d’une salle de cinéma.
- Comprendre les concepts de développements de micro-services et apprendre à utiliser trois types d’API.

## Travail Réalisé

### Extension du Service Movie

- Ajout de points d'entrée supplémentaires pour récupérer des informations détaillées sur les films, comme :
    - Liste des films disponibles.
    - Informations spécifiques à un film donné via son id.
    - Informations spécifiques à un film donné via son titre exact.
    - Informations spécifiques à un film donné via une partie de son titre.
    - Informations spécifiques à des films via un réalisateur.
    - Informations spécifiques à des films via un genre.
    - Ajouter un nouveau film.
    - Modifier la note d'un film.
    - Supprimer un film.
    - Ajout d'un point d'entrée help fournissant la liste des points d'entrée disponibles dans le service Movie.
- Mise à jour de la spécification OpenAPI pour inclure ces nouveaux points d'entrée.
- Tests avec Postman et Insomnia pour vérifier le bon fonctionnement des nouveaux points d'entrée.

### Création du Service Showtime

- Création du micro-service Showtime basé sur la spécification UE-archi-distribuees-Showtime-1.0.0-resolved.yaml.
- Implémentation des fonctionnalités permettant d'afficher les horaires des séances.
- Tests approfondis avec Postman et Insomnia pour valider le comportement du service et sa conformité avec la
  spécification.

### Création du Service Booking

- Création du micro-service Booking en suivant la spécification UE-archi-distribuees-Booking-1.0.0-resolved.yaml.
- Implémentation des fonctionnalités liées aux réservations, comme :
    - Affichage des réservations.
    - Affichage des réservations pour un utilisateur donné.
    - Création d’une réservation pour un utilisateur donné.
- Tests approfondis avec Postman et Insomnia pour valider le comportement du service et sa conformité avec la
  spécification.

### Création du Service User

- Analyse du fichier user.json pour concevoir une spécification OpenAPI adaptée au service User.
- Implémentation de points d'entrée intégrant les services Booking et Movie :
    - Récupération des réservations d’un utilisateur à partir de son nom ou ID, avec interrogation du service Booking
      pour valider les données.
    - Récupération des informations des films pour les réservations d’un utilisateur, nécessitant une communication avec
      les services Booking et Movie.
- Tests approfondis avec Postman et Insomnia pour valider le comportement du service et sa conformité avec la
  spécification.

### Mise à jour de la configuration Docker

- Mise à jour du fichier compose pour accepter les communications entre conteneurs et l'utilisation des constantes.

## Lancer le Projet

### Prérequis

- Docker et Docker Compose installés sur votre machine.

### Étapes

- Clonez le repository :

```bash
    git clone https://github.com/maxbodin/UE-AD-A1-REST.git
    cd UE-AD-A1-REST
```

- Lancez les services avec Docker Compose :

```bash
  docker-compose up --build
```

- Les services seront accessibles sur les ports décrits dans le fichier constants.py :

- Arrêtez les services avec :

```bash
    docker-compose down
```

## Organisation du Repository
```bash
├── docker-compose.yml # Configuration Docker Compose pour lancer tous les microservices
├── movie/ # Code source du service Movie
├── showtime/ # Code source du service Showtime
├── booking/ # Code source du service Booking
├── user/ # Code source du service User
├── constants.py # Contient les constantes utilisées par tous les services
└── README.md # Documentation du projet
```
