# Standard library imports
import os

import fitz

# Local application imports



class Stamper:
    """ Class prints stamps on invoices"""

    def __init__(self, invoice_id, db, company_id):
        self.invoice_id = invoice_id
        self.db = db
        self.company_id = company_id
        self.stamp_list = []

    def get_all_stamps(self) -> list:
        stamps = self.db.query.filter_by(invoice_id=self.invoice_id).all()

        text, value = [],[]
        for stamp in stamps:
            text.append(stamp.stamp.text)
            value.append(stamp.stamp_value)

        self.stamp_list = list(zip(text,value))

    def make_stamp_text(self) -> str:
        final_string = ""
        for stamp_text, stamp_value in self.stamp_list:
            stamp_value = "" if stamp_value == None else stamp_value
            final_string += f"{stamp_text} - {stamp_value}"
            final_string += "\n"
        return final_string

    def convert_non_polish_chars(self, text: str) -> str:
        polish_chars = {"Ą":"A","ą":"a","Ć":"C","ć":"c","Ę":"E","ę":"e","Ł":"L","ł":"l","Ó":"O","ó":"o","Ń":"N","ń":"n","Ś":"S","ś":"s","Ż":"Z","ż":"z","Ź":"Z","ź":"z"}

        for k, v in polish_chars.items():
            text = text.replace(k, v)

        return text

    def add_stamps(self) -> str:
        invoice = self.db.query.filter_by(invoice_id=self.invoice_id).first()
        invoice_path = invoice.invoice.filename

        doc = fitz.open(invoice_path, filetype="pdf")
        page = doc[0]

        p_ratio = [0.1, 0.92, 0.7, 0.99]

        rect_data = [p_ratio[0]*page.MediaBoxSize[0],
                     p_ratio[1]*page.MediaBoxSize[1],
                     p_ratio[2]*page.MediaBoxSize[0],
                     p_ratio[3]*page.MediaBoxSize[1]]

        rect = fitz.Rect(*rect_data)
        text = self.make_stamp_text()
        text = self.convert_non_polish_chars(text)
        page.clean_contents()
        page.drawRect(rect, color=(1,1,0), fill=(1,1,1))
        rc = page.insertTextbox(rect, text, fontsize=8, border_width=2)

        _, output_filename = os.path.split(invoice_path)
        output_path = os.path.join("allocate","uploads", str(self.company_id), "stamped", output_filename)
        doc.save(output_path)
        return output_path