import smtplib
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import ssl
import time
import random
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

# ==============================================================================
# ⚙️ CONFIGURATION
# ==============================================================================
# YOUR GMAIL ADDRESS AND APP PASSWORD (NO SPACES IN PASSWORD)
SENDER_EMAIL = "greencanyonecovillage@gmail.com"
APP_PASSWORD = "ygvuqukaweimbdve" # e.g. "abcd efgh ijkl mnop" -> "abcdefghijklmnop"

DATABASE_FILE = "Galt_B2B_Outreach_Database.xlsx"
# Optional: If you have exported your marketing package to PDF, put its name here. 
# Leave empty string "" if you don't want to attach a file.
ATTACHMENT_FILE = "" 

# Set to True to test the script WITHOUT actually sending emails.
DRY_RUN = False  

# ==============================================================================
# 📧 EMAIL TEMPLATE
# ==============================================================================
def get_html_body(contact_person, agency_name):
    """Generates the HTML body of the email based on the recipient's details."""
    
    # Logic to handle if we have a specific contact person or just an agency name
    if pd.isna(contact_person) or not contact_person or str(contact_person).lower() == "nan":
        greeting = f"Dear {agency_name} Team,"
    else:
        # e.g., "Dear John Doe,"
        greeting = f"Dear {contact_person},"

    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; font-size: 14px; color: #333; line-height: 1.6;">
        <p>{greeting}</p>
        
        <p>I hope this email finds you well.</p>
        
        <p>My name is Nodar, representing <strong>Green Canyon</strong>, a premium eco-village and high-yield real estate project located in the breathtaking mountains of Tsalka, Georgia.</p>
        
        <p>Knowing your agency's expertise in providing exceptional overseas real estate and high-ROI opportunities to your clients, I am reaching out to propose a highly lucrative B2B partnership.</p>
        
        <p>Georgia has rapidly become one of the top destinations for international property investment, and Green Canyon is uniquely positioned to offer an unparalleled product for investors seeking stable, hands-off passive income.</p>
        
        <h3 style="color: #2F4F4F;">Why Green Canyon is the perfect addition to your portfolio:</h3>
        <ul style="margin-bottom: 20px;">
            <li><strong>High Yield:</strong> A projected <strong>9-12% annual ROI</strong>, outperforming many traditional real estate markets.</li>
            <li><strong>100% Hassle-Free:</strong> We provide complete turnkey management with a <strong>60/40 profit split</strong> <span style="color: #666; font-size: 12px;">(60% to the investor, 40% to management, calculated <em>after</em> booking platform and service fees are deducted)</span>. We handle all marketing, bookings, guest relations, and maintenance. Your clients simply check their dashboard and collect returns.</li>
            <li><strong>Eco-Luxury Premium:</strong> Situated at 1500m altitude with clean air, sustainable infrastructure, and modern off-grid capabilities—highly attractive to the modern wellness-oriented investor.</li>
            <li><strong>Easy Foreign Ownership:</strong> Full legal ownership for foreigners with an automated, remote purchasing process.</li>
        </ul>
        
        <p>We invite you to explore our live inventory, cottage types, and interactive ROI calculator on our B2B Sales Portal:<br>
        👉 <strong><a href="https://green-canyon-sales-portal.netlify.app" style="color: #0066cc; font-size: 16px;">Green Canyon B2B Sales Portal</a></strong></p>
        
        <p><strong>What's in it for you?</strong><br>
        We offer a highly competitive commission structure for our international broker network and provide fully translated marketing materials (brochures, renders, financials) ready for your clients.</p>
        
        <p>I would love to schedule a brief 10-minute introductory call to show you the portal and discuss how we can structure our commission agreement. Are you available for a quick chat next week?</p>
        
        <p>Best regards,</p>
        
        <p style="margin-top: 30px;">
            <strong style="font-size: 16px;">Nodar</strong><br>
            <span style="color: #555;">Sales Director / Green Canyon</span><br>
            <a href="https://green-canyon-sales-portal.netlify.app" style="color: #0066cc;">Green Canyon Sales Portal</a><br>
            Website: <a href="https://www.greencanyon.ge" style="color: #0066cc;">www.greencanyon.ge</a><br>
            Phone/WhatsApp: +995597455545<br>
            Email: greencanyonecovillage@gmail.com
        </p>
      </body>
    </html>
    """
    return html

# ==============================================================================
# 🚀 MAIN MAILER LOGIC
# ==============================================================================
def main():
    print("🚀 Starting B2B Outreach Automation...")
    
    if DRY_RUN:
        print("⚠️  DRY_RUN is ENABLED. No emails will actually be sent.")
        print("Set DRY_RUN = False in the script when you're ready to send.\n")

    if APP_PASSWORD == "PUT_YOUR_16_DIGIT_APP_PASSWORD_HERE" and not DRY_RUN:
        print("❌ ERROR: You must input your Google App Password at the top of the script!")
        return

    # 1. Load the database
    try:
        df = pd.read_excel(DATABASE_FILE)
    except FileNotFoundError:
        print(f"❌ ERROR: Cannot find the database file '{DATABASE_FILE}'")
        return

    # Count total valid emails
    valid_contacts = df[df['Email'].notna() & df['Email'].str.contains('@')]
    print(f"📊 Found {len(valid_contacts)} valid contacts in the database.")
    
    if len(valid_contacts) == 0:
        print("❌ No valid emails found in the database. Exiting.")
        return

    # 2. Setup Server Connection
    # We use SSL context for secure connection
    context = ssl.create_default_context()
    server = None
    
    if not DRY_RUN:
        try:
            print("⏳ Connecting to Gmail SMTP server...")
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
            server.login(SENDER_EMAIL, APP_PASSWORD)
            print("✅ Successfully logged into Gmail.")
        except Exception as e:
            print(f"❌ Login failed: {e}")
            print("Make sure you generated an App Password correctly and 2FA is enabled.")
            return

    # 3. Iterate over the contacts and send
    sent_count = 0
    for index, row in valid_contacts.iterrows():
        email_to = str(row['Email']).strip()
        agency = str(row['Agency Name'])
        contact = str(row['Contact Person'])
        
        # Prevent sending to the placeholder test emails if not careful
        if "info@mira.ae" in email_to and not DRY_RUN:
            print(f"⏩ Skipping {email_to} (looks like a placeholder)")
            continue

        print(f"--------------------------------------------------")
        print(f"📨 Preparing email for: {agency} ({email_to})")
        
        msg = MIMEMultipart()
        msg['From'] = f"Nodar | Green Canyon <{SENDER_EMAIL}>"
        msg['To'] = email_to
        msg['Subject'] = "Exclusive Partnership: High-Yield Eco-Resort Investment in Georgia (9-12% ROI)"
        
        body_html = get_html_body(contact_person=contact, agency_name=agency)
        msg.attach(MIMEText(body_html, 'html'))
        
        # Attach a PDF if specified
        if ATTACHMENT_FILE and os.path.exists(ATTACHMENT_FILE):
            try:
                with open(ATTACHMENT_FILE, "rb") as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(ATTACHMENT_FILE))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(ATTACHMENT_FILE)}"'
                msg.attach(part)
                print(f"📎 Attached {ATTACHMENT_FILE}")
            except Exception as e:
                print(f"⚠️ Could not attach file: {e}")

        # Send the email
        if DRY_RUN:
            print(f"✅ [DRY RUN] Would send to {email_to}")
        else:
            try:
                server.send_message(msg)
                print(f"✅ Email SUCCESS to {email_to}")
                sent_count += 1
                
                # Antispam Delay: Wait a random amount of time (45 to 90 seconds) between emails
                # Skip waiting if it is the very last email
                if index < len(valid_contacts) - 1:
                    delay = random.randint(45, 90)
                    print(f"⏳ SPAM PREVENTION: Sleeping for {delay} seconds before next email...")
                    time.sleep(delay)
                    
            except Exception as e:
                print(f"❌ Failed to send to {email_to}: {e}")

    # Cleanup
    if server:
        server.quit()
        
    print(f"\n🎉 Finished! Successfully sent {sent_count} emails out of {len(valid_contacts)} valid contacts.")

if __name__ == "__main__":
    main()
