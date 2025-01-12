import streamlit as st

from app.pipeline import qa_pipeline

def main():
    st.title("Chatbot on Ardshinbank website")

    question = st.text_input("Enter your question:")

    if st.button("Get Answer"):
        if question.strip() == "":
            st.error("Please provide a question.")
        else:
            with st.spinner("Generating answer..."):
                try:
                    result = qa_pipeline.answer_question(question)
                    st.success("Answer Generated!")
                    st.write(f"**Answer:** {result['answer']}")
                    sources = result.get('sources', [])
                    if sources:
                        st.write("**References:**")
                        for source in sources:
                            st.write(f"- [{source['title']}]({source['url']})")
                    else:
                        st.write("**References:** N/A")
                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
