from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

example_blueprint = Blueprint('example_blueprint', __name__)


# This is working
# Now working
@example_blueprint.route('/', defaults={'page': 'index'})
@example_blueprint.route('/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}        
    try:
        print('%s.html' % page)
        return render_template('%s.html' % page, data = {"title":title})
    except TemplateNotFound:
        abort(404)