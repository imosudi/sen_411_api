# sen_411_api
A basic startup point for API development

# Clone repo    
 git clone https://github.com/imosudi/sen_411_api.git   

 cd sen_411_api/    


# Create app/.env file
 touch app/.env     
 API_DB_HOST="db-hostname-or-IP-address"
 API_DB_USER="graphqlapidb"
 API_DB_PASS="theweekPasswordthatmustbereplaced"
 API_DB_NAME="graphqlapidb"

 API_FLASK_SECRET='verydifficult-secret-key-goes-here'


# Create and activate Python virtual environment
 python3 -m venv venv
 source venv/bin/activate
 
# Install required libraries 
 pip install -r requirements.txt 

# Database initialisation
 flask db init
 flask db migrate   #run thia after every modification of app/models.py
 flask db upgrade   #run thia after every modification of app/models.py

# Start the API
 python main.py 

# Access the web interface
 http://localhost:8091