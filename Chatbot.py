from openai import OpenAI
import json
import streamlit as st
from vertexai.generative_models import (
    Content,
    GenerationConfig,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part,
)

with st.sidebar:
    gemini_api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    PROJECT_ID = st.text_input("Google Cloud Project ID:")
    LOCATION = st.text_input("Google Cloud Location:")
    MODEL_ID = st.selectbox(
    "Please select the base model",
    ("gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro-vision"))
    # "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

# Initialize Vertex AI
import vertexai

vertexai.init(project=PROJECT_ID, location=LOCATION)

#############################################
# Config Model
model = GenerativeModel(MODEL_ID)

#############################################

st.caption("🚀 A Streamlit chatbot powered by Vertex AI Gemini API")

tab1, tab2, tab3 = st.tabs(
    ["Proactive Agent", "Key Sales Agent", "Client Advisor Agent"]
)

with tab1:
    st.subheader(f"""💬 Chatbot with Proactive Agent""", divider="rainbow")

    # if "messages" not in st.session_state:
    #     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])

    # if prompt := st.chat_input(key='proactive-agent'):
    #     if not gemini_api_key:
    #         st.info("Please add your Gemini API key to continue.")
    #         st.stop()

    #     client = OpenAI(api_key=gemini_api_key)
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     st.chat_message("user").write(prompt)
    #     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #     msg = response.choices[0].message.content
    #     st.session_state.messages.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant").write(msg)

with tab2:
    st.subheader(f"""💬 Chatbot with Key Sales Agent""", divider="rainbow")

    # if "messages" not in st.session_state:
    #     st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

    # for msg in st.session_state.messages:
    #     st.chat_message(msg["role"]).write(msg["content"])

    # if prompt := st.chat_input(key='key-sales-agent'):
    #     if not gemini_api_key:
    #         st.info("Please add your Gemini API key to continue.")
    #         st.stop()

    #     client = OpenAI(api_key=gemini_api_key)
    #     st.session_state.messages.append({"role": "user", "content": prompt})
    #     st.chat_message("user").write(prompt)
    #     response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    #     msg = response.choices[0].message.content
    #     st.session_state.messages.append({"role": "assistant", "content": msg})
    #     st.chat_message("assistant").write(msg)

