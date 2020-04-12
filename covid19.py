import pandas as pd
import plotly.express as px
import plotly.io as pio

norm = 100000  # Normalizes cases and deaths every norm inhabitants

# Labels
columns_names = [
        "Date",
        "Day",
        "Month",
        "Year",
        "New Cases",
        "New Deaths",
        "Country",
        "ID",
        "Country Code",
        "Population"]

# Countries
countries = [
        "Argentina",
        "Bolivia",
        "Brazil",
        "Chile",
        "China",
        "Colombia",
        "Ecuador",
        "Italy",
        "Peru",
        "Spain",
        "Uruguay",
        "USA",
        "Venezuela"]

# Load data
cov_data_raw = pd.read_csv(
        "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv",
        parse_dates=['Date'], dayfirst=True, names=columns_names, header=0)

# Fix USA name
cov_data_raw.loc[cov_data_raw["ID"] == "US", "Country"] = "USA"

# Select countries
cov_data = cov_data_raw.loc[cov_data_raw["Country"].isin(countries)]

# Sort using ascending dates
cov_data = cov_data.sort_values("Date", ascending=True)

# Add cummulative columns
cov_data["Cases"] = cov_data["New Cases"].groupby(cov_data["Country"]).transform("cumsum")
cov_data["Deaths"] = cov_data["New Deaths"].groupby(cov_data["Country"]).transform("cumsum")

# Remove leading zeros
cov_data = cov_data.loc[cov_data["Cases"] != 0]

# Normalized every norm inhabitants
cov_data["Norm. Cases"] = cov_data["Cases"] / cov_data["Population"] * norm
cov_data["Norm. Deaths"] = cov_data["Deaths"] / cov_data["Population"] * norm

# Days since first case
cov_data["Days Elapsed"] = cov_data["Date"] - cov_data.groupby("Country")["Date"].transform("first")
# Convert from timedelta objects to int due to Plotly bug
cov_data["Days Elapsed"] = cov_data["Days Elapsed"].dt.days

# Plots
fig = px.line(cov_data, x="Days Elapsed", y="Cases", color="Country",
        title="Total cases", hover_data=["Population"])
pio.write_html(fig, file="docs/plots/cases.html")

fig = px.line(cov_data, x="Days Elapsed", y="Deaths", color="Country",
        title="Total deaths", hover_data=["Population"])
pio.write_html(fig, file="docs/plots/deaths.html")

fig = px.line(cov_data, x="Days Elapsed", y="Cases", color="Country",
        log_x=True, log_y=True, title="Total cases", hover_data=["Population"])
pio.write_html(fig, file="docs/plots/cases_log.html")

fig = px.line(cov_data, x="Days Elapsed", y="Deaths", color="Country",
        log_x=True, log_y=True, title="Total deaths", hover_data=["Population"])
pio.write_html(fig, file="docs/plots/deaths_log.html")

#----------

fig = px.line(cov_data, x="Days Elapsed", y="Norm. Cases", color="Country",
        title="Cases every 100,000 inhabitants", hover_data=["Population"])
pio.write_html(fig, file="docs/plots/norm_cases.html")

fig = px.line(cov_data, x="Days Elapsed", y="Norm. Deaths", color="Country",
        title="Deaths every 100,000 inhabitants", hover_data=["Population"])
pio.write_html(fig, file="docs/plots/norm_deaths.html")

fig = px.line(cov_data, x="Days Elapsed", y="Norm. Cases", color="Country",
        log_x=True, log_y=True, title="Cases every 100,000 inhabitants",
        hover_data=["Population"])
pio.write_html(fig, file="docs/plots/norm_cases_log.html")

fig = px.line(cov_data, x="Days Elapsed", y="Norm. Deaths", color="Country",
        log_x=True, log_y=True,title="Deaths every 100,000 inhabitants",
        hover_data=["Population"])
pio.write_html(fig, file="docs/plots/norm_deaths_log.html")
