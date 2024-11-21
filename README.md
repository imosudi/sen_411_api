# sen_411_api
A basic startup point for API development

## Clone the Repository
```bash
git clone https://github.com/imosudi/sen_411_api.git
cd sen_411_api/
```

## Create .env File
```bash
touch app/.env
```

```bash
cat <<EOT > app/.env
API_DB_HOST="db-hostname-or-IP-address"
API_DB_USER="graphqlapidb"
API_DB_PASS="theweekPasswordthatmustbereplaced"
API_DB_NAME="graphqlapidb"
API_FLASK_SECRET="verydifficult-secret-key-goes-here-thismustbereplacedinproduction"
JWT_SECRET_KEY="anotherverydifficult-secret-key-goes-here-alsomustbereplacedinproduction"
EOT
```

## Create and Activate Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```
Install Required Libraries
```bash
pip install -r requirements.txt
```
## Database Initialisation
```bash
flask db init
flask db migrate       # Run this after every modification of app/models.py
flask db upgrade       # Run this after every modification of app/models.py
```

## Start the API
```bash
python main.py
```

## Access the Web Interface

Visit http://localhost:8091

## Sample User Enrolment:
Visit: http://localhost:8091/api_mutation or http://machine-IP:8091/api_mutation

QUERY:
```graphql
mutation($enrolmentappuserinput: enrolmentAppUserInput!){
  enrolAppUser(
    enrolmentappuserinput:$enrolmentappuserinput
  ){
    error
    successMsg
    message
  }
}
```

QUERY VARIABLES:
```json
{
  "enrolmentappuserinput": {
    "email": "imosudi@gmail.com",
    "password": "nopassword",
    "passwordConfirm": "nopassword"
  }
}
```

RESPONSE:
```json
{
  "data": {
    "enrolAppUser": {
      "error": false,
      "successMsg": true,
      "message": "Registration for imosudi@gmail.com, successful! "
    }
  }
}
```

## Sample User Authentication:
Visit: http://localhost:8091/api_mutation or http://machine-IP:8091/api_mutation

QUERY:
```graphql
mutation ($email: String!$password: String!) {
  authenticateAppUser(
  	email: $email
    password: $password
  ) {
    error
    successMsg
    message
    accessToken
    refreshToken
  }
}
```

QUERY VARIABLES:
```json
{
  "email": "imosudi@gmail.com",
	"password": "nopasswordssddff"
}
```

RESPONSE:
```json
{
  "data": {
    "authenticateAppUser": {
      "error": true,
      "successMsg": false,
      "message": "Bad username or password! Kindly login with approved login details or request for user activation",
      "accessToken": null,
      "refreshToken": null
    }
  }
}
```