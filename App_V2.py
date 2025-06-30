import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import tempfile

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

def save_itinerary_to_pdf(itinerary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in itinerary_text.split('\n'):
        pdf.multi_cell(0, 10, line)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

if "history" not in st.session_state:
    st.session_state.history = []

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
        st.session_state.history.append({
        "destination": destination,
        "days": days,
        "interests": interests,
        "budget": budget,
        "itinerary": itinerary
        })

        st.success("Here's your AI-planned itinerary:")
        st.markdown(itinerary)

        # Generate PDF and add download button
        pdf_file = save_itinerary_to_pdf(itinerary)
        with open(pdf_file, "rb") as f:
            st.download_button("📥 Download Itinerary as PDF", f, file_name="itinerary.pdf", mime="application/pdf")

        if st.session_state.history:
            st.subheader("🕓 My Trips")
            for i, entry in enumerate(reversed(st.session_state.history), 1):
                with st.expander(f"{i}. {entry['destination']} for {entry['days']} days (₹{entry['budget']})"):
                    st.markdown(entry["itinerary"])

