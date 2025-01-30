from flask import Flask,render_template,request, redirect, url_for,jsonify
import google.generativeai as genai
from PIL import Image
import base64
import io
import os
my_api_key_gemini = "AIzaSyA22w3Zy6D5-6sN116iLdvsv-FY6fHzxpc"
genai.configure(api_key=my_api_key_gemini)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['uploadInput']
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        # Ensure correct mime type based on file extension
        if uploaded_file.filename.endswith('.jpg') or uploaded_file.filename.endswith('.jpeg'):
            mime_type = 'image/jpeg'
        elif uploaded_file.filename.endswith('.png'):
            mime_type = 'image/png'
        else:
            return jsonify(error='Unsupported file format'), 400
        
        # Encode image to base64 for sending to API
        buffered = io.BytesIO()
        image.save(buffered, format=image.format)
        encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        image_parts = [{
            "mime_type": mime_type,
            "data": encoded_image
        }]
        
        input_prompt = """

        I am building a dietary tracking app. I will provide an image of food, and I need you to:
        1. Identify all the visible food items in the image.
        2. Estimate the serving size for each food item based on standard portions (e.g., "1 cup cooked pasta," "150g grilled chicken").
        3. Provide the Glycemic Index (GI) for each food item.
        4. Calculate the Glycemic Load (GL) for each food item using the formula: GL = (GI × Carbohydrate Content in grams) / 100. Assume approximate carbohydrate content based on standard serving sizes.
        5. Summarize the results in a structured format.
        
        """
 

        # Simulate API response (replace with actual API call)
        model1 = genai.GenerativeModel('gemini-1.5-flash')
        response = model1.generate_content([input_prompt, image_parts[0]])
        result = response.text

        return jsonify(result=result, image=encoded_image)
    
    return jsonify(error='No file uploaded'), 400

if __name__ == "__main__":
    app.run(debug=True)         
    