with tab3:
    st.subheader(f"""💬 Chatbot with Client Advisor Agent""", divider="rainbow")

    chat_model = GenerativeModel(
        MODEL_ID,
        system_instruction=[ "You are customer personal assistant who willing the support your customer." 
                            , "You have to recommend or suggest the products that similar to the object in the query image based on product information and product image."
                            , "You should recommend or suggest the products that your customer would like to buy or looking for."
                            , "You have to convince them (not hard selling) to buy the products with special discount or campaign that you think is fit for the customers"
                            , "If that product is not in product list, you can recommend more than one similar product to increase sales chance."
                            , "You have to convince them (not hard selling) to buy the products with special discount or campaign that you think is fit for the customers."
                            , "Rule 1: Alway show image of the product."
                            , "Rule 2: Answer in the same language of customer question."],
        # Set model parameters
        generation_config = GenerationConfig(
            temperature=0.85,
            top_p=1.0,
            # top_k=32,
            candidate_count=1,
            max_output_tokens=2048,
        ),
        # Set safety settings
        # safety_settings = {
        #     HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        #     HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        #     HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        #     HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        # }

    )

    chat = chat_model.start_chat(
    history=[
            Content(role="user", parts=[Part.from_text("My name is Ton.")]),
            Content(role="model", parts=[Part.from_text(
                # f"""You are customer personal assistant who willing the support your customer.
                # You have to recommend or suggest the products that similar to the object in the query image based on product information and product image.
                # Only recommend or suggest the product in the product list.
                f"""Here is the product list in JSON format that we sell in our store. The list is consists of product details and product image, respectively.
                {json.dumps([
                    {
                        "product_id": 1,
                        "product_name": "Radiant Foundation",
                        "product_category": "Makeup",
                        "product_price": 1200,
                        "product_description": "A liquid foundation with a radiant finish.",
                        "product_color": "Beige",
                        "product_material": "Glass",
                        "product_image": "https://storage.googleapis.com/npkhack/radiant_foundation.png"
                    },
                    {
                        "product_id": 2,
                        "product_name": "Velvet Lipstick",
                        "product_category": "Makeup",
                        "product_price": 800,
                        "product_description": "Smooth and long-lasting velvet lipstick.",
                        "product_color": "Red",
                        "product_material": "Plastic",
                        "product_image": "https://storage.googleapis.com/npkhack/velvet_lipstick.png"
                    },
                    {
                        "product_id": 3,
                        "product_name": "Mineral Blush",
                        "product_category": "Makeup",
                        "product_price": 750,
                        "product_description": "Natural mineral blush for a healthy glow.",
                        "product_color": "Pink",
                        "product_material": "Plastic",
                        "product_image": "https://storage.googleapis.com/npkhack/mineral_blush.png"
                    },
                    {
                        "product_id": 4,
                        "product_name": "Perfect Eyeliner",
                        "product_category": "Makeup",
                        "product_price": 500,
                        "product_description": "Precise and smudge-proof eyeliner.",
                        "product_color": "Black",
                        "product_material": "Plastic",
                        "product_image": "https://storage.googleapis.com/npkhack/perfect_eyeliner.jpeg"
                    },
                    {
                        "product_id": 5,
                        "product_name": "Glow Skincare Set",
                        "product_category": "Skincare",
                        "product_price": 2200,
                        "product_description": "Complete skincare set for glowing skin.",
                        "product_color": "Multi-color",
                        "product_material": "Glass",
                        "product_image": "https://storage.googleapis.com/npkhack/glow_skincare_set.jpeg"
                    },
                    {
                        "product_id": 6,
                        "product_name": "Herbal Shampoo",
                        "product_category": "Haircare",
                        "product_price": 600,
                        "product_description": "Nourishing shampoo with herbal extracts.",
                        "product_color": "Green",
                        "product_material": "Plastic",
                        "product_image": None
                    },
                    {
                        "product_id": 7,
                        "product_name": "UV Defense Sunscreen",
                        "product_category": "Skincare",
                        "product_price": 1000,
                        "product_description": "Broad-spectrum sunscreen with UV defense.",
                        "product_color": "White",
                        "product_material": "Plastic",
                        "product_image": None
                    },
                    {
                        "product_id": 8,
                        "product_name": "Hydrating Face Mist",
                        "product_category": "Skincare",
                        "product_price": 650,
                        "product_description": "Refreshing and hydrating facial mist.",
                        "product_color": "Blue",
                        "product_material": "Glass",
                        "product_image": None
                    },
                    {
                        "product_id": 9,
                        "product_name": "All-in-One Concealer",
                        "product_category": "Makeup",
                        "product_price": 900,
                        "product_description": "Full-coverage concealer for all skin types.",
                        "product_color": "Beige",
                        "product_material": "Plastic",
                        "product_image": None
                    },
                    {
                        "product_id": 10,
                        "product_name": "Matte Eyeshadow Palette",
                        "product_category": "Makeup",
                        "product_price": 1100,
                        "product_description": "A palette with a variety of matte shades.",
                        "product_color": "Multi-color",
                        "product_material": "Plastic",
                        "product_image": None
                    },
                    {
                        "product_id": 11,
                        "product_name": "Elegant Sofa",
                        "product_category": "Living Room",
                        "product_price": 15000,
                        "product_description": "Comfortable and stylish sofa for living room.",
                        "product_color": "Gray",
                        "product_material": "Fabric",
                        "product_image": None
                    },
                    {
                        "product_id": 12,
                        "product_name": "Modern Coffee Table",
                        "product_category": "Living Room",
                        "product_price": 4500,
                        "product_description": "Sleek coffee table with a modern design.",
                        "product_color": "Black",
                        "product_material": "Glass",
                        "product_image": None
                    },
                    {
                        "product_id": 13,
                        "product_name": "Wooden Dining Table",
                        "product_category": "Dining Room",
                        "product_price": 12000,
                        "product_description": "Sturdy wooden dining table for family meals.",
                        "product_color": "Brown",
                        "product_material": "Wood",
                        "product_image": None
                    },
                    {
                        "product_id": 14,
                        "product_name": "Contemporary Chair",
                        "product_category": "Dining Room",
                        "product_price": 3500,
                        "product_description": "Comfortable and contemporary dining chair.",
                        "product_color": "White",
                        "product_material": "Plastic",
                        "product_image": None
                    },
                    {
                        "product_id": 15,
                        "product_name": "Spacious Bookshelf",
                        "product_category": "Home Office",
                        "product_price": 5500,
                        "product_description": "Large bookshelf for organizing books.",
                        "product_color": "Dark Brown",
                        "product_material": "Wood",
                        "product_image": None
                    },
                    {
                        "product_id": 16,
                        "product_name": "Cozy Bed",
                        "product_category": "Bedroom",
                        "product_price": 20000,
                        "product_description": "Cozy bed with a plush mattress.",
                        "product_color": "White",
                        "product_material": "Wood",
                        "product_image": "https://storage.googleapis.com/npkhack/cozy_bed.jpg"
                    },
                    {
                        "product_id": 17,
                        "product_name": "Minimalist Nightstand",
                        "product_category": "Bedroom",
                        "product_price": 2500,
                        "product_description": "Simple and functional nightstand.",
                        "product_color": "Light Brown",
                        "product_material": "Wood",
                        "product_image": "https://storage.googleapis.com/npkhack/minimalist_nightstand.jpg"
                    },
                    {
                        "product_id": 18,
                        "product_name": "Office Desk",
                        "product_category": "Home Office",
                        "product_price": 8000,
                        "product_description": "Ergonomic desk for home office use.",
                        "product_color": "Black",
                        "product_material": "Metal",
                        "product_image": "https://storage.googleapis.com/npkhack/office_desk.jpg"
                    },
                    {
                        "product_id": 19,
                        "product_name": "Stylish Lamp",
                        "product_category": "Living Room",
                        "product_price": 2000,
                        "product_description": "Stylish lamp for ambient lighting.",
                        "product_color": "Silver",
                        "product_material": "Metal",
                        "product_image": "https://storage.googleapis.com/npkhack/stylish_lamp.jpg"
                    },
                    {
                        "product_id": 20,
                        "product_name": "Rustic Wardrobe",
                        "product_category": "Bedroom",
                        "product_price": 12000,
                        "product_description": "Spacious wardrobe with a rustic finish.",
                        "product_color": "Brown",
                        "product_material": "Wood",
                        "product_image": "https://storage.googleapis.com/npkhack/rustic_wardrobe.jpg"
                    }
                ])}
                """)
                    , Part.from_uri("gs://npkhack/radiant_foundation.png", mime_type="image/png")
                    , Part.from_uri("gs://npkhack/velvet_lipstick.png", mime_type="image/png") 
                    , Part.from_uri("gs://npkhack/mineral_blush.png", mime_type="image/png")
                    , Part.from_uri("gs://npkhack/perfect_eyeliner.jpeg", mime_type="image/png")                 
                    , Part.from_uri("gs://npkhack/glow_skincare_set.jpeg", mime_type="image/png")
                    , Part.from_uri("gs://npkhack/cozy_bed.jpg", mime_type="image/png") 
                    , Part.from_uri("gs://npkhack/minimalist_nightstand.jpg", mime_type="image/png")
                    , Part.from_uri("gs://npkhack/office_desk.jpg", mime_type="image/png") 
                    , Part.from_uri("gs://npkhack/stylish_lamp.jpg", mime_type="image/png")
                    , Part.from_uri("gs://npkhack/rustic_wardrobe.jpg", mime_type="image/png")                                                                         
                    , Part.from_text("I must recommend or suggest the products that only in the product list.")])
        ]
    )


    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Hello Ton! How can I help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(key='client-advisor-agent'):
        # if not gemini_api_key:
        #     st.info("Please add your Gemini API key to continue.")
        #     st.stop()

        # client = OpenAI(api_key=gemini_api_key)

        st.session_state.messages.append({"role": "user", "content": prompt})

        st.chat_message("user").write(prompt)

        # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        
        response = chat.send_message(prompt)

        msg = response.text

        st.session_state.messages.append({"role": "assistant", "content": msg})

        st.chat_message("assistant").write(msg)
