import streamlit as st
import os
import google.generativeai as genai
import dotenv
import io

dotenv.load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Set up the model
model = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Streamlit app
def main():
    st.title("📚Chat PDF🤖")

    # Upload PDF
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

    if uploaded_file is not None:
        # Define a directory to save the uploaded file (ensure this exists)
        save_directory = "C:/Users/Admin/Desktop/Akash/pdfChatApp/uploads/"

        # Ensure the directory exists
        os.makedirs(save_directory, exist_ok=True)

        # Get the file path to save the uploaded file
        tmp_filepath = os.path.join(save_directory, uploaded_file.name)

        try:
            # Save the uploaded file to the specified location
            with open(tmp_filepath, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Use the temporary file path for upload
            file_id = genai.upload_file(path=tmp_filepath)

            # Delete the temporary file after upload
            os.remove(tmp_filepath)

        except Exception as e:
            st.error(f"Error while saving or uploading the file: {e}")
            return

        # Text input for asking multiple questions
        user_input = st.text_input("Ask a question about the document:")

        if user_input:
            try:
                # Prompt the model with the file ID and the user's question
                response = model.generate_content([file_id, user_input])

                # Display the answer
                st.text_area("Response:", response.text, height=200)

                # **Download the response functionality**
                response_text = response.text  # The content to be downloaded
                if st.button("Download Response as .txt"):
                    try:
                        # Prepare the text for download
                        st.download_button(
                            label="Download Response",
                            data=response_text,
                            file_name="response.txt",
                            mime="text/plain",
                            use_container_width=True  # Optional, for better button layout
                        )
                    except Exception as e:
                        st.error(f"Error preparing response for download: {e}")

            except Exception as e:
                st.error(f"Error generating response: {e}")

if __name__ == "__main__":
    main()
