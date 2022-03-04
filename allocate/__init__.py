# Standard library imports

# Third Party imports
from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

# Local application imports
from allocate.config import Config

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.email == 'adrian.kaminski@kodilla.com':
            return True
        else:
            return False


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'users.login'
migrate = Migrate()
mail = Mail()
admin = Admin(index_view=MyAdminIndexView(), template_mode='bootstrap4')

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    admin.init_app(app)
    mail.init_app(app)

    with app.app_context():
        db.create_all()

    @app.before_first_request
    def create_tables():
        from allocate.models import Company, User, Role, Stamp, Invoice, InvoiceStamps
        with app.app_context():
            db.create_all()

    from allocate.invoices.routes import invoices
    from allocate.main.routes import main
    from allocate.stamps.routes import stamps
    from allocate.stampsInvoices.routes import stampsInvoices
    from allocate.users.routes import users
    from allocate.adminbp.routes import adminblueprint

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(invoices)
    app.register_blueprint(stamps)
    app.register_blueprint(stampsInvoices)
    app.register_blueprint(adminblueprint)

    return app




# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#         return True
#         # if current_user.is_authenticated and current_user.role.name == 'Super Admin':
#         #     return True
#         # else:
#         #     return False
#
#
# class MyModelView(ModelView):
#     def is_accessible(self):
#         return True
#         # if current_user.is_authenticated and current_user.role.name == 'Super Admin':
#         #     return True
#         # else:
#         #     return False
# #
# # adminbp = Admin(app, index_view=MyAdminIndexView(), template_mode='bootstrap4')
# # adminbp.add_view(MyModelView(Company, db.session))
# # adminbp.add_view(MyModelView(User, db.session))
# # adminbp.add_view(MyModelView(Avatar, db.session))
# # adminbp.add_view(MyModelView(Logo, db.session))
# # adminbp.add_view(MyModelView(Role, db.session))
# # adminbp.add_view(MyModelView(Stamp, db.session))
# # adminbp.add_view(MyModelView(Invoice, db.session))
# # adminbp.add_view(MyModelView(InvoiceStamps, db.session))
# # adminbp.add_view(MyModelView(UsersPermissions, db.session))

