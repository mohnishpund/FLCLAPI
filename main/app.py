# from flask import Flask

# from flask_cors import CORS, cross_origin

# app = Flask(__name__)
# CORS(app)



from flask import Flask
from flask_cors import CORS

# 1. Create the app
app = Flask(__name__)
CORS(app)

# 2. IMPORT YOUR ROUTES HERE
# This tells Flask to read for_get_emp.py and register the /employee URL
import for_get_emp 
import upload_data
import register
import login
import is_log_in
import logout

# 3. Start the server
if __name__ == '__main__':
    app.run(debug=True)