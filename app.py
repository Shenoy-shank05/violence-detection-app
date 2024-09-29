import streamlit as st
import base64  # Import the base64 module
from vipas import model
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException
from vipas.logger import LoggerClient

# Create a ModelClient Object
vps_model_client = model.ModelClient()
logger = LoggerClient(__name__)

def main():
    # Set up the Streamlit interface
    st.title('Real_Time_Threat_Detction')
    
    # Input for the image data
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    predict_button = st.button('Predict')

    if predict_button:
        if uploaded_file is not None:
            # Convert the uploaded file to base64 format
            image_data = uploaded_file.read()
            input_data = base64.b64encode(image_data).decode('utf-8')
            
            try:
                model_id = "mdl-egd1sfadhctl3"  # Replace with your model ID
                
                # Make a prediction
                api_response = vps_model_client.predict(
                    model_id=model_id,
                    input_data=input_data,
                    async_mode=True  # Default is async mode
                )
                
                # Display prediction result
                st.success(f'Prediction: {api_response}')
                logger.info(f"Predicted response: {api_response}")

            except UnauthorizedException as err:
                st.error(f"UnauthorizedException: {err}")
                logger.error(f"UnauthorizedException: {err}")
            except NotFoundException as err:
                st.error(f"NotFoundException: {err}")
                logger.error(f"NotFoundException: {err}")
            except ClientException as err:
                st.error(f"ClientException: {err}")
                logger.error(f"ClientException: {err}")
        else:
            st.warning("Please upload an image file.")

if __name__ == '__main__':
    main()
