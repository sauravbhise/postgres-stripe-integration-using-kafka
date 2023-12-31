# Deployment Instructions 

Prerequisites: Docker, localtunnel

1. Clone this repository to your local machine

    `git clone git@github.com:sauravbhise/zenskar-assignment.git`

2. Open this project directory

    `cd zenskar-assignment`

3. Spin up the required docker containers using docker-compose

    `docker-compose -f docker-compose.yml up`

4. Open bash on the PostgreSQL container and launch PostgreSQL

    `docker exec -it zenskar-assignment-postgres-1 bash`

    `psql -U docker -d zenskar -W`

    You will then be prompted to enter the password (the default is: `docker`)

5. Once you are in PostgreSQL create the customers table

    ```
    CREATE TABLE customers (
    ID VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
    );
    ```

6. Alter the table's replica identity so Debezium can read changes

    `ALTER TABLE public.customers REPLICA IDENTITY FULL`

7. Now head over to [Stripe](https://stripe.com/) to create a free test account. 

8. Launch a new terminal window & cd into the zenskar-assignment dir and then run the following command to create the Debezium Connector

   `cd zenskar-assignment`

    `curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" http://localhost:8083/connectors/ -d @register-mysql.json`

10. cd into the api directory & install the required packages

    `cd api`

    `pip install -r requirements.txt`

11. Create a .env file with the details for the database connection

    `nano .env`

    .env

    ```
    DATABASE_NAME=zenskar
    DATABASE_USER=docker
    DATABASE_PASSWORD=docker
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    ```
     
12. Run the DB interaction api using the following command

    `python app.py`

13. cd into the kafka-consumer directory & install required packages

    `cd ../kafka-consumer`

    `pip install -r requirements.txt`

14. Create a .env file and add your stripe api key

    `nano .env`

    .env
    
    ```
    STRIPE_API_KEY=your_key
    ```

15. Run the consumer using the following command

    `python consumer.py`

16. cd into the webhook directory & install required packages

    `cd ../webhook`

    `pip install -r requirements.txt`

17. Create a .env file and add db connection details & your stripe api key as well as stripe epio secret

    `nano .env`

    .env
    
    ```
    DATABASE_NAME=zenskar
    DATABASE_USER=docker
    DATABASE_PASSWORD=docker
    DATABASE_HOST=localhost
    DATABASE_PORT=5432
    STRIPE_API_KEY=your_key
    STRIPE_ENDPOINT_SECRET=your_secret
    ```

18. Run the webhook using the following command

    `flask run --port=4242`

19. Setup a web hook in Stripe for the events: customer.created, customer.updated & customer.deleted

20. Expose port 4242 using localtunnel using the following command

    `lt --port=4242`

This command will provide you with an url that you can add to your Stripe web hook configuration

Now you're good to go! Interact with the database via our API or make changes via the Stripe web interface, your changes will always be in sync!
