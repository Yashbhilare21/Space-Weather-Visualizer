import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px
from io import BytesIO

# -------------------------------
# Caching to reduce repeated API calls
# -------------------------------
@st.cache_data(ttl=3600)
def fetch_data(event_type, start_date, end_date, api_key):
    url = f"https://api.nasa.gov/DONKI/{event_type}?startDate={start_date}&endDate={end_date}&api_key={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# -------------------------------
# App Title
# -------------------------------
st.set_page_config(page_title="Agnirva Space Weather Visualizer", page_icon="🚀", layout="wide")
st.title("Agnirva Space Weather Visualizer 🚀")

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("⚙️ Configure Space Weather Data")
api_key = st.sidebar.text_input("Enter your NASA API Key", "")

# Multi-event selection
event_types = st.sidebar.multiselect("Select Event Types", ["FLR", "CME", "GST"], default=["FLR"])
start_date = st.sidebar.date_input("Start Date", datetime.today() - timedelta(days=30))
end_date = st.sidebar.date_input("End Date", datetime.today())

# Optional filters
st.sidebar.subheader("🔍 Event Filters")
cme_speed = st.sidebar.slider("CME Speed (km/s)", 0, 3000, (0, 3000))
gst_kp = st.sidebar.slider("GST Kp Index", 0, 9, (0, 9))

# -------------------------------
# Fetch Data
# -------------------------------
if st.sidebar.button("Fetch Data"):
    if start_date > end_date:
        st.error("❌ Start Date cannot be later than End Date")
    elif api_key.strip() == "":
        st.error("❌ Please enter a valid NASA API Key")
    elif not event_types:
        st.error("❌ Please select at least one event type")
    else:
        all_dfs = []
        try:
            for event_type in event_types:
                data = fetch_data(event_type, start_date, end_date, api_key)
                if data:
                    df = pd.DataFrame(data)
                    df["event_type"] = event_type  # Add column to keep track of type

                    # Convert datetime columns and remove timezone info
                    for col in df.columns:
                        if df[col].dtype == "object" and df[col].str.contains("T").any():
                            try:
                                df[col] = pd.to_datetime(df[col], errors="ignore", utc=True).dt.tz_localize(None)
                            except Exception:
                                pass

                    # Apply filters
                    if event_type == "CME" and "speed" in df.columns:
                        df = df[(df["speed"] >= cme_speed[0]) & (df["speed"] <= cme_speed[1])]
                    if event_type == "GST" and "kp_index" in df.columns:
                        df["kp_index"] = pd.to_numeric(df["kp_index"], errors="coerce")
                        df = df[(df["kp_index"] >= gst_kp[0]) & (df["kp_index"] <= gst_kp[1])]

                    all_dfs.append(df)

            if all_dfs:
                final_df = pd.concat(all_dfs, ignore_index=True)
                st.subheader("📋 Combined Event Table")
                st.dataframe(final_df)

                # -------------------------------
                # Event Frequency Over Time
                # -------------------------------
                if "beginTime" in final_df.columns or "startTime" in final_df.columns:
                    final_df['event_date'] = pd.to_datetime(final_df.get('beginTime', final_df.get('startTime')), utc=True).dt.tz_localize(None)
                    freq_df = final_df.groupby([final_df['event_date'].dt.date, 'event_type']).size().reset_index(name='Event Count')
                    st.subheader("📊 Event Frequency Over Time")
                    fig = px.line(freq_df, x='event_date', y='Event Count', color='event_type',
                                  markers=True, title="Event Frequency Over Time")
                    st.plotly_chart(fig, use_container_width=True)

                # -------------------------------
                # Event Type Distribution
                # -------------------------------
                type_counts = final_df['event_type'].value_counts().reset_index()
                type_counts.columns = ['Event Type', 'Count']
                st.subheader("📈 Event Type Distribution")
                fig_type = px.pie(type_counts, names='Event Type', values='Count', hole=0.4)
                st.plotly_chart(fig_type, use_container_width=True)

                # -------------------------------
                # Export Options
                # -------------------------------
                st.subheader("⬇️ Export Data")
                for col in final_df.select_dtypes(include=["datetimetz"]).columns:
                    final_df[col] = final_df[col].dt.tz_localize(None)

                csv = final_df.to_csv(index=False).encode("utf-8")
                excel_buffer = BytesIO()
                with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
                    final_df.to_excel(writer, index=False, sheet_name="Events")

                col1, col2 = st.columns(2)
                col1.download_button("⬇️ Download CSV", csv, "events.csv", "text/csv")
                col2.download_button("⬇️ Download Excel", excel_buffer.getvalue(), "events.xlsx")

                # -------------------------------
                # Raw JSON viewer
                # -------------------------------
                with st.expander("🛠 Show Raw JSON Data"):
                    st.json(final_df.to_dict(orient="records"))

            else:
                st.warning("⚠️ No events found after applying filters.")

        except Exception as e:
            st.error(f"❌ Error fetching data: {e}")
