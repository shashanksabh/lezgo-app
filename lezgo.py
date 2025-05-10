#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 18:48:44 2024

@author: shashanksabhlok
"""

import streamlit as st
from langchain import PromptTemplate
from langchain_openai import OpenAI
from langchain.chat_models import ChatOpenAI
import json
# Initialize the OpenAI model
openai = OpenAI(
    model_name="gpt-3.5-turbo-instruct",
    openai_api_key="####"  # Be careful with your API key, don't expose it in your code.
)

template = """
Develop a travel itinerary for the city specified  that follows the
format below and customize it based on preferences of each traveler listed below for the specified city, and for the specified number of days:
    
Day 1: Historical and Cultural Exploration
Morning: Visit the Duomo di Milano. Start your Milan adventure with this iconic gothic cathedral. Take your time to explore the interior and if possible, climb up to the rooftop for a stunning view of the city.
Lunch: Dine at Galleria Vittorio Emanuele II. Located just beside the Duomo, this historic gallery is not only a shopping center but also home to some classic Milanese restaurants. Enjoy a leisurely lunch at one of the cafes or restaurants.
Afternoon: Explore the Sforza Castle. After lunch, walk to the Sforza Castle to discover Milan's history and view various art collections, including works by Michelangelo and Leonardo da Vinci.
Evening: Enjoy an opera at La Scala. End your day with a performance at one of the most famous opera houses in the world. Make sure to book tickets in advance.

Day 2: Art and Nature
Morning: Visit the Pinacoteca di Brera. Start your day with a visit to one of Milan's premier art galleries, home to a vast collection of Italian Renaissance art.
Lunch: Eat in the Brera district. After your museum visit, explore the charming streets of Brera and choose one of the district's cozy cafes for lunch.
Afternoon: Relax in the Sempione Park. Spend your afternoon strolling or resting in this large city park located behind the Sforza Castle, a perfect spot to unwind and people-watch.
Evening: Dinner and walk along Navigli. Finish your day with dinner at one of the many restaurants along the Navigli canals, followed by a pleasant walk along the waterways.

Day 3: Modern Milan and Shopping
Morning: Explore CityLife Shopping District. Start your day in this modern shopping and business district, which also offers some interesting architectural sights, including the futuristic skyscrapers designed by famous architects.
Lunch: Have lunch at Eataly. Located near the Porta Garibaldi railway station, Eataly offers a variety of restaurants and food shops where you can enjoy high-quality Italian food.
Afternoon: Visit the Fondazione Prada. Spend your afternoon at this contemporary art museum located in a former gin distillery, showcasing a variety of art from the 20th and 21st centuries.
Evening: Aperitivo and Farewell. For your last evening, participate in the Milanese tradition of aperitivo. Head to the trendy Isola district, find a cozy bar, and enjoy some drinks and snacks as you reflect on your Milanese adventure.

City: {city}

Days: {days}

Preferences: {prefs}

Itinerary:
"""

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["city", "days", "prefs"],  # We'll combine preferences into one variable
    template=template
)

# Streamlit UI setup
st.set_page_config(page_title='📍 Lezgo')
st.title('📍 Lezgo - Travel Itinerary Generator')
city = st.text_input('City', 'Enter the city')
days = st.text_input ('Number of days', 'Enter the number of travel days')
number_of_travelers = st.number_input('Number of travelers', min_value=1, max_value=10, value=2, step=1)

# Dynamic creation of preference input fields based on the number of travelers
preferences = []  # To hold the preferences of each traveler
for i in range(number_of_travelers):
    pref = st.text_input(f'Traveler {i + 1} preferences', f'Enter preferences for traveler {i + 1}')
    preferences.append(pref)

# Combine all preferences into a single string, each preference separated by "; "
prefs_combined = "; ".join(preferences)

# When the 'Generate Itinerary' button is clicked



if st.button('Generate Itinerary'):
    # Format the prompt
    formatted_prompt = prompt_template.format(
        city=city, days = days, prefs=prefs_combined
    )

    # Make the call to the OpenAI API
    try:
        generated_text = openai(formatted_prompt)  # Assuming this directly returns the text
        st.subheader('Generated Itinerary')
        st.write(generated_text)
    except Exception as e:
        # Log unexpected errors
        st.error(f"An error occurred: {e}")
        st.stop()
        
