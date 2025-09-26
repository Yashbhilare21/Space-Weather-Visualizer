## 📜 Progress Log

### Week 8, Day 1 – Capstone Development Part 1
- ✅ Project folder structure finalized:
  - `backend/` for Streamlit app
  - `data/` for cached API responses
  - `assets/` for images and icons
- ✅ Streamlit app skeleton created (`space_weather_app.py`)
- ✅ NASA DONKI API integration started:
  - Implemented API request with user-provided API key
  - Added sidebar for event type selection (FLR, CME, GST)
  - Start/end date input added
- ✅ First basic table display working with fetched data
- ⚡ Challenges:
  - Handled empty API responses
  - Added validation for invalid API key or incorrect dates

### Week 8, Day 2 – Capstone Development Part 2
- ✅ Data cleaning and preprocessing:
  - Handled datetime conversion
  - Removed timezone issues for Excel export
- ✅ Interactive visualizations added using Plotly:
  - Line charts showing event frequency over time
  - Pie charts for event type distribution (optional)
- ✅ Sidebar filters fully functional
- ✅ Added caching for API calls to reduce repeated requests
- ⚡ Challenges:
  - Handling inconsistent datetime formats from NASA API
  - Ensuring charts work with empty datasets

### Week 8, Day 3 – Capstone Development Part 3
- ✅ Export functionality implemented:
  - CSV and Excel download buttons
  - Timezone-unaware datetime ensured for Excel export
- ✅ Raw JSON viewer added under an expander
- ✅ Additional UI polish:
  - Wide page layout (`layout="wide"`)
  - Streamlined sidebar sections
- ✅ Event frequency chart finalized
- ⚡ Challenges:
  - Debugged Excel export errors due to timezone-aware datetimes
  - Optimized caching and API error handling

### Week 8, Day 4 – Final Testing & Deployment
- ✅ Comprehensive manual testing:
  - Buttons, inputs, charts, downloads, and JSON viewer
  - Cross-browser testing (Chrome, Firefox, Edge, Safari)
  - Mobile responsiveness verified
- ✅ Deployed app on Streamlit Cloud
  - Custom app URL: [https://space-weather-visualizer-agnirva.streamlit.app/]
- ✅ README.md updated with screenshots, instructions, and progress log
- ⚡ Challenges:
  - Adjusted layout and column widths for better readability
  - Verified Excel/CSV downloads on deployed app

### Week 8, Day 5 – Capstone Project Demo Day
- ✅ Recorded 5-minute demo walkthrough
- ✅ Explained problem, solution, and features implemented
- ✅ Collected feedback from peers and mentors
- ✅ Final adjustments based on feedback
- ✅ Project finalized for submission
