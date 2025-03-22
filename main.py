# main.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from bot.invoice_generator import generate_invoice_pdf
from bot.whatsapp_sender import send_whatsapp_message

app = FastAPI()

class InvoiceRequest(BaseModel):
    customer_id: str
    products: list  # list of product_id and quantity

@app.post("/generate_invoice/")
async def generate_invoice(data: InvoiceRequest):
    pdf_path = generate_invoice_pdf(data.customer_id, data.products)
    send_whatsapp_message(data.customer_id, pdf_path)
    return {"status": "sent", "pdf": pdf_path}
