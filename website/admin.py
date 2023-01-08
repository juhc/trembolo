from flask import abort
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.get_id() == "1":
            return True
        else:
            abort(403)
