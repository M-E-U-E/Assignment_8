# Assignment08


## Table of Contents
- [Description](#description)
- [Git Clone Instructions](#git-clone-instructions)
- [Access the Application](#access_the_application)
- [Sitemap Generation](#sitemap_generation)
- [Test](#test)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Code Coverage](#code_coverage)
- [Schema](#schema)
- [Authorization Rules](#authorization_rules)
- [Dependencies](#dependencies)
- [Remember](#remember)


## Description

This project scrapes hotel property data from trip.com and stores the collected data into a PostgreSQL database. The application utilizes Scrapy to gather details such as property title, rating, location, latitude, longitude, room type, price, and images. The scraped images are saved in a local directory, and their paths are stored in the database for retrieval.

## Git Clone Instructions

To clone this project to your local machine, follow these steps:

1. **Open terminal (Command Prompt, PowerShell, or Terminal)**

2. **Clone the repository**:
   
         git clone https://github.com/M-E-U-E/Assignment_8.git or git clone git@github.com:M-E-U-E/Assignment_8.git
   
    Go to the Directory:
    ```bash
    cd Assignment_8
    ```
4. **Set Up Virtual Environment**
   
    ```bash
    # Create virtual environment On macOS/Linux:
       python3 -m venv env
       source env/bin/activate
       pip install django
    # Activate virtual environment
    # Create virtual environment On Windows:
       python -m venv env
       venv\Scripts\activate
       pip install django
    
    ```
    Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

5. **Docker Instructions**

    To run the project using Docker, follow these steps:

    Build and Run Docker Containers Ensure you have Docker and Docker Compose installed. Then, use the following commands to build and run the containers:
  ```
      docker compose build
      docker compose up
   ```

   This will start both the PostgreSQL/PostGIS container and the Django application container.
   
   Apply Migrations in Docker After the containers are up, run the migrations inside the Django container:
   ```
   docker exec -it django_web python manage.py makemigrations
   docker exec -it django_web python manage.py migrate
   ```
   
   Create a Superuser in Docker Create a superuser to access the admin panel:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```
   then create superuser
   ```
      Username (leave blank to use 'root'): 
      Email address: 
      Password: 
      Password (again): 
   ```


## Sitemap Generation
   Add locations through json file:
   ```
   docker-compose exec web python manage.py loaddata locations_fixture.json
   ```
   then generate the sitemap
   
   Run this code:
   ```
      docker-compose exec web python manage.py generate_sitemap
   ```
   This will create a sitemap.json containing all property locations.
   
   #### After this we can import or export csv file, json file.


## Test
  Run the testing file:
   ```
      docker-compose run web coverage run manage.py test
   ```
  Run the testing html:
   ```
      docker-compose run web coverage html
   ```
  See the testig html:
   ```
      xdg-open htmlcov/index.html
   ```
    

## Project Structure
```
Assignment_8/
│
├── city_data/                      # Directory for city-related data
├── htmlcov/                        # Code coverage reports
├── tests/                          # Unit tests
│   ├── __init__.py
│   └── test_async_trip_spider.py   # Test for the async Trip Spider
│
├── trip/                           # Main project directory
│   ├── db/                         # Database setup
│   │   ├── __init__.py
│   │   ├── database.py             # Database connection setup
│   │   └── models.py               # SQLAlchemy models
│   │
│   ├── spiders/                    # Scrapy spiders
│   │   ├── __init__.py
│   │   └── async_trip_spider.py    # Spider for scraping trip.com
│   │
│   ├── items.py                    # Scrapy items
│   ├── middlewares.py              # Scrapy middlewares
│   ├── pipelines.py                # Scrapy pipelines
│   └── settings.py                 # Scrapy settings
│
├── venv/                           # Virtual environment
├── .coverage                       # Coverage data
├── .gitignore                      # Ignored files
├── docker-compose.yml              # Docker setup (if applicable)
├── dockerfile                      # Dockerfile for containerization
├── README.md                       # Project guidelines
├── requirements.txt                # Project dependencies
└── scrapy.cfg                      # Scrapy configuration

```
## Technologies Used

- Python: Programming language
- Scrapy: Web scraping framework
- PostgreSQL: Database to store hotel data
- SQLAlchemy: ORM for database interaction
- pytest: Testing framework

  
## Code Coverage  
      Coverage report: 66%
      - Files
        - trip/spiders/async_trip_spider.py
        - tests/test_async_trip_spider.py
        - trip/items.py
        - trip/middlewares.py
        - trip/pipelines.py
        - trip/settings.py
        - trip/db/database.py
        - trip/db/models.py


## Schema
  Database Schema (In-Memory):
  ```
  Users Table:
  +----------+-----------+----------+-------+
  | id       | username  | email    | role  |
  +----------+-----------+----------+-------+
  | string   | string    | string   | string|
  +----------+-----------+----------+-------+

  Accommodations Table:
  +----------+----------+---------------+--------+--------+-------------+----------+----------+------------+------------+
  | id       | feed     | title         | country_code | bedroom_count | review_score | usd_rate | center     | user_id    | published |
  +----------+----------+---------------+--------+--------+-------------+----------+----------+------------+------------+
  | string   | int      | string        | string | int     | decimal     | decimal  | PointField | ForeignKey | bool      |
  +----------+----------+---------------+--------+--------+-------------+----------+----------+------------+------------+

  LocalizeAccommodations Table:
  +----------+---------------+----------+-------------+--------+
  | id       | property_id   | language | description | policy |
  +----------+---------------+----------+-------------+--------+
  | int      | ForeignKey    | string   | text        | JSON   |
  +----------+---------------+----------+-------------+--------+

  Locations Table:
  +----------+--------+-------------+----------+----------------+-------------+----------+----------+------------+------------+
  | id       | title  | center      | parent_id| location_type  | country_code| state_abbr| city     | created_at | updated_at |
  +----------+--------+-------------+----------+----------------+-------------+----------+----------+------------+------------+
  | string   | string | PointField  | ForeignKey| string         | string      | string   | string   | datetime   | datetime   |
  +----------+--------+-------------+----------+----------------+-------------+----------+----------+------------+------------+

  PropertyOwners Table:
  +----------+--------+----------+----------+-------------+------------+
  | id       | name   | email    | phone    | address     | created_at |
  +----------+--------+----------+----------+-------------+------------+
  | string   | string | string   | string   | text        | datetime   |
  +----------+--------+----------+----------+-------------+------------+
```
  

  
 ## Dependencies
  All dependencies are listed in requirements.txt. Install them using:

    pip install -r requirements.txt

  Main dependencies:
  scrapy
  sqlalchemy
  psycopg2
  pytest
  pytest-cov
  
 ### Remember:
    Ensure PostgreSQL is running and properly configured.
    Install all dependencies in a virtual environment.
    Run tests and validate the code coverage before submission.
