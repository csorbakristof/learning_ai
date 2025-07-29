import pandas as pd

# Read the processed BME data
df = pd.read_excel('../data/bme_topic_data.xlsx')

print("DLXLS Test Results Summary")
print("=" * 50)
print(f"Total students collected: {len(df)}")
print(f"Data columns: {list(df.columns)}")
print("\nStudent Topic Summary:")
print("-" * 50)

for i, row in df.iterrows():
    student_name = row['Hallgató neve']
    category = row['Kategória']
    topic = row['Téma címe']
    print(f"{i+1}. {student_name}")
    print(f"   Category: {category}")
    print(f"   Topic: {topic}")
    print()

# Category distribution
print("Category Distribution:")
print("-" * 30)
category_counts = df['Kategória'].value_counts()
for category, count in category_counts.items():
    print(f"{category}: {count} students")
