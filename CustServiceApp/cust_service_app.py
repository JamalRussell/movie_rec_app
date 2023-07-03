import openai
import json
import streamlit as st

openai.api_key = "api_key"

delimiter = "####"

system_message_1 = f"""You are a helpful customer service assistant for a large electronics store.
You are dedicated to providing customers with information on products carried by the store, and
answer customer queries in a polite tone.

Below are a list of products, separated by category. Examine the query for specific products, as
well as product categories. If any of either are found in the query, match them to the appropriate
product and/or category from the list below and output your findings as a Python list array. Do
not output anything other than the list. If no products or categories are found, output an empty
list.

Products:

Computers and Laptops:
TechPro Ultrabook
BlueWave Gaming Laptop
PowerLite Convertible
TechPro Desktop
BlueWave Chromebook

Smartphones and Accessories:
SmartX ProPhone
MobiTech PowerCase
SmartX MiniPhone
MobiTech Wireless Charger
SmartX EarBuds

Televisions and Home Theater Systems:
CineView 4K TV
SoundMax Home Theater
CineView 8K TV
SoundMax Soundbar
CineView OLED TV

Gaming Consoles and Accessories:
GameSphere X
ProGamer Controller
GameSphere Y
ProGamer Racing Wheel
GameSphere VR Headset

Audio Equipment:
AudioPhonic Noise-Canceling Headphones
WaveSound Bluetooth Speaker
AudioPhonic True Wireless Earbuds
WaveSound Soundbar
AudioPhonic Turntable

Cameras and Camcorders:
FotoSnap DSLR Camera
ActionCam 4K
FotoSnap Mirrorless Camera
ZoomMaster Camcorder
FotoSnap Instant Camera"""

with open("products.json") as json_file:
    products = json.load(json_file)

system_message_2 = f"""You are a helpful customer service assistant for a large electronics store.
You are dedicated to providing customers with information on products carried by the store, and
answer customer queries concisely in a polite tone. You make sure to ask customers relevant follow
up questions when answering their queries.

After answering the user query, check your response against the product information and ensure
that the response as a whole discusses said products honestly. If so, output the response to the
user. If not, output "Sorry, but we could not find the information you were asking for. Please try
again." to the user."""

def customer_service_chain(query):
    message_1 = [{"role": "system", "content": system_message_1},
                  {"role": "user", "content": f"{delimiter}{query}{delimiter}"}]
    response = openai.ChatCompletion.create(messages=message_1, model="gpt-3.5-turbo",
                                             temperature=0.0, max_tokens=500)
    product_list = response.choices[0].message["content"]
    
    new_list = product_list.replace("[", "").replace("]", "").replace("'", "").replace('"', "").split(", ")
    
    product_information = []

    if new_list == []:
        return product_information
    
    for item in new_list:
        for key, val in products.items():
            if item == key:
                product_information.append(val)
            else:
                if item == val["category"]:
                    product_information.append(val)
                    
    message_2 = [{"role": "system", "content": system_message_2},
                  {"role": "user", "content": f"{delimiter}{query}{delimiter}"},
                  {"role": "assistant", "content": f"Relevant product information: {product_information}"}]
    response_2 = openai.ChatCompletion.create(messages=message_2, model="gpt-3.5-turbo",
                                               temperature=0.0, max_tokens=500)
    final_response = response_2.choices[0].message["content"]
    final_response

description = """This is an app designed to provide information regarding a large consumer
electronics store's products. Please enter your query below to get information on the products
of your choice. The more focused and specific your query is, the more focused and specific the
information returned will be. The nature of your query will also affect how quickly the output
is returned; keep this in mind when formulating your questions."""

st.title("Customer Service App")
st.markdown(description)
query = st.text_input("Query:", key="query")

if st.session_state.query:
    result = customer_service_chain(query)
    st.write(result)
