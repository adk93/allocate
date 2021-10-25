# Standard library imports
import os

# Third party imports
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required, current_user
from sqlalchemy import or_, and_

# Local application imports
from allocate.invoices.utils_invoice import ImportInvoices
from allocate.models import Invoice, Stamp, InvoiceStamps
from allocate import db
from allocate.invoices.forms import InvoiceUploadForm


invoices = Blueprint("invoices", __name__)


@invoices.route("/invoices", methods=["GET"])
@login_required
def invoices_list():

    company_id = current_user.company.id
    invoices = Invoice.query.outerjoin(InvoiceStamps,
                                       Invoice.id == InvoiceStamps.invoice_id).filter(and_(Invoice.company_id == company_id,
                                                                                           or_(Invoice.owner_id==current_user.id,
                                                                                               Invoice.owner_id.in_(map(lambda x: x.id, current_user.inferior_users))))).all()

    stamps = Stamp.query.filter_by(company_id=company_id).all()

    return render_template("invoices.html", stamps=stamps, invoices=invoices)


@invoices.route("/invoices/import", methods=["GET", "POST"])
@login_required
def invoices_import():
    form = InvoiceUploadForm()
    company_id = current_user.company.id
    uploaded_files = request.files.getlist("formFileMultiple")

    if request.method=="POST":

        # secure_filenames = form.get_secure_filename()

        invoices = ImportInvoices(uploaded_files, company_id)

        for filename, thumbnail, display_name in zip(invoices.file_paths, invoices.thumbnails, invoices.filenames):
            i = Invoice(filename=filename,
                        thumbnail=thumbnail,
                        display_name=display_name,
                        company_id=company_id,
                        owner_id=current_user.id)
            db.session.add(i)
        db.session.commit()

        return redirect(url_for('invoices.invoices_list'))
    else:
        return render_template("invoices_import.html", form=form)


@invoices.route("/invoice/<id>")
@login_required
def open_invoice(id):
    company_id = current_user.company.id
    invoice = Invoice.query.outerjoin(InvoiceStamps,
                                      Invoice.id==InvoiceStamps.invoice_id).filter(Invoice.id==id).first()

    stamps = Stamp.query.filter_by(company_id=company_id).all()

    return render_template("invoice.html", invoice=invoice, stamps=stamps)

@invoices.route("/invoice/delete/<id>")
@login_required
def delete_invoice(id):
    company_id = current_user.company.id
    invoice = Invoice.query.filter_by(id=id).first()
    file_path = invoice.filename
    if invoice.company_id == int(company_id):
        if os.path.exists(file_path):
            os.remove(file_path)
    db.session.delete(invoice)
    db.session.commit()
    return redirect(url_for('invoices.invoices_list'))

@invoices.route("/invoice/delete/batch", methods=["GET", "POST"])
@login_required
def delete_invoice_batch():
    if request.method == "POST":
        invoices = request.json
        for invoice_id in invoices:
            invoice = Invoice.query.filter_by(id=invoice_id).first()
            db.session.delete(invoice)
        db.session.commit()
    return redirect(url_for('invoices.invoices_list'))