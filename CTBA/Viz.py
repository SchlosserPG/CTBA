import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "data/livedata-weekly-job-changes-2025-07-23.csv"
df = pd.read_csv(file_path)

# Display the first few rows and column names to understand the structure
df.head(), df.columns

# Filter for departures
departures = df[df['arrival/departure'] == 'departure']

# Get top 10 companies with the most departures
top_departure_companies = departures['previous_job.company.name'].value_counts().nlargest(10)

# Top Companies by Number of Departures
plt.figure(figsize=(10, 6))
sns.barplot(
    x=top_departure_companies.values,
    y=top_departure_companies.index,
    hue=top_departure_companies.index,   # map palette to the y-axis categories
    dodge=False,
    legend=False,
    palette="coolwarm"
)
plt.title("Top Companies by Number of Departures")
plt.xlabel("Number of Departures")
plt.ylabel("Company")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()




##Plot Top 10 Job Functions by Number of Departures
# Count top 10 job functions
departures_by_function = departures['previous_job.function'].value_counts().nlargest(10)

# Top 10 Job Functions by Number of Departures
plt.figure(figsize=(10, 6))
sns.barplot(
    x=departures_by_function.values,
    y=departures_by_function.index,
    hue=departures_by_function.index,    # map palette to the y-axis categories
    dodge=False,
    legend=False,
    palette="Reds_r"
)
plt.title("Top 10 Job Functions by Number of Departures")
plt.xlabel("Number of Departures")
plt.ylabel("Job Function")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()


## Plotting weekly job arrivals vs. departures
# Convert date columns to datetime
df['current_job.started_at'] = pd.to_datetime(df['current_job.started_at'], errors='coerce')
df['previous_job.ended_at'] = pd.to_datetime(df['previous_job.ended_at'], errors='coerce')

# Create a 'week' column for aggregation
df['week'] = df.apply(
    lambda row: row['current_job.started_at'] if row['arrival/departure'] == 'arrival' else row['previous_job.ended_at'],
    axis=1
).dt.to_period('W').dt.start_time

# Count arrivals and departures by week
weekly_counts = df.groupby(['week', 'arrival/departure']).size().reset_index(name='count')

# Pivot to get arrivals and departures in separate columns
pivot_counts = weekly_counts.pivot(index='week', columns='arrival/departure', values='count').fillna(0)

# Plot the bar chart
plt.figure(figsize=(12, 6))
pivot_counts.plot(kind='bar', stacked=False, color=['green', 'red'])
plt.title("Weekly Job Arrivals vs. Departures")
plt.ylabel("Number of Changes")
plt.xlabel("Week")
plt.xticks(rotation=45)
plt.tight_layout()
plt.legend(title="Type")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

