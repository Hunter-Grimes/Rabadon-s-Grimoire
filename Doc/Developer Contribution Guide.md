# Developer Contribution Guide for Rabadon’s Grimoire

## Introduction
	
Welcome to Rabadon’s Grimoire developer guide! This document aims to provide all the necessary information for you to get started with contributing to our project. Our application runs on an AWS EC2 instance with Ubuntu. Utilizing Apache2, Python3, Django, and is distributed as an executable file.

## Accessing the Project

### System Requirements:
Before accessing the project, ensure you have the following installed:
-	Git: For version control.
-	Python 3.x: As our primary programming language.
-	Django: Our web framework.
-	Apache2
-	PIP: To manage Python packages.

### Local Setup:
-	Clone the Repository in terminal:
    -	git clone https://github.com/Hunter-Grimes/Rabadon-s-Grimoire.git
    -	cd Rabadon-s-Grimoire
-	Set up a new branch:
    -	git checkout -b ‘feature/new-features’
-	Install required Python dependencie:s
    -	cd Rabadon-s-Grimoire/backend/requirements.txt
    -	pip install -r requirements.txt
-	Set up environment variables required for local development
    -	export DEBUG = True  
export ALLOWED_HOSTS=['184.73.76.247', ‘www.rabadonsgrimoire.com’, ‘rabadonsgrimoire.com’, 127.0.0.1]
export DATABASE_NAME=BASE_DIR / db.sqlite3
-	Database Setup:
    -	python manage.py migrate
-	Run Development Server:
    -	python manage.py runserver



### Making Changes:
-	Code Modifications:
    -	Make changes or add new features to codebase, follow coding standards
    -	If adding new functionality, update or create new Django models, view, templates as necessary
-	Static Files:
    -	Manage static files appropriately in your development and ensure they are properly collected in production setups with					 ‘python manage.py collect static’

### Testing Changes:
-	Run Tests to make sure it does not break functionality
    -	python manage.py test

### Contributing Changes:
-	Commit Changes:
    -	git add . 
    -	git commit -m “Add a detailed message”
-	Push to your GitHub branch:
    -	G git push origin ‘feature/new-features’
-	Create Pull Request:
    -	Go to GitHub repository and create a pull request from your feature branch to the main branch. Provide a description of changes and other relevant information
-	Code Review:
    -	Participate in the code review process
-	Merge Changes:
    -	Once your pull request has been approved, it can be merged into the main branch by a project maintainer.

### Conclusion:
Thank you for contributing to Rabadon’s Grimoire! We value your effort to improve the project and look forward to seeing your contributions.

