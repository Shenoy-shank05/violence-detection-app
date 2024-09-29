import streamlit as st
import base64  # Import the base64 module
from vipas import model
from vipas.exceptions import UnauthorizedException, NotFoundException, ClientException
from vipas.logger import LoggerClient
from processor import pre_process, post_process  # Import the processor functions

# Create a ModelClient Object
vps_model_client = model.ModelClient()
logger = LoggerClient(__name__)

def main():
    # Set up the Streamlit interface
    st.title('Real-Time Threat Detection')
    
    # Input for the video data
    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
    
    predict_button = st.button('Predict')

    if predict_button:
        if uploaded_file is not None:
            # Convert the uploaded file to base64 format
            video_data = uploaded_file.read()
            input_data = base64.b64encode(video_data).decode('utf-8')
            
            try:
                model_id = "mdl-egd1sfadhctl3"  # Replace with your model ID
                
                # Preprocess the video
                processed_frames, original_video_base64 = pre_process(input_data)

                # Make a prediction
                api_response = vps_model_client.predict(
                    model_id=model_id,
                    input_data=processed_frames,
                    async_mode=True  # Default is async mode
                )
                
                # Postprocess the prediction result
                predictions = post_process(api_response)

                # Display prediction result
                st.success(f'Predictions: {predictions}')
                logger.info(f"Predicted response: {predictions}")

                # Optionally display the original video
                st.video(original_video_base64)

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
            st.warning("Please upload a video file.")

if __name__ == '__main__':
    main()
