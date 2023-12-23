import streamlit as st
from PIL import Image
import requests
import google.generativeai as genai
import google.ai.generativelanguage as glm
import io
import json
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import webbrowser

# components.html(open("index.html").read(), height=600)


# html_string = '''

# <script>
#     async function connectWallet() {
#         try {
#             // Check if Petra Wallet is available
#             if (window.petraWallet) {
#                 // Request connection to the user's Petra Wallet
#                 // Replace 'requestConnection' with the actual method
#                 const accounts = await window.petraWallet.requestConnection();
                
#                 if (accounts.length > 0) {
#                     // Successfully connected, accounts[0] is the user's address
#                     document.getElementById('wallet-result').innerText = 'Wallet Connected: ' + accounts[0];
#                 } else {
#                     document.getElementById('wallet-result').innerText = 'No accounts found. Please connect your wallet.';
#                 }
#             } else {
#                 document.getElementById('wallet-result').innerText = 'Petra Wallet is not installed.';
#             }
#         } catch (error) {
#             console.error('An error occurred:', error);
#             document.getElementById('wallet-result').innerText = 'Error connecting to Petra Wallet: ' + error.message;
#         }
#     }
#     </script>

#     <button onclick="connectWallet()">Connect to Petra Wallet</button>
#     <p id="wallet-result"></p>

# '''

# components.html(html_string)

selected = option_menu(
    menu_title=None,
    options=["Main","Chat"],
    menu_icon=['house', 'chat-dots'],
    orientation="horizontal")



API_URL = st.secrets["Hf_model"]
headers = {"Authorization": st.secrets["Auth_Hf_Key"]}





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


if (selected=="Main"):


   def ai_art(payload):
      response = requests.post(API_URL, headers=headers, json=payload)
      return response.content



   genai.configure(api_key= st.secrets["Google_API_Key"])

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
  
      image=Image.open(uploaded_file)
      st.image(image)
      if "image_bytes" in globals():
         chat_message = "From the provided food item, Please do identify the food and also do classify whether it's healthy or unhealthy. Also one more XP_Points as the parameter in between (1-10), the more healthier food would assign more XP and more unhealthier woulld be lesser value Provide the response in the json format. For Example - {name:'Paneer Mutter', status:'Unhealthy'}"
         vision_message = [chat_message, Image.open(io.BytesIO(image_bytes))]
         result = get_response(vision_message, model="gemini-pro-vision")
         # st.write(result)
      res_text = ""
      for chunk in result:
         res_text += chunk.text
         st.markdown(res_text)
         # st.write(type(res_text))
         res_text1=str(res_text)
         food=json.loads(res_text)
         n=str(food["name"])
         s=str(food["status"])
         # st.write(n)
         # st.write(s)



      # data = json.loads(res_text)
      # name = data["name"]
      prompt = f"Amazing photo of the Indian Food - Panner Mutter, intricate detail, 8k resolution, studio light, michelin art kitchen style --v 5. 0, 4k --ar 1:2 --quality 2"
      image_bytes1 = ai_art({
      "inputs": prompt,
      })

      art = Image.open(io.BytesIO(image_bytes1))
      st.image(art)
      # placeholder = st.empty()

      # Add a button to the placeholder
      # placeholder.button("Prepare One Claim Now!")
      if st.button('Prepare One Claim Now!'):
      # Open the URL in a new browser tab
         webbrowser.open('http://localhost:3000', new=2)

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



if (selected=="Chat"):
      
   select_model = "gemini-pro"
   if select_model == "gemini-pro-vision":
         uploaded_image = st.file_uploader(
               "upload image",
               label_visibility="collapsed",
               accept_multiple_files=False,
               type=["png", "jpg"],
         )
         st.caption(
               "Note: The vision model gemini-pro-vision is not optimized for multi-turn chat."
         )
         if uploaded_image:
               image_bytes = uploaded_image.read()

   def get_response(messages, model="gemini-pro"):
      model = genai.GenerativeModel(model)
      res = model.generate_content(messages, stream=True,
                                 safety_settings={'HARASSMENT':'block_none'})
      return res

   if "messages" not in st.session_state:
      st.session_state["messages"] = []
   messages = st.session_state["messages"]

   if messages and select_model != "gemini-pro-vision":
      for item in messages:
         role, parts = item.values()
         if role == "user":
               st.chat_message("user").markdown(parts[0])
         elif role == "model":
               st.chat_message("assistant").markdown(parts[0])

   chat_message = st.chat_input("Say something")

   if chat_message:
      st.chat_message("user").markdown(chat_message)
      res_area = st.chat_message("assistant").empty()

      if select_model == "gemini-pro-vision":
         if "image_bytes" in globals():
               vision_message =  [chat_message, Image.open(io.BytesIO(image_bytes))]
               res = get_response(vision_message, model="gemini-pro-vision")
         else:
               vision_message = [{"role": "user", "parts": [chat_message]}]
               st.warning("Since there is no uploaded image, the result is generated by the default gemini-pro model.")
               res = get_response(vision_message)
      else:
         messages.append(
               {"role": "user", "parts":  [chat_message]},
         )
         res = get_response(messages)

      res_text = ""
      for chunk in res:
         res_text += chunk.text
         res_area.markdown(res_text)

      if select_model != "gemini-pro-vision":
         messages.append({"role": "model", "parts": [res_text]})
