# Simple_Flask_Project


A simple and basic a web application using Flask and SQLite created for a software engineering databases course. Developed an api using CRUD practices (GET, POST specifically). Overall, users are able to POST and GET data to and from an sqlite database. Data in database can be accessed via web browser or command line using CURL AFTER initializing server. Also a feature is present where users are able to re-initialized the database (the .sqlite file) via command line using "flask initdb". 



## API Description:
GET /profiles
Description:
Get a list of all profiles formatted in an html file
Parameters:
None

GET /profiles/api
Description:
Get a list of all profiles in json format
Parameters:
None

GET /locations
Description:
Get a list of all locations formatted in an html file
Parameters:
None

GET /locations/api
Description:
Get a list of all locations in json format
Parameters:
None

GET /favorites
Description:
Get a list of all favorites formatted in an html file
Parameters:
None

GET /favorites/api
Description:
Get a list of all favorites in json format
Parameters:
None

POST /
Description:
Add items to profiles, locations, and favorites table
Parameters:
request forms

GET /
Description:
Get html template containing forms for the POST method
Parameters:
None
