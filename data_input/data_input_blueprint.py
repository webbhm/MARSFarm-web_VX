from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime

data_input_blueprint = Blueprint('data_input_blueprint', __name__, template_folder='templates')

# Page functions
# Charts
from functions.GBE_Util import *

# This is working
@data_input_blueprint.route('/input')
def index():
    try:
        print('input/index.html')
        return render_template('data_input/index.html')
    except TemplateNotFound:
        abort(404)
        
# Now working
@data_input_blueprint.route('/input/', defaults={'page': 'index'})
@data_input_blueprint.route('/input/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template: %s.html' % page)
        return render_template('/data_input/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
        
#--------------- GBE Charts below here --------------------------
        
@data_input_blueprint.route('/input/pheno', methods=['GET', 'POST'])
def pheno():
    # Phenotype data entry - basic plant data
    print("Pheno")
    try:
        # FIX: need to get dates from trial, and attribute from input
        title = "Phenotype Data Entry"
        farm = "OpenAgBloom"
        field = "GBE_D_3"
        experiment = "GBE_E_3"
        trial = "GBE_T_3"
        plants = [{"id":1},{"id":2},{"id":3},{"id":4}]
        week = 4
        page_data = {'title':title, 'farm':farm, 'field':field, 'experiment':experiment, 'trial':trial, 'plants':plants, 'week':week}
        #page_data = {'title':title, 'farm':farm, 'field':field, 'experiment':experiment, 'trial':trial}
        print("Render Pheno Template")
        return render_template('/data_input/phenotype_input.html', data=page_data)
    except Exception as e:
        print("Except Phenotype", e)
        abort(404)    