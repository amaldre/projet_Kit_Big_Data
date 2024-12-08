

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
  - [ ] Protection des branches c'est impossible je crois qu'il faut github premium       

Optionnel : créez éventuellement des tags de version pour marquer les versions
stables de votre application.


- [X] Streamlit : développer votre webapp avec une expérience utilisateur (UX) simple et
intuitive, en laissant à l’utilisateur la possibilité d'interagir avec vos données pour bien
comprendre la storytelling que vous lui raconterez. Cette storytelling doit comporter
des insights au travers de graphiques (charts, etc.) et doit répondre à votre
problématique / question initiale.
  - [X] Story Telling
  - [X] Question Initial : "Pourquoi le site perds des membres ?"
  - Pages :
    - [X] Accueil
    - [X] Preprocessing


### La programmation

- [X] Programmation orientée objet : dans la mesure du possible, utilisez le paradigme
orienté objet. Utilisez les principes de l'encapsulation et de l'héritage si approprié.
Utilisez également les bonnes structures de données.
- [X] Type Hinting : utilisez des annotations de type pour améliorer la lisibilité de votre
code.
- [X] PEP 8 : assurez-vous que votre code respecte les normes PEP 8 pour la lisibilité et
la cohérence du code. Utilisez un formateur (par exemple black)
  - [X] Améliorer la note de 6/10 de pylint -> 7.5/10
- [X] Gestion des exceptions : gérez les erreurs de manière appropriée en utilisant des
exceptions personnalisées lorsque nécessaire. Par exemple en cas de saisie
incorrecte de l'utilisateur.
- [X] Logger : utilisez le module logging pour enregistrer les actions de l'utilisateur et les
événements importants dans un fichier de log. Créer un fichier de log pour le debug,
et un autre pour les erreurs (ERROR et CRITICAL). 
- [X] Sécurité : assurez-vous (un minimum) que les bibliothèques que vous utilisez sont
connues et n'ont pas de vulnérabilités de sécurité évidentes. Si vous autorisez une
entrée utilisateur, ne pas utiliser la fonction `eval`, évitez les mots de passe/token en
clair dans le code, etc.



### Les tests

- [X] Tests unitaires : écrivez des tests unitaires approfondis pour chaque composant de
votre application en utilisant pytest. Vérifiez que la logique de votre application
fonctionne correctement.
- [X] Test coverage : utilisez un outil de test coverage (comme pytest-cov) pour mesurer
la couverture de vos tests et assurez-vous d'avoir une couverture suffisante (90% de
couverture minimum).

### La documentation du projet

- [ ] Commentaires : assurez-vous d'inclure des commentaires pertinents dans votre
code pour expliquer la logique complexe ou les décisions de conception importantes.
- [X] Docstrings : utilisez des docstrings pour documenter vos classes, méthodes et
fonctions de manière détaillée, en expliquant leur but, leurs paramètres et leurs
valeurs de retour. Vous pouvez utiliser la convention qu'il vous plaira : Google,
NumPy ou reStructuredText (reST).
- [X] Documentation : créez une documentation claire et concise pour votre application
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
