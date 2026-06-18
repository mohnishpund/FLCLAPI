from database_conn import get_db_connection
from app import app
from flask import jsonify, request
from werkzeug.utils import secure_filename

from is_log_in import is_logged_in

# 1. Import your isolated cloud connection function
from cloud_conn import upload_image_to_cloud

# Configuration 
app.secret_key = "caircocoders-ednalan"

# 2. Restrict extensions strictly to images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Add post profile picture to cloud storage and update database
@app.route('/emp_profile/<int:employee_id>', methods=['PUT'])
@is_logged_in
def proc_pic(employee_id):
    conn = None
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database is currently offline."}), 500

        # Check if the file part is present in the request
        if 'profile_picture' not in request.files:
            return jsonify({"error": "No profile_picture payload found"}), 400

        _profile_picture = request.files.getlist('profile_picture')
        
        cloud_url = None
        errors = {} 

        for file in _profile_picture:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                content_type = file.content_type
                
                # 3. Upload directly to Cloudinary (No local saving!)
                upload_result = upload_image_to_cloud(file, filename, content_type)
                
                # Check if upload was successful (Cloudinary returns a secure https URL)
                if upload_result.startswith("http"):
                    cloud_url = upload_result
                    break  # Stop after successfully uploading the first valid image
                else:
                    errors[file.filename] = f"Cloud Error: {upload_result}"
            else:
                if file.filename:
                    errors[file.filename] = 'File type is not allowed. Images only.'

        # If there were file validation errors and no successful upload, return them
        if errors and not cloud_url:
            return jsonify({"errors": errors}), 400

        # 4. Update Oracle database using the Cloud URL
        if cloud_url:
            cursor = conn.cursor()
            # We pass the cloud_url directly into the :proc_file bind variable
            sql_orcl_query = """UPDATE EMPLOYEES SET profile_picture = :proc_file WHERE employee_id = :employee_id"""
            bind_data = (cloud_url, employee_id)
            
            cursor.execute(sql_orcl_query, bind_data)
            conn.commit()
            cursor.close()

            return jsonify({
                "Result": "Your profile picture was successfully uploaded to the cloud and database.",
                "Cloud_URL": cloud_url,
                "Employee_ID": employee_id,
                "status": "success"
            }), 200 
            
        else:
            return jsonify({"error": "No valid file uploaded"}), 400

    except Exception as e:
        print('Error adding employee profile picture data:', e)
        return jsonify({"error": "Internal server error occurred"}), 500

    finally:
        if conn:
            conn.close()