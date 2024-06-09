import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def analyze_literary_work(text):
   
    max_tokens = 4096
    sentences = text.split(".")
    current_tokens = 0
    truncated_text = ""
    for sentence in sentences:
        if current_tokens + len(sentence.split()) <= max_tokens:
            truncated_text += sentence + "."
            current_tokens += len(sentence.split())
        else:
            break

    prompt = f"""
    You are an analyst of literary works. I want you to analyze this work:

    {truncated_text}

    and I want to focus on these aspects:
    1. Character analysis:
       - Understand the motivations of the main and secondary characters and how they influence the events and conflicts in the story.
    2. Evaluate the author's portrayal and presentation of the characters.
    3. Analysis of symbols and major themes:
       - Understand the main themes explored by the author (such as love, death, identity, politics, etc.).
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a literary analysis assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        analysis = {
            "character_analysis": response.choices[0].message.content,
            "plot_and_narrative_analysis": response.choices[0].message.content,
            "themes_analysis": response.choices[0].message.content
        }
        return analysis
    except Exception as e:
        st.error(f"Error: {e}")
        return {}

st.set_page_config(page_title="Literary Work Analysis")
st.title("Literary Work Analysis")

literary_work = st.text_area("Hi, I am a literary analyst, available to help you with your literary works. Enter your literary work:", height=300)

if st.button("Analyze"):
    analysis = analyze_literary_work(literary_work)
    if analysis:
        st.subheader("Character Analysis")
        st.write(analysis["character_analysis"])
        st.subheader("Plot and Narrative Structure Analysis")
        st.write(analysis["plot_and_narrative_analysis"])
        st.subheader("Themes Analysis")
        st.write(analysis["themes_analysis"])