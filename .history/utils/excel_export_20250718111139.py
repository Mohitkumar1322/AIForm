import pandas as pd
import json
from models.models import Form, Response
from app import db

def export_to_excel(form_id):
    form = Form.query.get(form_id)
    responses = Response.query.filter_by(form_id=form_id).all()
    field_names = json.loads(form.fields)
    data = [json.loads(resp.data) for resp in responses]
    df = pd.DataFrame(data, columns=field_names)
    df.to_excel(f"form_{form_id}_responses.xlsx", index=False)
