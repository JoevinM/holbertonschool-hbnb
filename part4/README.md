# Sommaire:

- [Structure du projet](#structure-du-projet)

- [Core Models](#core-models)  
  - [BaseModel](#basemodel)  
  - [User](#user)  
  - [Place](#place)  
  - [Review](#review)  
  - [Amenity](#amenity)

- [Diagramme de la base de données](#Diagramme-Entité-Relation)  

- [Fichiers unittest](#fichier-unittest)  
  - [test_user.py](#test_userpy)  
  - [test_place.py](#test_placepy)  
  - [test_amenity.py](#test_amenitypy)  
  - [test_review.py](#test_reviewpy)

- [Lancer l'application](#Lancer-l'application)

<br>

# Structure du projet

Voici une petite représentation visuelle de la structure globale du projet:

<img width="307" height="698" alt="Structure" src="https://github.com/user-attachments/assets/1c292731-5ba0-4a3f-ba08-53b741a04aae" />


### Description:

| Fichier / Dossier     | Description                                                                                                                                                      |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| app/                  | Contient le code essentiel pour le fonctionnement de l'application.                                                                                             |
| api/                  | Contient tous les fichiers contenant les points de terminaison ou endpoints de chaque entité (users, places ...), organisé par version.                         |
| models/               | Contient les classes de la logique métier.                                                                                                                      |
| services/             | Contient la façade dans laquelle est gérer toutes les interactions entre les différentes couches.                                                               |
| persistence/          | Contient le fichier repository où est implémenté le "in-memory repository", qui va être remplacé plus tard par une vraie base de données utilisant SQL Alchemy. |
| run<space>.py                | C'est le fichier qui sert à lancer l'application Flask. <br>On peut lancer l'application avec la commande suivante: python3 run<space>.py                                                                                                             |
| config<space>.py             | Configure les variables d'environnement et les paramètres de l'application.                                                                                     |
| requirements.txt      | C'est un fichier qui sert aux utilisateurs à bien configurer leur environnement pour que l'application puisse se lancer et fonctionner. Il liste les packages essentiels python.<br>Voici la commande pour installer ces packages: pip install -r requirements.txt                                                                                   |
| README<space>.md             | Vous êtes dans ce fichier qui sert à documenter et avoir un apperçu globale du projet.                                                                          |
| __init __.py           | Ils sont présents un peu partout, cela indique à Python que de traiter les répertoires dans lesquels ils se trouvent comme des paquets importables              |
| repository<space>.py         | Contient toutes les méthodes pour intéragir avec une base de données.                                            |
| facade<space>.py             | Gère la communication entre les différentes couches: le Presentation Layer, La Business Logic Layer et le Persistence Layer.                                   |

<br>
<br>

# Core Models

Comme vous avez pu le voir dans le diagramme de classe, il existe plusieurs entités essentielles au bon fonctionnement de l'applicattion, qui sont au coeur de la logique métier.
Nous les avons initialisé dans le dossier "models", dans des fichiers portant leur nom respectif.
Voici une description complète du rôle de chaque entité, et de leur fonctionnement.


<br>

## BaseModel:
Cette entité contient tous les attributs et méthodes communes aux autres entités.

#### Relations:
Toutes les autres entités héritent de cette classe.

#### Structure:

| Attribut        | Type     | Description                                 |
|-----------------|----------|---------------------------------------------|
| `id`            | UUID     | Identifiant unique de l'objet               |
| `created_at`    | datetime | Date de création de l'objet                 |
| `updated_at`    | datetime | Date de mise à jour de l'objet              |

| Méthode             | Description                                                    | Paramètres  |    Retour   |
|---------------------|----------------------------------------------------------------|-------------|-------------|
| `create(data)`      |Créer un objet avec ses informations                            |data         |None         |
| `read(id)`          |Lit les informations d'un objet                                 |id           |None         |
| `update(data)`      |Met à jour le informations d'un objet                           |data         |None         |
| `delete(id)`        |Supprime un objet                                               |id           |None         |



<br>

## User
Cette entité représente un utilisateur inscrit et enregistré dans l'application.

#### Relations:
L'utilisateur hérite de la classe BaseModel.
L'utilisateur peut avoir plusieurs logements et avis.
Si l'utilisateur supprime son compte, les logements qui lui étaient associés disparaissent mais ses avis resteront.

#### Structure:

| Attribut        | Type     | Description                                 |
|-----------------|----------|---------------------------------------------|
| `first_name`    | string   | Prénom de l'utilisateur                     |
| `last_name`     | string   | Nom de famille de l'utilisateur             |
| `email`         | string   | Adresse email (unique, validée)             |
| `password_hash` | string   | Mot de passe haché                          |
| `is_admin`      | boolean  | Rôle (`user` ou `admin`)                    |

| Méthode             | Description                                                    | Paramètres  |    Retour   |
|---------------------|----------------------------------------------------------------|-------------|-------------|
| `add_review()`      |Ajoute un avis dans la liste d'avis de l'utilisateur            |None         |None         |
| `add_place()`       |Ajoute une location dans la liste de logements de l'utilisateur |None         |None         |

#### Exemple d'utilisation:

from app.models.user import User

def test_user_creation():
    user = User(first_name="John", last_name="Doe", email="john.doe@example.<space>com")
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john.doe@example<space>.com"
    assert user.is_admin is False  # Default value
    print("User creation test passed!")

test_user_creation()

<br>

## Place
Cette entité représente les locations mises à disposition sur l'application.

#### Relations:
Le logement peut avoir plusieurs commodités et avis.
Si le logement disparait, les avis disparaissent aussi.
Si le propriétaire du logement supprime son compte, celui-ci est supprimé également.

#### Structure:

| Attribut      | Type     | Description                                      |
|---------------|----------|--------------------------------------------------|
| `title`       | string   | Titre du lieu                                    |
| `description` | string   | Description textuelle du lieu                    |
| `price`       | float    | Prix associé au lieu (ex. location, entrée)      |
| `latitude`    | float    | Latitude géographique                            |
| `longitude`   | float    | Longitude géographique                           |
| `owner`       | User     | Propriétaire du lieu (instance de `User`)        |
| `reviews`     | list     | Liste des avis associés à ce lieu (`Review`)     |
| `amenities`   | list     | Liste des équipements disponibles (`Amenity`)    |

| Méthode           | Description                                 | Paramètres             | Retour     |
|-------------------|---------------------------------------------|------------------------|------------|
| `add_review()`    | Ajoute un avis à la liste `reviews`.        | `review: Review`       | `None`     |
| `add_amenity()`   | Ajoute un équipement à la liste `amenities`.| `amenity: Amenity`     | `None`     |


<br>

## Review
Cette entité représente les avis laissés sur les logements, pour pouvoir juger de la qulaité du logement.

#### Relations:
Un avis ne peut provenir que d'un seul utilisateur mais celui-ci peut en écrire plusieurs.
Il peut y avoir plusieurs avis sur un même logement.
Si le logement disparait, les avis sur cette habitation disparaîssent.
Si l'utilisateur supprime son compte, son avis reste.

#### Structure:

| Attribut   | Type     | Description                                      |
|------------|----------|--------------------------------------------------|
| `text`     | string   | Commentaire rédigé par l'utilisateur             |
| `rating`   | int      | Note attribuée au lieu (généralement entre 1–5)  |
| `owner`    | User     | Auteur de l'avis (instance de `User`)            |
| `place`    | Place    | Lieu concerné par l'avis (instance de `Place`)   |

#### Exemple  d'utilisation avec place et review:

from app.models.place import Place
from app.models.user import User
from app.models.review import Review

def test_place_creation():
    owner = User(first_name="Alice", last_name="Smith", email="alice.smith@example.<space>com")
    place = Place(title="Cozy Apartment", description="A nice place to stay", price=100, latitude=37.7749, longitude=-122.4194)
    # Adding a review
    review = Review(text="Great stay!", rating=5, place=place)
    place.add_review(review)
    assert place.title == "Cozy Apartment"
    assert place.price == 100
    assert len(place.reviews) == 1
    assert place.reviews[0].text == "Great stay!"
    print("Place creation and relationship test passed!")

test_place_creation()



<br>

## Amenity
Entité représentant les commodités associées à un logement. (piscine, wi-fi...)

#### Relations:
Un logement peut avoir plusieurs commodités.
Il peut y avoir la même commodité sur plusieurs logements.

#### Structure:

| Attribut | Type   | Description                            |
|----------|--------|----------------------------------------|
| `name`   | string | Nom de l'équipement ou commodité       |

#### Exemple d'utilisation:

from amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi")
    assert amenity.<space>name == "Wi-Fi"
    print("Amenity creation test passed!")

test_amenity_creation()

<br>
<br>

# Diagramme Entité-Relation

Voici ci-dessous le diagramme d'entité-relations représente la structure de notre base de données avec ses entités,
leurs attributs ainsi que leurs relations.

### Entité:
C'est un objet stocké sous forme de données, ici nous avons par exemple les utilisateurs (User) et les logements (Place).

### Attribut:
Ce sont les propriétées d'une entité comme son identifiant (id) (User.id), ou son prénom (name) (User.name).

### Relation:
C'est un lien entre deux entités pour définir leurs comportements (many to many, one to many). Par exemple un lieu peut avoir plusieurs avis.

<img width="1260" height="2105" alt="ER Diagram" src="https://github.com/user-attachments/assets/08931ffb-0f78-44c6-8e68-70fb6fd91d00" />


En complément de ce diagramme et pour plus de précisions, voici une clarification sur le comportement des entités lors de la suppression.
Nous avons décidé que tous les lieux associés à un utilisateur seront supprimés si celui-ci supprime son compte.
En revanche, ses avis seront conservés.
À l’inverse, si un lieu est supprimé, tous les avis qui lui sont liés seront également supprimés.
Les méthodes DELETE ont été implémentées uniquement pour les avis, mais cette précision vise à expliciter la logique de suppression appliquée aux différentes entités.


# Fichiers unittest

Voici ci-dessous tous les fichiers effectuant des tests unitaires dans le but de vérifier le bon fonctionnement de l'application.
Il vérifie notamment que les endpoints de chaque entitée fonction et que la gestion des erreurs est correcte.

<br>

## test_user.py

Commande de test: python3 test_user.py


| **Nom**                            | **Test**                                                                 | **Payload/informations envoyées**                                                                                                                                     | **Résultat attendu**                                                                                                                       | **Résultat obtenu**                                                                                                                        |
|-----------------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| `test_valid_user_creation`        | Création d'un nouvel utilisateur valide                                  | `{"first_name": "Light", "last_name": "Yagami", "email": "light.yagami@mail.com"}`                                                                                    | Un nouvel utilisateur avec un ID unique et un code de réponse **201**.                                                                    | Un nouvel utilisateur avec un ID unique et un code de réponse **201**.                                                                    |
| `test_invalid_empty_last_name`    | Création d'un nouvel utilisateur avec un nom de famille vide             | `{"first_name": "Saitama", "last_name": "", "email": "saitama@mail.com"}`                                                                                             | Échec de la requête en renvoyant un message d'erreur avec un code de réponse **400**.                                                     | Échec de la requête en renvoyant un message d'erreur avec un code de réponse **400**.                                                     |
| `test_invalid_empty_first_name`   | Création d'un nouvel utilisateur avec un prénom vide                     | `{"first_name": "", "last_name": "Albator", "email": "albator@mail.com"}`                                                                                             | Échec de la requête en renvoyant un message d'erreur avec un code de réponse **400**.                                                     | Échec de la requête en renvoyant un message d'erreur avec un code de réponse **400**.                                                     |
| `test_invalid_empty_email`        | Création d'un nouvel utilisateur avec un email vide                      | `{"first_name": "Tanjiro", "last_name": "Kamado", "email": ""}`                                                                                                       | Échec de la requête en renvoyant un message d'erreur avec un code de réponse **400**.                                                     | Échec de la requête en renvoyant un message d'erreur avec un code de réponse **400**.                                                     |
| `test_invalid_duplicate_email`    | Création d'un utilisateur déjà existant                                  | `{"first_name": "Son", "last_name": "Goku", "email": "sayan@mail.com"}` deux fois à la suite.                                                                        | Création du premier utilisateur avec un ID unique puis échec de la requête car l'utilisateur existe déjà avec un code de réponse **400**. | Création du premier utilisateur avec un ID unique puis échec de la requête car l'utilisateur existe déjà avec un code de réponse **400**. |
| `test_update_valid_fields`        | Mettre à jour les informations d'un utilisateur avec des valeurs correctes, test directement dans le code. | Création d'un nouvel utilisateur: `{first_name="Yugi", last_name="Yami", email="yugi.yami@mail.com"}` puis envoie de nouvelles informations: `{"first_name": "Yugi", "last_name": "Muto", "email": "yugi.muto@mail.com"}` | Création d'un utilisateur et une mise à jour de ses informations avec un code de réponse **200**.                                         | Création d'un utilisateur et une mise à jour de ses informations. Un code de réponse **200** est obtenu sur Postman.                      |
| `test_update_invalid_first_name`  | Mettre à jour les informations d'un utilisateur avec un prénom vide, test directement dans le code.       | Création d'un nouvel utilisateur: `{first_name="Naruto", last_name="Uzumaki", email="naruto.uzumaki@mail.com"}` puis envoie de nouvelles informations: `{"first_name": "", "last_name": "Muto", "email": "yugi.muto@mail.com"}` | Création d'un utilisateur et échec de la mise à jour de ses informations avec un message d'erreur.                                       | Création d'un utilisateur et échec de la mise à jour de ses informations avec un message d'erreur.                                       |
| `test_update_invalid_last_name`   | Mettre à jour les informations d'un utilisateur avec un nom de famille vide, test directement dans le code. | Création d'un nouvel utilisateur: `{first_name="Gojo", last_name="Satoru", email="gojo.satoru@mail.com"}` puis envoie de nouvelles informations: `{"first_name": "Gojo", "last_name": "", "email": "gojo.satoru@mail.com"}` | Création d'un utilisateur et échec de la mise à jour de ses informations avec un message d'erreur.                                       | Création d'un utilisateur et échec de la mise à jour de ses informations avec un message d'erreur.                                       |

<br>

## test_place.py

Commande de test: python3 test_place.py

| Nom du test                         | Description                                                                 | Payload / Données envoyées                                                                 | Résultat attendu                                                                 | Résultat obtenu                                                                  |
|------------------------------------|------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| `test_create_place`                | Création d’un lieu avec des données valides                                 | `{title, description, price, latitude, longitude, owner_id}`                               | Code de réponse `201` avec la création d'un nouveau logement avec un id unique                                                            | Code de réponse `201` avec la création d'un nouveau logement avec un id unique                                                            |
| `test_create_empty_title`         | Création d’un lieu avec un titre vide                                       | `{title: ""}`                                                                              | Exception `ValueError` avec un échec de création du nouveau logement                                                           | Exception `ValueError` avec un échec de création du nouveau logement                                                          |
| `test_create_invalid_price`       | Création d’un lieu avec un prix négatif                                     | `{price: -90}`                                                                             | Exception `ValueError` avec un échec de création du nouveau logement                                                          | Exception `ValueError` avec un échec de création du nouveau logement                                                           |
| `test_create_invalid_type_price`  | Création d’un lieu avec un prix non numérique                               | `{price: "yo"}`                                                                            | Exception `TypeError` avec un échec de création du nouveau logement                                                           | Exception `TypeError` avec un échec de création du nouveau logement                                                            |
| `test_create_invalid_latitude`    | Création d’un lieu avec une latitude hors limites                           | `{latitude: -100.7749}`                                                                    | Exception `ValueError` avec un échec de création du nouveau logement                                                           | Exception `ValueError` avec un échec de création du nouveau logement                                                           |
| `test_create_invalid_type_latitude`| Création d’un lieu avec une latitude non numérique                          | `{latitude: "ah"}`                                                                         | Exception `TypeError` avec un échec de création du nouveau logement                                                           | Exception `TypeError` avec un échec de création du nouveau logement                                                           |
| `test_create_invalid_longitude`   | Création d’un lieu avec une longitude hors limites                          | `{longitude: -222.4194}`                                                                   | Exception `ValueError` avec un échec de création du nouveau logement                                                          | Exception `ValueError` avec un échec de création du nouveau logement                                                          |
| `test_create_invalid_type_longitude`| Création d’un lieu avec une longitude non numérique                         | `{longitude: "non-float"}`                                                                 | Exception `TypeError` avec un échec de création du nouveau logement                                                           | Exception `TypeError` avec un échec de création du nouveau logement                                                           |
| `test_create_empty_owner_id`      | Création d’un lieu avec un `owner_id` vide                                  | `{owner_id: ""}`                                                                           | Exception `ValueError` avec un échec de création du nouveau logement                                                          | Exception `ValueError` avec un échec de création du nouveau logement                                                          |
| `test_create_place_invalid_owner_id`| Création d’un lieu avec un `owner_id` inexistant                            | `{owner_id: "aaaaaaah"}`                                                                   | Code de réponse `400` avec un échec de création du nouveau logement                                                            | Code de réponse `400` avec un échec de création du nouveau logement                                                           |
| `test_create_same_place`          | Création d’un lieu déjà existant (doublon)                                  | Deux requêtes identiques avec les mêmes données                                            | Première requête OK, seconde échoue avec code `400`                              | Première requête OK, seconde échoue avec code `400`                              |
| `test_get_all_places`             | Récupération de tous les lieux via l’API                                    | Requête GET sans payload                                                                   | Code de réponse `200`                                                            | Code de réponse `200`                                                            |
| `test_valid_update_place`         | Mise à jour d’un lieu avec des données valides                              | `{description: "A nice place to stay"}`                                                    | Mise à jour réussie, attribut modifié                                            | Mise à jour réussie, attribut `description` mis à jour                           |
| `test_invalid_update_place`       | Mise à jour d’un lieu avec un titre vide                                    | `{title: ""}`                                                                              | Exception `ValueError` échec de la mise à jour                                                          | Exception `ValueError` échec de la mise à jour                                                          |

<br>

## test_review.py

Commande de test: python3 test_review.py

| Nom du test                             | Description                                                                 | Payload / Données envoyées                                                                                     | Résultat attendu                                      | Résultat obtenu                                       |
|----------------------------------------|-----------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|
| `test_create_review_success`           | Création d’un avis avec des données valides                                 | `{text, rating: 5, user_id, place_id}`                                                                          | Code de réponse `201` et création d'un avis avec un ID unique                                 | Code de réponse `201` et création d'un avis avec un ID unique                                  |
| `test_create_review_invalid_text`      | Création d’un avis avec un texte vide                                       | `{text: "", rating: 5, user_id, place_id}`                                                                      | Code de réponse `400`                                  | Code de réponse `400`                                  |
| `test_create_review_invalid_rating`    | Création d’un avis avec une note hors de l’intervalle 1–5                   | `{text, rating: 9, user_id, place_id}`                                                                          | Code de réponse `400` et échec de création d'un avis                                 | Code de réponse `400` et échec de création d'un avis                                 |
| `test_create_review_invalid_user`      | Création d’un avis avec un ID utilisateur inexistant                        | `{text, rating: 5, user_id: "user_id", place_id}`                                                               | Code de réponse `404` et échec de création d'un avis                                 | Code de réponse `404` et échec de création d'un avis                                 |
| `test_create_review_invalid_place`     | Création d’un avis avec un ID lieu inexistant                               | `{text, rating: 5, user_id, place_id: "place_id"}`                                                              | Code de réponse `404` et échec de création d'un avis                                 | Code de réponse `404` et échec de création d'un avis                                 |
| `test_get_all_reviews`                 | Récupération de tous les avis via l’API                                     | Requête GET sans payload                                                                                        | Code de réponse `200`                                  | Code de réponse `200`                                  |
| `test_get_review_by_id`                | Récupération d’un avis par ID valide                                        | Requête GET avec `review.id` valide                                                                             | Code de réponse `200` et récupération de l'avis                                 | Code de réponse `200` et récupération de l'avis                                 |
| `test_get_review_not_found`            | Récupération d’un avis avec un ID invalide                                  | Requête GET avec `review-id` inexistant                                                                         | Code de réponse `404` et la non récupération de l'avis                                 | Code de réponse `404` et la non récupération de l'avis                                 |
| `test_update_review_success`           | Mise à jour d’un avis avec des données valides                              | `{text, rating: 5, user_id, place_id}`                                                                          | Code de réponse `200` et la mise à jour de l'avis                                | Code de réponse `200` et la mise à jour de l'avis                                 |
| `test_update_review_not_found`         | Mise à jour d’un avis avec un ID inexistant                                 | `{text, rating: 5, user_id, place_id}` vers `/reviews/fake-id`                                                 | Code de réponse `404` et l'échec de la mise à jour de l'avis                                | Code de réponse `404` et l'échec de la mise à jour de l'avis                                  |
| `test_update_review_invalid_rating`    | Mise à jour d’un avis avec une note invalide                                | `{text, rating: 10, user_id, place_id}`                                                                         | Code de réponse `400` et l'échec de la mise à jour de l'avis                                 | Code de réponse `400` et l'échec de la mise à jour de l'avis                                 |
| `test_delete_review_success`           | Suppression d’un avis existant                                              | Requête DELETE vers `/reviews/{review.id}`                                                                      | Code de réponse `200`  et la suppression de l'avis                                | Code de réponse `200` et la suppresion de l'avis                                 |
| `test_delete_review_not_found`         | Suppression d’un avis avec un ID inexistant                                 | Requête DELETE vers `/reviews/fake-id`                                                                          | Code de réponse `404` Avis pas trouvé                                 | Code de réponse `404` Avis pas trouvé                                 |
| `test_get_reviews_by_place`            | Récupération de tous les avis pour un lieu valide                           | Requête GET vers `/reviews/places/{place.id}/reviews`                                                           | Code de réponse `200` et affiche tous les avis reliés au lieu                                 | Code de réponse `200` et affiche tous les avis reliés au lieu                                 |
| `test_get_reviews_by_place_place_not_found` | Récupération des avis pour un lieu inexistant                          | Requête GET vers `/reviews/places/fake-id/reviews`                                                              | Code de réponse `404` le lieu n'a pas été trouvé                                 | Code de réponse `404` le lieu n'a pas été trouvé                                 |

<br>

## test_amenity.py

Commande de test: python3 test_amenity.py

| Nom du test                      | Description                                                             | Payload / Données envoyées                          | Résultat attendu                                      | Résultat obtenu                                       |
|----------------------------------|-------------------------------------------------------------------------|------------------------------------------------------|--------------------------------------------------------|--------------------------------------------------------|
| `test_create_amenity`           | Création d’une commodité avec un nom valide                             | `{ "name": "Wi-Fi" }`                                | Code de réponse `201` et création de la nouvelle commodité avec un nouvel ID unique                                  | Code de réponse `201` et création de la nouvelle commodité avec un nouvel ID unique                                  |
| `test_create_empty_amenity`     | Création d’une commodité avec un nom vide                               | `{ "name": "" }`                                     | Exception `ValueError` et échec de création d'une nouvelle amenity                                | Exception `ValueError` et échec de création d'une nouvelle amenity                                |
| `test_create_same_amenity`      | Création d’une commodité avec un nom déjà existant                      | Deux requêtes avec `{ "name": "Wi-Fi" }`             | Première requête OK, seconde échoue avec code `400`    | Première requête OK, seconde échoue avec code `400`    |
| `test_get_all_amenities`        | Récupération de toutes les commodités via l’API                         | Requête GET sans payload                             | Code de réponse `200`                                  | Code de réponse `200`                                  |
| `test_valid_update_amenity`     | Mise à jour d’une commodité avec un nom valide                          | `{ "name": "Jacuzzi" }`                              | Mise à jour réussie, attribut modifié                  | Mise à jour réussie, attribut `name` mis à jour        |
| `test_invalid_update_amenity`   | Mise à jour d’une commodité avec un nom vide                            | `{ "name": "" }`                                     | Exception `ValueError` et échec de la mise à jour                                | Exception `ValueError` et échec de la mise à jour                                  |


<br>

# Lancer l'application

Voici ci-dessous, les différentes étapes pour lancer l'application :

- Installez tous les outils/extensions requis avec la commande :
pip install -r requirements

- Lancez l'application en étant dans /holbertonschool-hbnb/part3 :
python3 run.py