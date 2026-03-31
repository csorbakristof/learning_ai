import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

# Read the CSV file
print("CSV fájl beolvasása...")
df = pd.read_csv('e:/learning_ai/ITMP_http_eloadas/temperatures/temperatures.csv')

# Convert DateTime column to datetime type
df['DateTime'] = pd.to_datetime(df['DateTime'])

# Extract just the date (without time)
df['Date'] = df['DateTime'].dt.date

# Group by date and calculate statistics
print("Napi statisztikák számítása...")
daily_stats = df.groupby('Date')['Temperature'].agg([
    ('Min', 'min'),
    ('Max', 'max'),
    ('Mean', 'mean')
]).reset_index()

# Convert Date back to datetime for plotting
daily_stats['Date'] = pd.to_datetime(daily_stats['Date'])

print(f"Napok száma: {len(daily_stats)}")
print(f"Időszak: {daily_stats['Date'].min()} - {daily_stats['Date'].max()}")

# Create the diagram
fig, ax = plt.subplots(figsize=(16, 8))

# Plot min, max, and mean temperatures
ax.plot(daily_stats['Date'], daily_stats['Min'], 
        label='Minimum', color='blue', linewidth=1, alpha=0.7)
ax.plot(daily_stats['Date'], daily_stats['Max'], 
        label='Maximum', color='red', linewidth=1, alpha=0.7)
ax.plot(daily_stats['Date'], daily_stats['Mean'], 
        label='Átlag', color='green', linewidth=2)

# Fill area between min and max
ax.fill_between(daily_stats['Date'], daily_stats['Min'], daily_stats['Max'], 
                alpha=0.2, color='gray', label='Hőmérséklet-tartomány')

# Formatting
ax.set_xlabel('Dátum', fontsize=12, fontweight='bold')
ax.set_ylabel('Hőmérséklet (°C)', fontsize=12, fontweight='bold')
ax.set_title('T2_Terasz Napi Hőmérséklet Statisztika', fontsize=16, fontweight='bold')
ax.legend(loc='best', fontsize=10)
ax.grid(True, alpha=0.3)

# Format x-axis to show dates nicely
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=45, ha='right')

# Tight layout to prevent label cutoff
plt.tight_layout()

# Save the diagram
output_file = 'e:/learning_ai/ITMP_http_eloadas/temperatures/temperature_diagram.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\nDiagram mentve: {output_file}")

# Show statistics
print("\nStatisztikák:")
print(f"Legalacsonyabb hőmérséklet: {daily_stats['Min'].min():.2f}°C")
print(f"Legmagasabb hőmérséklet: {daily_stats['Max'].max():.2f}°C")
print(f"Átlagos hőmérséklet: {daily_stats['Mean'].mean():.2f}°C")

# Display the plot
plt.show()

print("\nKész!")
