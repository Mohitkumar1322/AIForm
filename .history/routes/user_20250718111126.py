
from flask import Blueprint, render_template, request, redirect
from models.models import Form, Response
from app import db
import json
from utils.excel_export import export_to_excel

user_bp = Blueprint('user', __name__)

@user_bp.route('/form/<int:form_id>', methods=['GET', 'POST'])
def form_view(form_id):
    form = Form.query.get_or_404(form_id)
    fields = json.loads(form.fields)
    if request.method == 'POST':
        responses = json.dumps([request.form.get(field, '') for field in fields])
        new_response = Response(form_id=form.id, data=responses)
        db.session.add(new_response)
        db.session.commit()
        export_to_excel(form.id)  # Export latest data
        return "Thanks for submitting!"
    return render_template('form_view.html', form=form, fields=fields)

