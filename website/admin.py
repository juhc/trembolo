from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class AdminView(ModelView):
    def is_accessible(self):
        print(current_user.get_id)
        if current_user.is_authenticated:
            if current_user.get_id == 'admin@trembola.com':
                return True
            return True
        else:
            abort(403)