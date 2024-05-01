# Website
### Overview
 Unlike the frontend and backend explanations this won't be a file by file explanation as the way the website works can be completely changed if needed, as though it serves as the first thing possible users will see, our product is the Rabadon's Grimore app. Thus this file will explain the main parts of the site. 
 For a quick on what the role website is, visit the [Getting Started](./Technical.md) file.
### AWS EC2 
- to host our Rabadon’s Grimoire since it was a dynamic website due to the login and signup feature

### Ubuntu:
- Ubuntu provided a development environment for our team. It supports a wide range of pre-built languages and frameworks, which allows us to use Docker containers directly. Django also uses a Python3 framework to handle our web traffic and data processing.
- #### Python3 is used for: 
    -  URL Routing: Define URL patterns and routing. Each URL is associated with a view that handles incoming requests and returns responses.
    - Views: Python3 functions receive web requests and return responses, such as querying the Django database to process form data.
    - Models: Defined in Python3, describe our data schema to create database tables and methods that define business logic related to that data.

### Django:
-We used Django to implement our Login and Signup feature. It was a pre-built package that allowed us to keep track of our user authentication, and user database and also gave us a pre-built admin page for our site.

### Apache2:
-We used Apache2 to serve web pages to clients. It handles requests from users' browsers and provides them with the requested HTML pages and CSS styles. Apache2 also supports HTTPS which is critical for secure connections over the internet, to prevent any malicious attempts on our website.