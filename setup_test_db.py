import pandas as pd

# Creating a test database with just 1 row for the user to evaluate
data = {
    "Agency Name": ["Test Agency Dubai"],
    "Country": ["UAE (Dubai)"],
    "Contact Person": ["Nodar"],
    "Email": ["greencanyonecovillage@gmail.com"],
    "Phone": ["+971 4 000 0000"],
    "Potential Interest": ["High-Yield ROI"]
}

df = pd.DataFrame(data)
df.to_excel("Test_Database.xlsx", index=False)
print("✅ Test database set and saved.")
