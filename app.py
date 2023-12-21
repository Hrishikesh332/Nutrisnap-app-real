import streamlit as st
from PIL import Image
import requests
import google.generativeai as genai
import google.ai.generativelanguage as glm
import io
import cv2
import json


API_URL = st.secrets["Hf_model"]
headers = {"Authorization": st.secrets["Auth_Hf_Key"]}



def ai_art(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content


genai.configure(api_key=st.secrets["Google_API_Key"])

page_element="""
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://wallpapercave.com/wp/wp3589963.jpg");
background-size: cover;
}
[data-testid="stHeader"]{
background-color: rgba(0,0,0,0);
}
[data-testid="stToolbar"]{
right: 2rem;
background-image: url("");
background-size: cover;
}
[data-testid="stSidebar"]> div:first-child{
background-image: url("https://img.freepik.com/premium-vector/skyblue-gradient-background-advertisers-gradient-hq-wallpaper_189959-513.jpg");
background-size: cover;
}
</style>

"""
st.markdown(page_element, unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center;';>NutriSnap 🌿</h1>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
  st.title("NutriSnap - Your Healthy Habits, Rewarded!")
  st.markdown("Welcome to NutriSnap, the app that rewards your healthy habits with NFTs!")
  st.info('Capture a photo of your food intake and let our AI model predict its healthiness.')
  st.markdown("More healthy food, more XP on your NFT!")
  st.toast("Stay tuned for more exciting features and rewards!")

with col2:
  st.image('logo.png', use_column_width=True)

st.markdown("---")
st.markdown("Upload a photo of your food intake and get rewarded with NFTs!")

def get_response(vision_message, model="gemini-pro"):
   
    model = genai.GenerativeModel(model)
    res = model.generate_content(vision_message, stream=True,
                                safety_settings={'HARASSMENT':'block_none'})
    return res

    
# # def query(uploaded_file):
#    data = uploaded_file.read()
#    response = requests.post(API_URL, headers=headers, data=data)
#    return response.json()



# with st.form(key='my_form2'):
#    uploaded_file = st.camera_input("Take a picture")
#    submit = st.form_submit_button("Submit")



# uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png'])

uploaded_file = st.file_uploader(
            "upload image",
            label_visibility="collapsed",
            accept_multiple_files=False,
            type=["png", "jpg"],
        )

if uploaded_file:
            image_bytes = uploaded_file.read()


if uploaded_file is not None:
   img = cv2.imread(uploaded_file.name)
   image=Image.open(uploaded_file)
   st.image(image, caption='Uploaded Image')
   if "image_bytes" in globals():
      chat_message = "From the provided food item, Please do identify the food and also do classify whether it's healthy or unhealthy. Provide the response in the json format. For Example - {name:'Paneer Mutter', status:'Unhealthy'}"
      vision_message = [chat_message, Image.open(io.BytesIO(image_bytes))]
      result = get_response(vision_message, model="gemini-pro-vision")
      # st.write(result)
   res_text = ""
   for chunk in result:
        res_text += chunk.text
        st.markdown(res_text)



   # data = json.loads(res_text)
   # name = data["name"]
   prompt = f"Amazing photo of the Indian Food - Panner Mutter, intricate detail, 8k resolution, studio light, michelin art kitchen style --v 5. 0, 4k --ar 1:2 --quality 2"
   image_bytes1 = ai_art({
	"inputs": prompt,
   })

   art = Image.open(io.BytesIO(image_bytes1))
   st.image(art)


    # healthiness = predict_healthiness(image)

    # st.write(f"The food is {'healthy' if healthiness > 0.5 else 'unhealthy'}")
    # st.write(f"You earned {healthiness} XP on your NFT!")

col3, col4 = st.columns(2)

with col3:
   st.title("Use Your NFTs as Coupons for Health Services")
   st.markdown("NFTs can be used as coupons to avail various health services. Here are some of the services you can avail using your NFTs:")
   st.markdown("1. **Health Checkups** - Use your NFTs to avail health checkups at discounted rates.")
   st.markdown("2. **Nutrition Counseling** - Get personalized nutrition counseling for your healthy habits.")
   st.markdown("3. **Fitness Classes** -  Attend fitness classes at a reduced cost using your NFTs.")
   st.markdown("4. **Diet Food Services** -  Get personalized discount on the Keto Diet Plans from vendors.")


with col4:
   st.image('photo.jpg', use_column_width=True)
#    st.markdown("""<img src="photo.jpg" style="border-radius: 20px;" />""", unsafe_allow_html=True)


