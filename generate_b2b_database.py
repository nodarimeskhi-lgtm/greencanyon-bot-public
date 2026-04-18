import pandas as pd

data = {
    "Agency Name": [
        "Mira Real Estate", 
        "Metropolitan Premium Properties", 
        "Colliers International (MENA)", 
        "RE/MAX Israel", 
        "ExpatHub Georgia", 
        "VESTIN Property", 
        "Savills UK", 
        "Realting Network", 
        "Georgia-Israel Real Estate", 
        "Fam Properties Dubai"
    ],
    "Country": [
        "UAE (Dubai)", 
        "UAE (Dubai)", 
        "UAE (Gulf)", 
        "Israel", 
        "Georgia (Expats)", 
        "Georgia (Expats)", 
        "UK", 
        "Poland/Germany", 
        "Israel", 
        "UAE (Dubai)"
    ],
    "Contact Person": [
        "Sales Director", 
        "Partnership Manager", 
        "Investment Advisor", 
        "Brokerage Partner", 
        "B2B Manager", 
        "B2B Manager", 
        "Global Markets Lead", 
        "Network Coordinator", 
        "Sales Lead", 
        "International Sales"
    ],
    "Email": [
        "info@mira.ae", 
        "partners@metropolitan.realestate", 
        "info.mena@colliers.com", 
        "info@remax.co.il", 
        "info@expathub.ge", 
        "contact@vestinproperty.ge", 
        "international@savills.co.uk", 
        "partners@realting.com", 
        "contact@georgia-israel.com", 
        "info@famproperties.com"
    ],
    "Phone": [
        "+971 4 000 0000", 
        "+971 4 000 0000", 
        "+971 4 000 0000", 
        "+972 3 000 0000", 
        "+995 500 000 000", 
        "+995 500 000 000", 
        "+44 20 0000 0000", 
        "+48 00 000 0000", 
        "+972 5 000 0000", 
        "+971 4 000 0000"
    ],
    "Potential Interest": [
        "High-Yield ROI", 
        "Golden Visa / Residency", 
        "Institutional Investment", 
        "Second Homes", 
        "Expat Resettlement", 
        "Direct Investment", 
        "Luxury/Wellness", 
        "EU Buyers", 
        "Vacation Homes", 
        "High-Yield ROI"
    ]
}

df = pd.DataFrame(data)
df.to_excel("Galt_B2B_Outreach_Database.xlsx", index=False)
print("Excel database generated successfully: Galt_B2B_Outreach_Database.xlsx")
