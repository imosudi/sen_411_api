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
## Sample User Authentication -Failed :
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

## Sample User Authentication -Successful :

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
  "password": "nopassword"
}
```

RESPONSE:
```json
{
  "data": {
    "authenticateAppUser": {
      "error": false,
      "successMsg": true,
      "message": "success",
      "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzMyMzA5NTQ3LCJuYmYiOjE3MzIzMDk1NDcsImp0aSI6IjU3OTVlYTdkLTJmOTItNGFlZS05OTI0LWVhMDlhMjMyMDczMiIsImlkZW50aXR5IjoiaW1vc3VkaUBnbWFpbC5jb20iLCJleHAiOjE3MzIzMTAxNDd9.lFNU-tNiOK13h5dwrchOCGZH9Vpx4dB32KzqvO2Ug84",
      "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoicmVmcmVzaCIsImlhdCI6MTczMjMwOTU0NywibmJmIjoxNzMyMzA5NTQ3LCJqdGkiOiI5MTkwYTc3Ni1hNTYwLTQ0N2MtODc1MC1iYTFkNmVkMTg1MjkiLCJpZGVudGl0eSI6Imltb3N1ZGlAZ21haWwuY29tIiwiZXhwIjoxNzMyNTY4NzQ3fQ.DaVBEeRPQnpr7oLwdI0oClLrB7nDJ3BiS9QehlhfsBM"
    }
  }
}
```

## Sample Secure Query with JWT Access token from a successful authentication :

QUERY:
```graphql
query($token:String!){
  allUsers(
    token:	$token
  ){
    edges{
      node{
        email
      }
    }
  }
}
```

QUERY VARIABLES:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzMyMzA5NTQ3LCJuYmYiOjE3MzIzMDk1NDcsImp0aSI6IjU3OTVlYTdkLTJmOTItNGFlZS05OTI0LWVhMDlhMjMyMDczMiIsImlkZW50aXR5IjoiaW1vc3VkaUBnbWFpbC5jb20iLCJleHAiOjE3MzIzMTAxNDd9.lFNU-tNiOK13h5dwrchOCGZH9Vpx4dB32KzqvO2Ug84"
}
```

RESPONSE:
```json
{
  "data": {
    "allUsers": {
      "edges": [
        {
          "node": {
            "email": "imosudi@gmail.com"
          }
        },
        {
          "node": {
            "email": "imosudi@outlook.com"
          }
        }
      ]
    }
  }
}
```

## Sample Secure Mutation with JWT Access token from a successful authentication :

QUERY:
```graphql
mutation($studentdatainput: studentDataInput!, $token:String!){
  addStudentData(
    token:	$token
    studentdatainput: $studentdatainput
  ){
    error
    message
    successMsg
  }
}
```

QUERY VARIABLES:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzMyMzA5NTQ3LCJuYmYiOjE3MzIzMDk1NDcsImp0aSI6IjU3OTVlYTdkLTJmOTItNGFlZS05OTI0LWVhMDlhMjMyMDczMiIsImlkZW50aXR5IjoiaW1vc3VkaUBnbWFpbC5jb20iLCJleHAiOjE3MzIzMTAxNDd9.lFNU-tNiOK13h5dwrchOCGZH9Vpx4dB32KzqvO2Ug84",
  "studentdatainput": {
    "email": "imosudi@outlook.com",
    "gender": "Male",
    "firstName": "Isiaka",
    "lastName": "Mosudi",
    "middleName": "Olukayode",
    "matricNumber": "22/34567",
    "phoneNumber": "08053673498",
    "enrollmentYear": 2022,
    "level": 600,
    "address": "Block A",
    "department": "Department of Software Engineering",
    "faculty": "Natural and Applied Science"
  }
}
```

RESPONSE:
```json
{
  "data": {
    "addStudentData": {
      "error": false,
      "message": "Student Isiaka Mosudi successfully registered.",
      "successMsg": true
    }
  }
}
```

## Student data Secure Query with JWT Access token from a successful authentication :

QUERY:
```graphql
query($token:String!){
  allStudentRecord(
    token:$token
  ){
    edges{
      node{
        email
        matricNumber
        firstName
        middleName
        lastName
        phoneNumber
        level
        enrollmentYear
        department
        faculty
        gender
      }
    }
  }
}
```

QUERY VARIABLES:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0eXBlIjoiYWNjZXNzIiwiaWF0IjoxNzMyMzA5NTQ3LCJuYmYiOjE3MzIzMDk1NDcsImp0aSI6IjU3OTVlYTdkLTJmOTItNGFlZS05OTI0LWVhMDlhMjMyMDczMiIsImlkZW50aXR5IjoiaW1vc3VkaUBnbWFpbC5jb20iLCJleHAiOjE3MzIzMTAxNDd9.lFNU-tNiOK13h5dwrchOCGZH9Vpx4dB32KzqvO2Ug84"
}
```

RESPONSE:
```json
{
  "data": {
    "allStudentRecord": {
      "edges": [
        {
          "node": {
            "email": "imosudi@gmail.com",
            "matricNumber": "22/34566",
            "firstName": "Isiaka",
            "middleName": "Olukayode",
            "lastName": "Mosudi",
            "phoneNumber": "08053673498",
            "level": 600,
            "enrollmentYear": 2022,
            "department": "Department of Software Engineering",
            "faculty": "Natural and Applied Science",
            "gender": "Male"
          }
        },
        {
          "node": {
            "email": "imosudi@outlook.com",
            "matricNumber": "22/34567",
            "firstName": "Isiaka",
            "middleName": "Olukayode",
            "lastName": "Mosudi",
            "phoneNumber": "08053673498",
            "level": 600,
            "enrollmentYear": 2022,
            "department": "Department of Software Engineering",
            "faculty": "Natural and Applied Science",
            "gender": "Male"
          }
        }
      ]
    }
  }
}
```