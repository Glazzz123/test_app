from flask import Flask, request, jsonify
from tinydb import TinyDB
import re
from datetime import datetime

app = Flask(__name__)
db = TinyDB('db.json')


def validate_field(value):
    # Дата
    date_formats = ["%d.%m.%Y", "%Y-%m-%d"]
    for fmt in date_formats:
        try:
            datetime.strptime(value, fmt)
            return "date"
        except ValueError:
            pass
    # Телефон
    if re.match(r"^\+7 \d{3} \d{3} \d{2} \d{2}$", value):
        return "phone"
    # Email
    if re.match(r"^[^@]+@[^@]+\.[^@]+$", value):
        return "email"
    # Текст
    return "text"

@app.route('/get_form', methods=['POST'])
def get_form():
    data = request.form.to_dict()
    templates = db.all()

    for template in templates:
        template_fields = template['fields']
        match = True
        for field_name, field_type in template_fields.items():
            if field_name not in data or validate_field(data[field_name]) != field_type:
                match = False
                break
        if match:
            return jsonify({"template_name": template["name"]})

    # Если шаблон не найден
    result = {k: validate_field(v) for k, v in data.items()}
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

