# Standard library imports
import os
# Third party imports
import zipfile

from flask import Blueprint, request, redirect, url_for, send_file
from flask_login import login_required, current_user

# Local application imports
from allocate.stampsInvoices.utils_stampsInvoices import Stamper

from allocate.models import InvoiceStamps
from allocate import db

stampsInvoices = Blueprint("stampsInvoices", __name__)

@stampsInvoices.route("/invoicestamp/add/invoice/<invoice_id>", methods=["POST"])
@login_required
def add_invoice_stamp(invoice_id):
    data = request.form
    invoice_stamp = InvoiceStamps(invoice_id=invoice_id,
                                  stamp_id=data['stamp_text'],
                                  stamp_value=data['stamp_value'])
    db.session.add(invoice_stamp)
    db.session.commit()
    return redirect(request.referrer)


@stampsInvoices.route("/invoicestamp/delete/<id>", methods=["GET","POST"])
@login_required
def delete_invoice_stamp(id):
    invoice_stamp = InvoiceStamps.query.filter_by(id=id).first()
    db.session.delete(invoice_stamp)
    db.session.commit()
    return redirect(request.referrer)


@stampsInvoices.route("/printstamp/<id>")
@login_required
def print_stamp(id):
    company_id = current_user.company.id
    stamper = Stamper(id, InvoiceStamps, company_id)
    stamper.get_all_stamps()
    stamper.add_stamps()
    return redirect(url_for('invoices.invoices_list'))


@stampsInvoices.route("/printstamp/add/batch", methods=["GET", "POST"])
@login_required
def print_stamp_batch():
    if request.method == "POST":
        company_id = current_user.company.id
        zipfolder = zipfile.ZipFile(os.path.join("allocate",'Invoices.zip'), 'w',
                                    compression=zipfile.ZIP_STORED)
        invoices_paths = []
        invoices = request.json
        print(invoices)
        for invoice in invoices:
            stamper = Stamper(invoice, InvoiceStamps, company_id)
            stamper.get_all_stamps()
            invoice_path = stamper.add_stamps()
            zipfolder.write(invoice_path)
            invoices_paths.append(invoice_path)
        zipfolder.close()
        return "Invoices"

@stampsInvoices.route("/invoices/send/<name>")
@login_required
def send_stamped_invoices(name):
    filename = name+'.zip'
    print(filename)
    return send_file(filename,
                     mimetype='zip',
                     attachment_filename=filename,
                     as_attachment=True)

@stampsInvoices.route("/invoicestamp/add/batch", methods=["GET", "POST"])
@login_required
def stamp_batch_add():
    if request.method == "POST":
        data = request.json
        stamp_id = data['stamp_id']
        invoice_ids = data['invoice_ids']
        for invoice_id in invoice_ids:
            invoice_stamp = InvoiceStamps(invoice_id=int(invoice_id),
                                          stamp_id=stamp_id)
            db.session.add(invoice_stamp)
        db.session.commit()
        return redirect(url_for("invoices.invoices_list"))
    return redirect(url_for("invoices.invoices_list"))
