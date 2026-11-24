
import streamlit as st
import hashlib
from PIL import Image

from detector import detect_potholes
from map import create_map


# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="AI Pothole Detection",
    page_icon="🚧",
    layout="wide"
)

st.title("🚧 AI-Based Pothole Detection System")

st.markdown("""
Detect potholes using our custom-trained YOLOv8 model
and visualize their reported locations on an English-labelled map.
""")

st.divider()


# --------------------------------
# SESSION STATE
# --------------------------------

if "detected_image" not in st.session_state:
    st.session_state.detected_image = None

if "detections" not in st.session_state:
    st.session_state.detections = None

if "image_hash" not in st.session_state:
    st.session_state.image_hash = None


# --------------------------------
# SIDEBAR SETTINGS
# --------------------------------

st.sidebar.header("⚙️ Detection Settings")

confidence = st.sidebar.slider(
    "Confidence Threshold",
    min_value=0.10,
    max_value=0.90,
    value=0.25,
    step=0.05
)

st.sidebar.info("""
**Model:** Custom YOLOv8 Nano

**Detection Class:** Potholes

**Device:** CPU
""")


# --------------------------------
# IMAGE UPLOAD
# --------------------------------

st.subheader("📸 Upload Road Image")

uploaded_file = st.file_uploader(
    "Choose a road image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image_bytes = uploaded_file.getvalue()

    current_hash = hashlib.sha256(
        image_bytes
    ).hexdigest()

    # Reset previous results when a new image is uploaded
    if current_hash != st.session_state.image_hash:

        st.session_state.detected_image = None
        st.session_state.detections = None
        st.session_state.image_hash = current_hash

    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Road Image")

    st.image(
        image,
        width="stretch"
    )


    # --------------------------------
    # DETECTION
    # --------------------------------

    if st.button(
        "🔍 Analyze Image",
        type="primary"
    ):

        try:

            with st.spinner("Analyzing road image using YOLOv8..."):

                result_image, result_detections = detect_potholes(
                    image,
                    confidence
                )

            st.session_state.detected_image = result_image
            st.session_state.detections = result_detections

            st.success("Image analysis completed!")

        except Exception as error:

            st.error(f"Detection failed: {error}")


    # --------------------------------
    # DISPLAY RESULTS
    # --------------------------------

    if st.session_state.detected_image is not None:

        st.divider()

        st.subheader("📊 Pothole Detection Results")

        detections = st.session_state.detections

        col1, col2 = st.columns(2)

        with col1:

            st.image(
                st.session_state.detected_image,
                caption="YOLOv8 Analyzed Image",
                width="stretch"
            )

        with col2:

            st.metric(
                "Total Potholes Detected",
                len(detections)
            )

            if detections:

                st.write("### Detection Details")

                for index, item in enumerate(detections, start=1):

                    st.write(
                        f"**Pothole {index}**"
                    )

                    st.write(
                        f"Confidence: {item['confidence']}%"
                    )

            else:

                st.info("No potholes detected in this image.")


        # --------------------------------
        # LOCATION REPORTING
        # --------------------------------

        st.divider()

        st.subheader("📍 Pothole Location Reporting")

        st.warning(
            "Enter the actual GPS coordinates where the road image "
            "was captured. These coordinates are not automatically "
            "identified by the YOLO model."
        )

        col1, col2 = st.columns(2)

        with col1:

            latitude = st.number_input(
                "Latitude",
                min_value=-90.0,
                max_value=90.0,
                value=None,
                placeholder="Enter latitude",
                format="%.6f"
            )

        with col2:

            longitude = st.number_input(
                "Longitude",
                min_value=-180.0,
                max_value=180.0,
                value=None,
                placeholder="Enter longitude",
                format="%.6f"
            )


        # --------------------------------
        # MAP DISPLAY
        # --------------------------------

        if latitude is not None and longitude is not None:

            st.subheader("🗺️ English-Language Location Map")

            try:

                create_map(
                    latitude,
                    longitude,
                    len(detections)
                )

            except Exception as error:

                st.error(
                    f"Map could not be loaded: {error}"
                )

        else:

            st.info(
                "Enter both latitude and longitude to display "
                "the reporting location."
            )


else:

    st.info(
        "Upload a road image to begin pothole detection."
    )

    st.markdown("""
    ### How the system works

    1. Upload a road image.
    2. YOLOv8 detects potholes.
    3. Bounding boxes highlight detected potholes.
    4. Confidence scores are displayed.
    5. Enter the actual GPS coordinates.
    6. View the reported location on an English-labelled map.
    """)
