import streamlit as st
import duckdb
import pandas as pd
import altair as alt

# page setup
st.set_page_config(page_title="# 🚲 NYC Citi Bike vs. Weather", layout="wide")
st.title("🚲 NYC Citi Bike vs. Weather")
st.markdown("Daily temperature and rainfall impact on NYC ridership.")

@st.cache_data
def load_daily_data():
    con = duckdb.connect("bike_project/bike.duckdb", read_only=True)
    df = con.execute("""
        SELECT 
            weather_date,
            AVG(temp_f) AS avg_temp,
            SUM(precipitation) AS total_precip,
            SUM(total_rides) AS daily_rides
        FROM main.fct_citibike_weather_impact
        GROUP BY weather_date
    """).df()
    con.close()
    
    df['temp_bucket'] = pd.cut(df['avg_temp'], bins=[0, 40, 60, 80, 100], labels=['<40°F', '40-60°F', '60-80°F', '80°F+'])
    df['weather_type'] = df['total_precip'].apply(lambda x: 'Rainy' if x > 0.1 else 'Dry')
    return df

df = load_daily_data()

color_scale = alt.Scale(domain=['Dry', 'Rainy'], range=['#FF4B4B', '#00D4FF'])

# 1.
st.subheader("Daily Rides vs. Temperature")

scatter = alt.Chart(df).mark_circle(opacity=0.8, stroke='#888888', strokeWidth=1).encode(
    x=alt.X('avg_temp:Q', title='Daily Average Temp (°F)'),
    y=alt.Y('daily_rides:Q', title='Total Daily Rides'),
    size=alt.Size('total_precip:Q', scale=alt.Scale(range=[80, 1000]), title='Rain Volume (Inches)'),
    color=alt.Color('weather_type:N', scale=color_scale, title='Weather Condition'),
    tooltip=['weather_date', 'avg_temp', 'total_precip', 'daily_rides']
).interactive()

st.altair_chart(scatter, use_container_width=True)

st.divider()

# 2.
st.subheader("Average Rides: Dry vs. Rainy Days")

bar = alt.Chart(df).mark_bar().encode(
    x=alt.X('temp_bucket:O', title='Temperature Range', axis=alt.Axis(labelAngle=0)),
    xOffset=alt.XOffset('weather_type:N'),
    y=alt.Y('mean(daily_rides):Q', title='Average Daily Rides'),
    color=alt.Color('weather_type:N', scale=color_scale, title='Weather Condition'),
    tooltip=['temp_bucket', 'weather_type', 'mean(daily_rides)']
).properties(
    height=400 
)

st.altair_chart(bar, use_container_width=True)