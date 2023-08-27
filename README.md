# OCR_P12_EpicEvent
## Projet 12: EpicEvent
Django version 4.1.4

## Installation et exécution de l'application :

### Installation :
1. Cloner ce dépôt git de code à l'aide de la commande:

    - HTTPS :  https://github.com/motaALI/OCR_P12_EpicEvent.git
    - SSH : git@github.com:motaALI/OCR_P12_EpicEvent.git
    - Zip file : (vous pouvez également télécharger le code en utilisant un fichier zip)
    
2. Rendez-vous depuis un terminal à la racine du répertoire P12_epicEvent
3. Créer un environnement virtuel pour le projet avec :  
    
    `$ python -m venv env` sous windows
    
    `$ python3 -m venv env`  sous mac os ou linux.

4. Activez l'environnement virtuel avec $ env\Scripts\activate sous windows ou $ source env/bin/activate sous macos ou linux.
5. Installez les dépendances du projet avec la commande : 
    `$ pip install -r requirements.txt`  
6. Créer et alimenter la base de données avec la commande:
    `$ 
    6.1 : Créer un schéma postgresl ex:
        ** SCHEMA NAME
        epic_events_schema
    6.2 Créer un uilisateur de la base de données, pour le connecter à votre schéma ex:
        ** SCHEMA USER
            username: epic_events_user
            password: admin
    6.3 : Connecter l'utilsater àla base de données:
        ** SET USER TO SCHEMA
	    ALTER ROLE epic_events_user SET search_path TO epic_events_schema;
    6.4 : Créer un super utilisateur :
    `$ python manage.py createsuperuser`
   `
      
7. Faire des migrations pour cerer la base des données: 
    `python .\manage.py makemigrations`  
8. Appliquer les changements sur la base des données:
    `python manage.py migrate`
    
### Exécution :
1. Avec un environnement virtuel activé exécuter la commande suivante pour démarrer l'application:
    `python .\manage.py runserver`
    
2. Une fois démarrer l'application un serveur de développement sera accessible via une url donnée dans le terminal:
    par défaut django serveur est sur : `http://127.0.0.1:8000/`
3. Pour tester l'API vous pouvez uiliser un postman.