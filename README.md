# Projet_kit_big_data

Par Damien Thai, Baptiste Cervoni, Alexandre Malfoy, Alexandre Rocchi


## Etape 1
Conscient que ce dataset vous permet de réaliser différentes analyses pertinentes,
Mangetamain a décidé de vous faire pleinement confiance et vous laisse
l'opportunité de choisir l’axe d’analyse que vous trouverez le plus intéressant à
développer et mettre en avant.
Ainsi, vous devez identifier une question / un thème qui définissent le fil principal de
votre étude, par exemple :


### Liste des thèmes potentiels

- [X] Le profil des utilisateurs contribuant le plus au site ?
- [X] Quelles sont les caractéristiques des recettes les plus populaires ?
- [X] Recommandation de recette en fonction du temps dont on dispose, avec une interface permettant de sélectionner le temps/les ingrédients
- [X] Visualisation des recettes par réduction de dimension pour déterminer les recettes qui se rapprochent de celles que l'on a déjà faites
- [X] Générer un nom de recette à partir des ingrédients et des techniques utilisées pour la réaliser
- [X] Est-ce que les utilisateurs les plus anciens obtiennent de meilleures notes à leurs recettes ?
   
ETC..



### Idée

- [X] Faire une page relative à la nutrition, se  concentrer sur chaque ingrédients, à quel point il est nutritif, les qualités nutritives des recettes qui l'utilisent
- [X] relations entre popularité d'une recette (à définir) et une autre feature (les ingrédients qu'elle utilise, le temps qu'elle met, sa popularité au fil du temps, sa classe)
- [X] Tag, ingrédients, nutrition à la mode



# TODO: Points clefs du projets

### La gestion du projet
- [X] Structure du projet : organisez votre projet en respectant une structure cohérente.
Utilisez des packages et des modules pour diviser votre code en composants
logiques. Vous pouvez utiliser Visual Studio Code si vous n’avez pas encore d’IDE
préféré.
- [X] Environnement Python : utilisez un gestionnaire d'environnement Python ou
Poetry pour gérer les dépendances de votre projet. Choisissez bien votre version
de Python. Assurez-vous d'avoir un fichier requirements.txt ou pyproject.toml
correctement configuré.
  - [ ] : Vérifier sur un nouvel env que le requirements.txt est à jour

- [X] Git : initialiser un dépôt Git pour votre projet et suivez les meilleures pratiques de
gestion de code avec des commits (assurez-vous de committer régulièrement), et
dans la mesure du possible, des branches et des Pull Request pour travailler en
équipe. Assurez-vous d'inclure un fichier README.md qui explique comment
installer, exécuter, déployer et utiliser votre application.
  - [ ] README à mettre à jour
  - [ ] Protection des branches        

Optionnel : créez éventuellement des tags de version pour marquer les versions
stables de votre application.


- [ ] Streamlit : développer votre webapp avec une expérience utilisateur (UX) simple et
intuitive, en laissant à l’utilisateur la possibilité d'interagir avec vos données pour bien
comprendre la storytelling que vous lui raconterez. Cette storytelling doit comporter
des insights au travers de graphiques (charts, etc.) et doit répondre à votre
problématique / question initiale.
  - [ ] Story Telling
  - [X] Question Initial : "Pourquoi le site perds des membres ?"
  - Pages :
    - [ ] Accueil
    - [ ] Preprocessing


### La programmation

- [X] Programmation orientée objet : dans la mesure du possible, utilisez le paradigme
orienté objet. Utilisez les principes de l'encapsulation et de l'héritage si approprié.
Utilisez également les bonnes structures de données.
- [ ] Type Hinting : utilisez des annotations de type pour améliorer la lisibilité de votre
code.
- [ ] PEP 8 : assurez-vous que votre code respecte les normes PEP 8 pour la lisibilité et
la cohérence du code. Utilisez un formateur (par exemple black)
  - [ ] Améliorer la note de 6/10 de pylint -> 7.5/10
- [ ] Gestion des exceptions : gérez les erreurs de manière appropriée en utilisant des
exceptions personnalisées lorsque nécessaire. Par exemple en cas de saisie
incorrecte de l'utilisateur.
- [ ] Logger : utilisez le module logging pour enregistrer les actions de l'utilisateur et les
événements importants dans un fichier de log. Créer un fichier de log pour le debug,
et un autre pour les erreurs (ERROR et CRITICAL). 
-> J'ai crée le logging_config. Maintenant dans chaque module du dossier src il faut faire :
import logging
logger = logging.getLogger(__name__)
Puis ensuite je placer des lignes logger.info, logger.error, logger.debug à des endroits stratégiques dans les fonctions.
- [X] Sécurité : assurez-vous (un minimum) que les bibliothèques que vous utilisez sont
connues et n'ont pas de vulnérabilités de sécurité évidentes. Si vous autorisez une
entrée utilisateur, ne pas utiliser la fonction `eval`, évitez les mots de passe/token en
clair dans le code, etc.



### Les tests

- [ ] Tests unitaires : écrivez des tests unitaires approfondis pour chaque composant de
votre application en utilisant pytest. Vérifiez que la logique de votre application
fonctionne correctement.
- [ ] Test coverage : utilisez un outil de test coverage (comme pytest-cov) pour mesurer
la couverture de vos tests et assurez-vous d'avoir une couverture suffisante (90% de
couverture minimum).

### La documentation du projet

- [ ] Commentaires : assurez-vous d'inclure des commentaires pertinents dans votre
code pour expliquer la logique complexe ou les décisions de conception importantes.
- [ ] Docstrings : utilisez des docstrings pour documenter vos classes, méthodes et
fonctions de manière détaillée, en expliquant leur but, leurs paramètres et leurs
valeurs de retour. Vous pouvez utiliser la convention qu'il vous plaira : Google,
NumPy ou reStructuredText (reST).
- [ ] Documentation : créez une documentation claire et concise pour votre application
en utilisant Sphinx. Documentez les classes, les méthodes, et expliquez comment
installer et utiliser votre application.
### La CI
- [ ] Pipeline CI/CD : configurez un pipeline de CI avec GitHub Actions pour checker
que pep8 est bien respecté, que les docstrings sur les fonctions / méthodes,
classes, modules sont bien présentes, pour automatiser les tests et vérifier que le
test coverage est supérieur à 90% du code. Les tests unitaires doivent être
exécutés automatiquement à chaque push sur une branche en review, et lors du
merge de la branche en review sur master.
Optionnel : inclure votre phase de déploiement de l’application dans votre CI/CD
### Commentaires
- [ ] Commentaires à avoir en liste : Importer la liste de tout les commentaires et
pas la liste des caractères des commentaires