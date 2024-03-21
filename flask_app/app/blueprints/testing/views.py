from flask import current_app, render_template, render_template_string, request
from . import bp
from app.extensions import db
from sqlalchemy import select
from app.utils import generate_csrf_token
from markupsafe import Markup


@bp.route('/test')
def test_connection():
    try:
        # Execute a simple database query to test the connection
        db.session.execute(select('1')).scalars().first()
        return 'Database connection successful!'
    except Exception as e:
        return f'Database connection failed: {str(e)}'
    

@bp.route('/test/xss', methods=['GET', 'POST'])
def test_xss():
    if request.method == 'POST':
        xss_input = Markup(request.form.get('xss_input'))
        return render_template_string("<h1>XSS Input: {{ xss_input }}</h1>", xss_input=xss_input)
        
    return render_template('testing/test_xss.html')


@bp.route('/test/sql_injection')
def test_sql_injection():
    pass