import streamlit as st
import google.generativeai as genai

# Configure Gemini API Key
genai.configure(api_key="Your API Key")

# Function to generate itinerary
def generate_itinerary(destination, days, interests, budget):
    prompt = f"""
    Plan a travel itinerary for a person visiting {destination} for {days} days.
    Interests include: {interests}.
    The budget is {budget} INR.
    Suggest activities, places to visit, meals, and travel tips day-wise.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.title("🧳 AI Travel Itinerary Planner")
st.write("Plan your dream trip with AI ✨")

destination = st.text_input("Enter Destination")
days = st.number_input("Number of Days", min_value=1, max_value=30, step=1)
interests = st.text_area("What are your Interests? (e.g. nature, history, food, adventure)")
budget = st.number_input("Budget (INR)", min_value=1000, max_value=1000000, step=1000)
#The step=1000 means:
# The number will increase or decrease in steps of 1000 when the user uses the up/down arrow buttons.

if st.button("Generate My Travel Plan"):
    with st.spinner("Planning your trip..."):
        itinerary = generate_itinerary(destination, days, interests, budget)
        st.success("Here's your AI-planned itinerary:")
        st.markdown(itinerary)


