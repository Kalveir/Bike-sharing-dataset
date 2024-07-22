import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load datasets
df_day = pd.read_csv('https://raw.githubusercontent.com/Kalveir/Bike-sharing-dataset/main/day.csv')

# Mapping categorical values
df_day['mnth'] = df_day['mnth'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})

df_day['season'] = df_day['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})

df_day['weekday'] = df_day['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})

df_day['weathersit'] = df_day['weathersit'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Rain',
    4: 'Severe Weather'
})

df_day['yr'] = df_day['yr'].map({
    0: '2011', 1: '2012'
})

df_day['workingday'] = df_day['workingday'].map({
    0: 'Holiday', 1: 'Workingday'
})

# Changing data types to categorical
df_day['season'] = df_day['season'].astype('category')
df_day['yr'] = df_day['yr'].astype('category')
df_day['mnth'] = df_day['mnth'].astype('category')
df_day['holiday'] = df_day['holiday'].astype('category')
df_day['weekday'] = df_day['weekday'].astype('category')
df_day['workingday'] = df_day['workingday'].astype('category')
df_day['weathersit'] = df_day['weathersit'].astype('category')

# Set up Streamlit app
st.title("Bike Sharing Dashboard")

# Sidebar for filters
st.sidebar.title("Filters")
season_filter = st.sidebar.multiselect("Select Season", df_day['season'].unique())
month_filter = st.sidebar.multiselect("Select Month", df_day['mnth'].unique())
year_filter = st.sidebar.multiselect("Select Year", df_day['yr'].unique())
weather_filter = st.sidebar.multiselect("Select Weather", df_day['weathersit'].unique())
workingday_filter = st.sidebar.multiselect("Select Working Day", df_day['workingday'].unique())

# Filter data based on sidebar selections
filtered_data = df_day[
    (df_day['season'].isin(season_filter)) &
    (df_day['mnth'].isin(month_filter)) &
    (df_day['yr'].isin(year_filter)) &
    (df_day['weathersit'].isin(weather_filter)) &
    (df_day['workingday'].isin(workingday_filter))
]

# Show summary statistics
st.write("### Summary Statistics")
st.write(filtered_data.describe())

# Line chart for trend in bike rentals by month and year
st.subheader("Trend Sewa Sepeda per Bulan dan Tahun")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=filtered_data.groupby(by=["mnth","yr"]).agg({"cnt": "sum"}).reset_index(),
    x="mnth",
    y="cnt",
    hue="yr",
    palette="rocket",
    marker="o",
    ax=ax
)
ax.set_title("Trend Sewa Sepeda")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Penyewaan")
ax.legend(title="Tahun", loc="upper right")
st.pyplot(fig)

# Bar chart for bike rentals based on weather condition
st.subheader("Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca")
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='weathersit',
    y='cnt',
    data=filtered_data,
    ax=ax2
)
ax2.set_title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
ax2.set_xlabel('Kondisi Cuaca')
ax2.set_ylabel('Jumlah Pengguna Sepeda')
st.pyplot(fig2)

# Bar chart for bike rentals by season
st.subheader("Jumlah penyewa sepeda berdasarkan musim")
season_pattern = filtered_data.groupby('season')[['registered', 'casual']].sum().reset_index()
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.bar(
    season_pattern['season'],
    season_pattern['registered'],
    label='Registered',
    color='tab:red'
)
ax3.bar(
    season_pattern['season'],
    season_pattern['casual'],
    label='Casual',
    color='tab:green'
)
ax3.set_title('Jumlah penyewa sepeda berdasarkan musim')
ax3.set_xlabel('Musim')
ax3.set_ylabel('Jumlah Penyewa')
ax3.legend()
st.pyplot(fig3)

# Bar chart for bike rentals on working days vs holidays
st.subheader("Perbandingan Penyewa Sepeda pada Hari Kerja dan Libur")
fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(
    x='workingday',
    y='cnt',
    data=filtered_data,
    ax=ax4
)
ax4.set_title('Perbandingan Penyewa Sepeda Workingday dan Holiday')
ax4.set_xlabel(None)
ax4.set_ylabel('Jumlah Pengguna Sepeda')
st.pyplot(fig4)
