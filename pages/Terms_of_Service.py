import streamlit as st

st.set_page_config(page_title="Terms of Service", page_icon="📜")

st.title("📜 Terms of Service for Smart Scheduler AI")
st.caption("Last Updated: January 6, 2026")

st.markdown("---")

st.header("Acceptance of Terms")
st.write("By accessing and using Smart Scheduler AI, you accept and agree to be bound by these Terms of Service.")

st.header("Description of Service")
st.write("Smart Scheduler AI is a free web application that helps users schedule calendar events using natural language conversation and AI assistance.")

st.header("User Responsibilities")

st.subheader("API Keys")
st.write("""
- You must provide your own Google Gemini API key
- You are responsible for any charges incurred from your Gemini API usage
- Keep your API key secure and do not share it
""")

st.subheader("Google Calendar Access")
st.write("""
- You grant the app permission to access your Google Calendar
- You can revoke this permission at any time
- You are responsible for the accuracy of event information you provide
""")

st.subheader("Acceptable Use")
st.write("""
You agree to:
- Use the service only for lawful purposes
- Not attempt to gain unauthorized access to the service
- Not use the service in any way that could damage or impair it
""")

st.header("Limitations")

st.subheader("No Warranty")
st.write("""
- The service is provided "as is" without warranties of any kind
- We do not guarantee uninterrupted or error-free service
- We are not responsible for any errors in scheduled events
""")

st.subheader("Limitation of Liability")
st.write("""
- We are not liable for any damages arising from your use of the service
- You use the service at your own risk
- We are not responsible for any data loss or calendar errors
""")

st.header("Third-Party Services")
st.write("""
This service relies on:
- Google Calendar API (subject to Google's Terms of Service)
- Google Gemini AI (subject to Google's Terms of Service)

You must comply with the terms of service of these third-party providers.
""")

st.header("Data and Privacy")
st.write("Your use of Smart Scheduler AI is also governed by our Privacy Policy. Please review it to understand our data practices.")

st.header("Termination")
st.write("We reserve the right to terminate or suspend access to the service at any time without notice.")

st.header("Changes to Terms")
st.write("We may modify these terms at any time. Continued use of the service constitutes acceptance of modified terms.")

st.header("Contact")
st.write("For questions about these Terms of Service, contact: prasanjeetkr313@gmail.com")

st.header("Governing Law")
st.write("These terms are governed by applicable laws without regard to conflict of law provisions.")

st.markdown("---")
if st.button("← Back to App"):
    st.switch_page("app.py")
