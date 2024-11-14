# from flask import Flask,request, jsonify
# import util

# app = Flask(__name__)

# # @app.route("/", methods=["GET"])
# # def home():
# #     return "Welcome to the home page!"

# @app.route('/classify_image', methods=['GET', 'POST'])
# def classify_image():
#     image_data = request.form['image_data']
    
#     response = jsonify(util.classify_image(image_data))
    
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing

    
#     return response

# if __name__ == "__main__":
#     print("Starting Python Flask Server For Sports Celebrity Image Classification")
#     util.load_saved_artifacts()
#     app.run(port=5000)




# from flask import Flask, request, jsonify, make_response
# import util

# app = Flask(__name__)

# @app.route('/classify_image', methods=['POST'])
# def classify_image():
#     image_data = request.form['image_data']
    
#     # Assuming util.classify_image returns a JSON-serializable object
#     classification_result = util.classify_image(image_data)
    
#     # Create the JSON response
#     response = make_response(jsonify(classification_result))
    
#     # Add security headers
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing
    
#     return response

# if __name__ == "__main__":
#     print("Starting Python Flask Server For Sports Celebrity Image Classification")
#     util.load_saved_artifacts()
#     app.run(port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)  # Enable CORS globally for all routes

@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Sports Celebrity Image Classification API!"

@app.route('/classify_image', methods=['GET', 'POST'])
def classify_image():
    image_data = request.form.get('image_data')  # Use get() to avoid KeyError
    if not image_data:
        return jsonify({"error": "No image data provided"}), 400  # Return 400 if image data is missing

    try:
        result = util.classify_image(image_data)
        response = jsonify(result)
        response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return 500 if an internal error occurs

if __name__ == "__main__":
    print("Starting Python Flask Server For Sports Celebrity Image Classification")
    util.load_saved_artifacts()
    app.run(port=5000, debug=True)  # Enable debug mode for development
