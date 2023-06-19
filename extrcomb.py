from reportlab.pdfgen import canvas
import requests
from bs4 import BeautifulSoup

def scrape():
    url = "https://ktu.edu.in/eu/core/announcements.htm"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find("table", {"class": "ktu-news"})
        tr_list = table.findAll("tr")

        tr = tr_list[1] # Retrieve only the second row (i.e., the first notification)

        content = ''

        for li in tr.find_all("li"):
            texts = li.find_all(string=True)
            for text in texts:
                if len(text) > 25:
                    content += text.replace('\n','').replace('\r','')+'\n'

        return content.strip()

    except Exception as e:
        print(str(e))

# Scrape the content
content = scrape()

# Create a PDF file
pdf_filename = "announcements.pdf"
pdf = canvas.Canvas(pdf_filename)

# Set the font and size
pdf.setFont("Helvetica", 12)

# Write the content to the PDF
pdf.drawString(30, 750, content)

# Save and close the PDF
pdf.save()

print(f"Content written to {pdf_filename} successfully.")
