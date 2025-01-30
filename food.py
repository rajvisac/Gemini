
# from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# load_dotenv()

my_api_key_gemini = "AIzaSyA22w3Zy6D5-6sN116iLdvsv-FY6fHzxpc"
genai.configure(api_key=my_api_key_gemini)
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def upload(image_parts):
    # uploaded_file = request.files['uploadInput']
    
    if uploaded_file:
    #     image = Image.open(uploaded_file)
        
    #     # Ensure correct mime type based on file extension
    #     if uploaded_file.filename.endswith('.jpg') or uploaded_file.filename.endswith('.jpeg'):
    #         mime_type = 'image/jpeg'
    #     elif uploaded_file.filename.endswith('.png'):
    #         mime_type = 'image/png'
    #     else:
    #         return jsonify(error='Unsupported file format'), 400
        
    #     # Encode image to base64 for sending to API
    #     buffered = io.BytesIO()
    #     image.save(buffered, format=image.format)
    #     encoded_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # image_parts = [{
        #     "mime_type": mime_type,
        #     "data": encoded_image
        # }]
        
        # input_prompt = """

        # I am building a dietary tracking app. I will provide an image of food, and I need you to:
        # 1. Identify all the visible food items in the image.
        # 2. Estimate the serving size for each food item based on standard portions (e.g., "1 cup cooked pasta," "150g grilled chicken").
        # 3. Provide the Glycemic Index (GI) for each food item.
        # 4. Calculate the Glycemic Load (GL) for each food item using the formula: GL = (GI × Carbohydrate Content in grams) / 100. Assume approximate carbohydrate content based on standard serving sizes.
        # 5. Summarize the results in a structured format.
        
        # """
        input_prompt = """

        I am building a dietary tracking app. I will provide an image of food, and I need you to:
        1. Identify all the visible food items in the image.Estimate the serving size for each food item based on standard portions (e.g., "1 cup cooked pasta," "150g grilled chicken").Provide the Glycemic Index (GI) for each food item.Calculate the Glycemic Load (GL) for each food item using the formula: GL = (GI × Carbohydrate Content in grams) / 100. Assume approximate carbohydrate content based on standard serving sizes.Summarize the results and give the output in JSON format only.
        Json format with example: {
  "food_items": [
    {
      "name": "Salmon en Croute",
      "serving_size_g": 150,
      "carbohydrate_content_g": 5,
      "GI_estimate": 50,
      "GL_estimate": 2.5
    },
    {
      "name": "Boiled Potatoes",
      "serving_size_g": 150,
      "carbohydrate_content_g": 30,
      "GI_estimate": 70,
      "GL_estimate": 21
    },
    {
      "name": "Leafy Greens",
      "serving_size_g": 50,
      "carbohydrate_content_g": 5,
      "GI_estimate": 15,
      "GL_estimate": 0.75
    }
  ],
  "totals": {
    "GI_estimate": 135,
    "carbohydrate_content_g": 35,
    "GL_estimate": 24.25
  }
}

        """
 

        # Simulate API response (replace with actual API call)
        model1 = genai.GenerativeModel('gemini-1.5-flash')
        response = model1.generate_content([input_prompt, image_parts[0]])
        result = response.text
        return result


# def get_gemini_repsonse(input,image,prompt):
#     model=genai.GenerativeModel('gemini-pro-vision')
#     response=model.generate_content([input,image[0],prompt])
#     return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


st.header("🤖 Hello, I am Food Genie AI ! 💬")
st.subheader("I can help you to recognize food items from the given image 🤔")

# input=st.text_input("Ask me: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button(" Submit")

input_prompt= """You are an expert in reconizing food items from the Given image, Give some interesting fact related to that food provided in image and calculate the total Calories,fat, protein, carbohydrate, sugar inside that given picture"""
if submit:
    image_data=input_image_setup(uploaded_file)
    # print('Image dataaaa',image_data)
    response=upload(image_data)
    st.subheader("The Response is")
    st.write(response)


