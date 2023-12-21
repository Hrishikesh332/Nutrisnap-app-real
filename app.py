import streamlit as st
from PIL import Image
import requests


API_KEY = st.secrets["API_KEY"]

API_URL = "https://api-inference.huggingface.co/models/rajistics/finetuned-indian-food"
headers = {"Authorization": API_KEY}



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


def query(uploaded_file):
   data = uploaded_file.read()
   response = requests.post(API_URL, headers=headers, data=data)
   return response.json()



with st.form(key='my_form'):
   uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png'])
   submit = st.form_submit_button("Submit")

# with st.form(key='my_form2'):
#    uploaded_file = st.camera_input("Take a picture")
#    submit = st.form_submit_button("Submit")



if submit and uploaded_file is not None:
   image = Image.open(uploaded_file)
   st.image(image, caption='Uploaded Image')
   output = query(uploaded_file)
   st.write(output)



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


