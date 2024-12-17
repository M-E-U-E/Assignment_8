# Assignment08


## Table of Contents
- [Description](#description)
- [Git Clone Instructions](#git-clone-instructions)
- [Test](#test)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Code Coverage](#code_coverage)
- [Code Coverage Report](#code_coverage_report)
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

    # Activate virtual environment
    # Create virtual environment On Windows:
       python -m venv env
       venv\Scripts\activate

    
    ```
    Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```
    **Run In docker**
    ```
    docker-compose up --build
    ```
    After set up the docker
    Go to new terminal the run this code to open psql db
    ```
    docker exec -it assignment_8-db-1 psql -U username -d hotel_db
    ```
    ```
    \dt [list of the tables]
    SELECT * FROM hotels; [see all hotels]
    SELECT * FROM hotels LIMIT 10; [only show 10 hotels]
    \q for exit


   



## Test
  Run the testing file:
  Ensure the coverage is install:
   ```
   pip install coverage
   ```
   Check the version:
   ```
   coverage --version
   ```

   ```
   coverage run --source=trip -m unittest discover -s tests
   ```
  See report in terminal:
   ```
   coverage report -m
   ```
  Run the testing html:
   ```
   coverage html
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

## Code Coverage Report
```
| **File**                                | **Statements** | **Missing** | **Coverage** | **Missing Lines**                          |
|-----------------------------------------|---------------:|------------:|-------------:|-------------------------------------------|
| `trip/__init__.py`                      | 0             | 0          | 100%         | -                                         |
| `trip/db/__init__.py`                   | 0             | 0          | 100%         | -                                         |
| `trip/db/database.py`                   | 10            | 0          | 100%         | -                                         |
| `trip/db/models.py`                     | 17            | 0          | 100%         | -                                         |
| `trip/items.py`                         | 16            | 0          | 100%         | -                                         |
| `trip/middlewares.py`                   | 0             | 0          | 100%         | -                                         |
| `trip/pipelines.py`                     | 38            | 22         | 42%          | 52-55, 59-62, 72-73, 78-79, 82-104         |
| `trip/settings.py`                      | 10            | 0          | 100%         | -                                         |
| `trip/spiders/__init__.py`              | 0             | 0          | 100%         | -                                         |
| `trip/spiders/async_trip_spider.py`     | 126           | 63         | 50%          | 31-49, 53-54, 65-81, 87-115, 141-142, 152-154, 181, 209-214, 220-229, 238-239 |
| **TOTAL**                               | **217**       | **85**     | **61%**      | -                                         |
  
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
