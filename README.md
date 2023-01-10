# SystemeDeRecommandation
Système De Recommandation dans la plateforme YELP en utilisant Python et Neo4j

De nos jours, nous remarquons l'existence de plusieurs sites participatifs dans lesquels, des utilisateurs de la plateforme partage des avis qui 
concernent différents business tels que des restaurants, des commerciaux,
des écoles et des établissements locaux. Parmi ces sites, on cite Yelp
(https://www.yelp.com) , qui est un site participatif d’avis sur les
commerces locaux et de réseautage social, où les utilisateurs peuvent
soumettre un avis de leurs produits et services à l'aide d'un système de
notation de 1 à 5 étoiles. Les sociétés peuvent également actualiser leurs
coordonnées, leurs heures d'exploitation et d'autres renseignements de base
ou ajouter des renseignements précis. En plus de rédiger des
commentaires, les utilisateurs peuvent réagir aux commentaires, planifier
des activités ou parler de leur vie personnelle.
L’objectif du projet est de faire l’analyse des données Yelp concernant les
utilisateurs, les avis des différents utilisateurs et les restaurants sous forme
des données orientés graphes à la base d’un schéma modélisé dédié pour
notre cas : Création des nœuds pour chaque entité étudiée et les différentes
relations correspondantes avec le logiciel neo4j desktop. Après, on
interroge la base de données graphe créée avec le langage Cypher qui est
langage informatique de requête orienté graphe utilisé par Neo4j. Ce projet
fait partie de l'étude sur des restaurants implémentés dans la région du
Delaware faite par un groupe industriel. Ce groupe souhaite inviter dans
chacun de ses restaurants des utilisateurs de la plateforme Yelp qui
joueront ensuite le rôle d’influenceurs auprès de leurs amis afin de les
promouvoir et d’attirer un maximum de clientèle.
Pour sélectionner les utilisateurs qui sont des influenceurs pour chacun des
restaurants, le groupe propose de calculer un score d’influence des
utilisateurs de la plateforme
