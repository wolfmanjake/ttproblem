Requirements:
python 3.6
python3-psycopg2
python3-pip
postgresql (installed and running, postgres account password set to superduper)
postgresql-contrib

Steps:
1. Install and configure requirements listed above.
2. pip install flask-restplus
3. download the csv to the project directory
4. run python3.6 loaddata.py
5. run python3.6 ttproblem.py
6. Make HTTP calls to http://${my_server_ip}:7777/organizations
7. Point browser to http://${my_server_ip}:7777 for swagger documentation

TODO:
- Automate build and deployment
    - build a python egg
    - script bringing up a docker container and installing requirements
    - script deploying the egg and starting the server
- Implement API tests
- Implement Unit tests and integrate into build
    - unit test generate_query string with all of the combinations of parameters and check the query string
    - mock the db and unit test query_db with of the combinations of parameters and check return
- Performance tests and enhancements
- use a real logger with log levels and rollover
- use a production WSGI server
- trim white spaces on import/input as trimming at retrieval time is not good for performance
- add authentication/security
- refactor into separate classes when we add more API's for read-ability
