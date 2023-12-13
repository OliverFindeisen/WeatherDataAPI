python3 -m venv weather
source venv/bin/activate
pip install flask psycopg2-binary



### Flask 

Flask has a built-in development server and a fast debugger.
Flask provides integrated support for unit testing.
RESTful request dispatching.
Flask support for secure cookies (client-side sessions).
It is WSGI 1.0 compliant.

Advantages:

Flask is a microframework, which provides only the bare essentials for building web applications and APIs. This makes it lightweight, fast, and easy to use.
Flask is designed to be easily extended with third-party libraries and plugins. There are many extensions available for Flask that provide additional functionality such as database integration, authentication, and more.
 Flask includes a built-in development server that makes it easy to test and debug your API during development.
Flask uses the Jinja2 templating engine, which makes it easy to build dynamic and reusable templates for rendering HTML pages or JSON responses.
High Flexibility: The configuration is even more flexible than that of Django, giving you plenty of solutions for every production need.

Disadvantage:

Limited functionality: Flask API is a microframework, which means it provides only the essentials for building web APIs. This can be a disadvantage if you need more complex functionality, as you may need to integrate third-party libraries or plugins.
Steep learning curve: While Flask is easy to learn and use for small projects, it can become more difficult to manage as the application grows in complexity. Developers may need to spend more time managing dependencies and integrating third-party libraries.
No built-in support for database integration: Flask API does not provide built-in support for database integration. Developers need to use third-party libraries like SQLAlchemy to integrate databases with their APIs.
Security vulnerabilities: As with any web framework, Flask API can be vulnerable to security threats like SQL injection or cross-site scripting attacks. Developers need to be aware of these vulnerabilities and take steps to secure their APIs.

### Postgres 

- https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/#install-requirements

### Upload

curl -X POST -F cityname=athens -F file=@weather-athens.csv localhost:8088/upload
curl -X POST -F cityname=berlin -F file=@weather-berlin.csv localhost:8088/upload

### endpointquerys 

A: curl "localhost:8088/endpointa?cityname=berlin&datestring=2021-12-14"
B: curl "localhost:8088/endpointb?cityname=athens&month=10"
C: curl "localhost:8088/endpointc?cityname=berlin&datestring=2021-12-14"
D: curl "localhost:8088/endpointd?cityname=athens&year=2015"



### TODO

#### upload
- check column order



