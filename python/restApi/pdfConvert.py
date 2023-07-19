#! /usr/bin/env python3

from fpdf import FPDF

pdf = FPDF()

pdf.add_page()

pdf.set_font("Arial", size=7)

f = open('placeOrderCurl.txt', 'r')

for x in f:
    pdf.multi_cell(200, 10, txt=x, ln=1, align='C')


pdf.output("curlPlaceOrder.pdf")
