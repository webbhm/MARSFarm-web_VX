from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

test_blueprint = Blueprint('test_blueprint', __name__, template_folder='templates')

# Page functions
from test.functions.test_chart import get_JSONChart, get_page_data, fmt
from test.functions.user_get_data import get_user_data
from test.functions.test_data import get_test_data

# This is working
@test_blueprint.route('/test')
def index():
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for /test index.html')
        return render_template('test/index.html', data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)

# Now working
@test_blueprint.route('/test/', defaults={'page': 'index'})
@test_blueprint.route('/test/url', defaults={'page': 'url'})
@test_blueprint.route('/test/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('test/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
@test_blueprint.route('/test/dynamic')
def dynamic():

    title = "MarsFarm"
    access = get_user_data('foo')
    data = {"title":title, 'access': access}    
    try:
        return render_template('test/dynamic_load_dropdown.html', data = data)
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)

    
@test_blueprint.route('/test/test_chart', methods=['GET', 'POST'])
def test_chart():
    try:
        data = get_test_data('temperature')
        page_data = get_page_data()
        print(page_data)
        #fig = env_chart(attribute, school, start_date, end_date)
        graphJSON = get_JSONChart(data, fmt)
        print("Render_Template")
        return render_template('test/test_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        print("Except test_chart", e)
        abort(404)