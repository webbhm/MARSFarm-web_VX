from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from functions.GBE_Query import *
import plotly
import ast

adv_blueprint = Blueprint('adv_blueprint', __name__, template_folder='templates')

# This is working
@adv_blueprint.route('/adv')
def index():
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for index.html')
        return render_template('adv/index.html', data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)

# Now working
@adv_blueprint.route('/adv/', defaults={'page': 'index'})
@adv_blueprint.route('/adv/url', defaults={'page': 'url'})
@adv_blueprint.route('/adv/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('adv/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
        
# -------------------- Experimental Stuff ----------------------
@adv_blueprint.route('/adv/test_query', methods=['GET', 'POST'])
def test_query():

    # weekly change of attribute for a school
    query = request.args.get('query')
    print("Test Query", query)
    title = "Test Query" 
    description = "Write your own query"
    data = []    
    try:
        if query == None:
            query = [{"$match":{
               "status.status_qualifier":SUCCESS,
               "subject.attribute.name":"temp",
               "location.farm.name":"Academir Charter School West",
               "subject.attribute.value":{"$ne":0}
                }}]
        else:
            # change string to list
            query = ast.literal_eval(query)
            
        # limit results to 25 records    
        if "$match" in query:
            query["$match"]["limit"] = 25
        #print(type(query), query)
        page_data = {"title":title, "description":description,
                "query":query, "results":data}
    
        data = run_query(query)
        page_data["results"] = data
        #for d in data:
        #  print("data", d)
        #print(page_data)
        return render_template('adv/query.html', data=page_data)
    except Exception as e:
        page_data = {"title":title, "description":"Failure running query", "query":query, "data":[], "error":e}
        return render_template('error', data=page_data)
    
@adv_blueprint.route('/adv/design_chart', methods=['GET', 'POST'])
def design_chart():  
    # weekly change of attribute for a school
    attribute = request.args.get('attribute') 
    x_axis = request.args.get('x_axis')
    y_axis = request.args.get('y_axis')
    error_plus = request.args.get('error')
    error_minus = request.args.get('error_minus')    
    template = request.args.get('template')
    chart_type = request.args.get('chart_type')
    group = request.args.get('group')    
    #print("Req", school, attribute)
    
    title = "Design Your Own Custom Chart"
    description = "Select your data, then choose a type of chart and decide how the data will be displayed on the chart"
    attributes = ["width", "height", "depth", "edible_mass"]
    
    page_data = {"title":title, "description":description, "attributes":attributes}
    
    if attribute == None:
        return render_template('/adv/design_chart.html', graphJSON=None, data=page_data)        
    if x_axis == "attribute":
        x_axis = attribute
    if y_axis == "attribute":
        y_axis = attribute
    if error_plus == "None":
        error_plus = None
    if error_minus == "None":
        error_minus = None        
    print(title, attribute, chart_type, x_axis, y_axis, group, error_plus, error_minus, template)    
    page_data = {"title":title, "description":description
            }        
    try:
        print("design_chart_data")
        fig = design_chart_data(title, attribute, chart_type, x_axis, y_axis, group, error_plus, error_minus, template)
        print("got fig, now dump")
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        print("render design chart")
        return render_template('adv/design_chart.html', graphJSON=graphJSON, data=page_data)
    except Exception as e:
        data = {"msg":"Failure with Environmental Chart", "err":e}
        return render_template('error.html', data=data)

        

