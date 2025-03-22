# bot/invoice_generator.py
from fpdf import FPDF
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["invoice_bot"]

def generate_invoice_pdf(customer_id, products):
    customer = db.customers.find_one({"customer_id": customer_id})
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Header
    pdf.cell(200, 10, txt="Invoice", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Customer: {customer['name']} | Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True)

    # Table header
    pdf.cell(60, 10, "Product", 1)
    pdf.cell(40, 10, "Quantity", 1)
    pdf.cell(40, 10, "Price", 1)
    pdf.cell(40, 10, "Total", 1)
    pdf.ln()

    total_amount = 0
    for item in products:
        product = db.products.find_one({"product_id": item['product_id']})
        qty = item['quantity']
        price = product['price']
        total = qty * price
        total_amount += total

        pdf.cell(60, 10, product['name'], 1)
        pdf.cell(40, 10, str(qty), 1)
        pdf.cell(40, 10, f"{price:.2f}", 1)
        pdf.cell(40, 10, f"{total:.2f}", 1)
        pdf.ln()

    pdf.cell(180, 10, f"Total Amount: ₹{total_amount:.2f}", 1)

    file_path = f"invoices/invoice_{customer_id}_{datetime.now().timestamp()}.pdf"
    pdf.output(file_path)
    return file_path
