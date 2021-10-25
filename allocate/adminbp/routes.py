

# Third party imports
from flask_admin.contrib.sqla import ModelView
from flask import Blueprint

# Local application imports
from allocate import admin, db
from allocate.models import Company, User, Role, Stamp, Invoice, InvoiceStamps


adminblueprint =  Blueprint('adminblueprint', __name__)


class MyModelView(ModelView):
    def is_accessible(self):
        return True
        # if current_user.is_authenticated and current_user.role.name == 'Super Admin':
        #     return True
        # else:
        #     return False



admin.add_view(MyModelView(Company, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(Stamp, db.session))
admin.add_view(MyModelView(Invoice, db.session))
admin.add_view(MyModelView(InvoiceStamps, db.session))