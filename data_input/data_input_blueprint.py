from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound
from datetime import datetime
from functions.Plant import plants_for_trial

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
    trial = "GBE_T_3"    
    plant = plants_for_trial(trial)
    try:
        # FIX: need to get dates from trial, and attribute from input
        title = "Phenotype Data Entry"
        farm = plant["location"]["farm"]
        field = plant["location"]["field"]
        experiment = plant["location"]["experiment"]
        plants = plant["plants"]

        page_data = {'title':title, 'farm':farm, 'field':field, 'experiment':experiment, 'trial':trial, 'plants':plants}
        #page_data = {'title':title, 'farm':farm, 'field':field, 'experiment':experiment, 'trial':trial}
        print("Render Pheno Template")
        return render_template('/data_input/phenotype_input.html', data=page_data)
    except Exception as e:
        print("Except Phenotype", e)
        abort(404)
        
@data_input_blueprint.route('/input/setup', methods=['GET', 'POST'])
def setup():
    # Plant setup - randomize location
    print("Setup")
    trial = "GBE_T_3"    
    plant = plants_for_trial(trial)
    try:
        # FIX: need to get dates from trial, and attribute from input
        title = "Plant Setup"
        farm = plant["location"]["farm"]
        field = plant["location"]["field"]
        experiment = plant["location"]["experiment"]
        plants = plant["plants"]
        page_data = {'title':title, 'farm':farm, 'field':field, 'experiment':experiment, 'trial':trial, 'plants':plants}
        #page_data = {'title':title, 'farm':farm, 'field':field, 'experiment':experiment, 'trial':trial}
        print("Render Plant Template")
        return render_template('/data_input/setup.html', data=page_data)
    except Exception as e:
        print("Except Plant Setup:", e)
        abort(404)            