import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import pandas as pd
import tempfile

# Configure Gemini API Key
genai.configure(api_key="Your API Key")

# Function to generate itinerary
def generate_itinerary(destination, days, interests, budget, theme):
    # prompt = f"""
    # Plan a travel itinerary for a person visiting {destination} for {days} days.
    # Interests include: {interests}.
    # The budget is {budget} INR.
    # Suggest activities, places to visit, meals, and travel tips day-wise.
    # """

    final_prompt = f"""
Act as an expert travel planner. Create a detailed {theme.lower()} itinerary for a trip to {destination} for {days} days.
{theme_instruction}
Give a day-wise breakdown. Be creative and engaging.
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(final_prompt)
    return response.text

def clean_text(text):
    return text.replace("–", "-").replace("“", '"').replace("”", '"')

def save_itinerary_to_pdf(itinerary_text):
    itinerary_text = clean_text(itinerary_text)  # Clean unsupported characters
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # for line in itinerary_text.split('\n'):
    #     pdf.multi_cell(0, 10, line)

    # tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    # pdf.output(tmp_file.name)
    # return tmp_file.name
    for line in itinerary_text.split("\n"):
        pdf.cell(200, 10, txt=clean_text(line), ln=True)

    filename = "itinerary.pdf"
    pdf.output(filename)
    return filename

if "history" not in st.session_state:
    st.session_state.history = []

# Streamlit UI
st.title("🧳 AI Travel Itinerary Planner")
st.write("Plan your dream trip with AI ✨")
theme = st.selectbox("Select your trip theme", ["Relaxing", "Adventure", "Romantic", "Spiritual"])

# Adjust the prompt accordingly
theme_instruction = {
    "Relaxing": "Focus on slow-paced, rejuvenating experiences like beaches, nature, spas, etc.",
    "Adventure": "Focus on hiking, camping, thrilling sports, and bold explorations.",
    "Romantic": "Include cozy cafes, candlelight dinners, sunset spots, and beautiful scenery.",
    "Spiritual": "Include visits to temples, spiritual retreats, historical sites, and peaceful nature."
}[theme]
destination = st.text_input("Enter Destination")
days = st.number_input("Number of Days", min_value=1, max_value=30, step=1)
interests = st.text_area("What are your Interests? (e.g. nature, history, food, adventure)")
budget = st.number_input("Budget (INR)", min_value=1000, max_value=1000000, step=1000)
#The step=1000 means:
# The number will increase or decrease in steps of 1000 when the user uses the up/down arrow buttons.

destination_query = destination.replace(" ", "+")
maps_url = f"https://www.google.com/maps/search/?api=1&query={destination_query}"
st.markdown(f"[📍 View {destination} on Google Maps]({maps_url})", unsafe_allow_html=True)


if st.button("Generate My Travel Plan"):
    with st.spinner("Planning your trip..."):
        itinerary = generate_itinerary(destination, days, interests, budget, theme_instruction)
        st.session_state.history.append({
        "theme": theme_instruction,
        "destination": destination,
        "days": days,
        "interests": interests,
        "budget": budget,
        "itinerary": itinerary
        })
      
        st.success("Here's your AI-planned itinerary:")
        st.markdown(itinerary)
        # st.text(st.session_state.history[-1]["itinerary"])
        
        # Generate PDF and add download button
        pdf_file = save_itinerary_to_pdf(itinerary)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Itinerary as PDF", f, file_name="itinerary.pdf", mime="application/pdf")

        if st.session_state.history:
            st.subheader("🕓 My Trips")
            for i, entry in enumerate(reversed(st.session_state.history), 1):
                with st.expander(f"{i}. {entry['destination']} for {entry['days']} days (₹{entry['budget']})"):
                    st.markdown(entry["itinerary"])

