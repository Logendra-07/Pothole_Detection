
import streamlit as st
import streamlit.components.v1 as components
import json


def create_map(latitude, longitude, pothole_count):

    api_key = st.secrets["MAPTILER_API_KEY"]

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">

        <script src="https://cdn.maptiler.com/maptiler-sdk-js/v4.2.1/maptiler-sdk.umd.min.js"></script>

        <link href="https://cdn.maptiler.com/maptiler-sdk-js/v4.2.1/maptiler-sdk.css"
              rel="stylesheet" />

        <style>
            body {{
                margin: 0;
                padding: 0;
            }}

            #map {{
                width: 100%;
                height: 460px;
            }}
        </style>
    </head>

    <body>

        <div id="map"></div>

        <script>

            maptilersdk.config.apiKey = {json.dumps(api_key)};

            const map = new maptilersdk.Map({{
                container: "map",
                style: maptilersdk.MapStyle.STREETS,

                center: [
                    {longitude},
                    {latitude}
                ],

                zoom: 15,

                language: "en"
            }});

            map.on("load", function() {{

                new maptilersdk.Marker({{
                    color: "#e63946"
                }})
                .setLngLat([
                    {longitude},
                    {latitude}
                ])
                .setPopup(
                    new maptilersdk.Popup().setHTML(
                        "<b>Pothole Report</b><br>" +
                        "Detected potholes: {pothole_count}"
                    )
                )
                .addTo(map);

            }});

        </script>

    </body>
    </html>
    """

    components.html(
        html,
        height=480,
        scrolling=False
    )
