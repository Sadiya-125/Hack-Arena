import streamlit as st
import pandas as pd
from utils.file_handler import FileHandler
from utils.cad_processor import CADProcessor
import asyncio

async def main():
    st.set_page_config(page_title="FlowGuard Application", layout="wide")

    file_handler = FileHandler()
    cad_processor = CADProcessor()
    
    st.title("Crowd Management System")
    st.sidebar.header("Data Source")
    st.sidebar.write("Upload your AutoCAD (.dwg) file for processing.")

    uploaded_file = st.sidebar.file_uploader("Upload AutoCAD file", type=['dwg'])
    if uploaded_file:
        st.sidebar.success("File uploaded successfully.")
    else:
        st.sidebar.warning("Please upload an AutoCAD (.dwg) file to proceed.")
    
    st.subheader("Processing Configuration")
    processing_option = st.radio(
        "Choose processing option:",
        ["Generate 3D Visualization", "Custom Analysis"],
        help="Select the type of processing to perform on the AutoCAD file."
    )

    custom_prompt = None
    if processing_option == "Custom Analysis":
        custom_prompt = st.text_area(
            "Enter your custom analysis prompt:",
            "Replace this text with the details of what analysis you need.",
            help="Provide specific details about the processing you'd like to perform."
        )
    
    if st.button("Start Processing"):
        if not uploaded_file:
            st.error("No file uploaded. Please upload an AutoCAD file to proceed.")
            return

        st.subheader("Processing Status")
        status_text = st.empty()
        processing_progress = st.progress(0)
        
        status_text.text("Reading AutoCAD file...")
        try:
            file_data = file_handler.read_autocad_file(uploaded_file)
            status_text.text("File read successfully.")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            return

        status_text.text(f"Performing {processing_option}...")
        try:
            if processing_option == "Custom Analysis" and custom_prompt:
                result = await cad_processor.custom_analysis(file_data, custom_prompt)
            else:
                result = await cad_processor.process_file(file_data, processing_option)
            
            status_text.text("Processing complete.")
            processing_progress.progress(100)
        except Exception as e:
            st.error(f"Error during processing: {e}")
            return
        
        st.subheader("Processing Results")
        if isinstance(result, pd.DataFrame):
            st.dataframe(result)
        else:
            st.text_area("Output", result, height=300)
        
        output, filename = file_handler.export_results(result)
        if output and filename:
            st.download_button(
                label="Download Processed Output",
                data=output,
                file_name=filename,
                mime="text/plain"
            )

if __name__ == "__main__":
    asyncio.run(main())
