# Standard library imports

# Third party imports
from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import current_user, login_required

# Local application imports
from allocate.stamps.import_stamps import StampsImport
from allocate.models import Stamp
from allocate import db

stamps =  Blueprint('stamps', __name__)

@stamps.route("/stamps",methods=["GET"])
@login_required
def stamps_list():
    company_id = current_user.company.id
    stamps = Stamp.query.filter_by(company_id=company_id).all()

    return render_template("stamps.html", stamps=stamps)

@stamps.route("/stamps/import", methods=['GET','POST'])
@login_required
def import_stamps():
    company_id = current_user.company.id

    if request.method == "POST":
        uploaded_file = request.files['formStampCSV']

        if uploaded_file.filename.endswith(".csv"):
            stamps_import = StampsImport(uploaded_file)
            for _stamp in stamps_import.stamp_list:
                stamp = Stamp(text=_stamp, company_id=company_id)
                db.session.add(stamp)
            db.session.commit()
            return redirect(url_for('stamps.stamps_list'))

    return render_template('stamps_import.html')

@stamps.route("/stamps/add", methods=["POST"])
@login_required
def add_stamp():
    data = request.form['stamp_text']
    company_id = current_user.company.id
    print(data)
    stamp = Stamp(text=data, company_id=company_id)
    db.session.add(stamp)
    db.session.commit()
    return redirect(url_for("stamps.stamps_list"))

@stamps.route("/stamps/delete/<id>")
@login_required
def delete_stamp(id):
    company_id = current_user.company.id
    obj = Stamp.query.filter_by(id=id).first()
    if obj.company_id == int(company_id):
        db.session.delete(obj)
        db.session.commit()

        return redirect(url_for('stamps.stamps_list'))