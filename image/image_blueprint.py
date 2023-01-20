from flask import Blueprint, render_template, abort, request, session, redirect, url_for
from jinja2 import TemplateNotFound
from image.functions.Image_Query import images

image_blueprint = Blueprint('image_blueprint', __name__, template_folder='templates')

# This is working
@image_blueprint.route('/image')
def index():
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for image/index.html')
        return render_template('image/index.html', data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)

# Now working
@image_blueprint.route('/image/', defaults={'page': 'index'})
@image_blueprint.route('/image/url', defaults={'page': 'url'})
@image_blueprint.route('/imge/<page>')
def show(page):
    title = "MarsFarm"
    data = {"title":title}    
    try:
        print('Render Template for %s.html' % page)
        return render_template('image/%s.html' % page, data = {"title":title})
    #    except TemplateNotFound:
    except Exception as e:
        print("Except", e)
        abort(404)
# ----------------- MARSFarm specific stuff -----------------        
@image_blueprint.route('/image/plant_image', methods=['GET'])
def plant_image():
    # display latest jpg image or gif image
    farm = "OpenAgBloom"
    field = "GBE_D_3"    
    from gbet_charts.functions.ImageRetrieve import get_jpg
    
    start_date_str, name, image = get_jpg(farm, field)

    title = "Latest hourly jpg image"
    alt = "latest hourly plant image"

    #print(image)
    end_date_str = start_date_str
    description = "Development of plant image display"
    image_type = 'jpg'
    
    page_data = {"title":title, "description":description,
            "farm":farm,
            "field":field,
            "start_date_str":start_date_str,
            "end_date_str":end_date_str,
            "image_type":image_type,
            "alt":alt,
            "image":image
                 }        

    #print(page_data)
    try:
        print("Render Plant_Image")
        return render_template('image/image.html', data=page_data)
    except Exception as e:
        data = {"msg":"Failure getting Image", "err":e}
        return render_template('error.html', data=data)
   
@image_blueprint.route('/image/plant_gif', methods=['GET'])
def plant_gif():
    # display latest jpg image or gif image
    farm = "OpenAgBloom"
    field = "GBE_D_3"    
    from gbet_charts.functions.ImageRetrieve import get_gif
    start_date_str, end_date_str, name, image = get_gif(farm, field)
    title = "Daily GIF of trial"
    alt = "Daily GIF of trial"
    farm = "OpenAgBloom"
    field = "GBE_D_3"
    description = "GIF since start of trial"
    image_type = 'gif'
    
    page_data = {"title":title, "description":description,
            "farm":farm,
            "field":field,
            "start_date_str":start_date_str,
            "end_date_str":end_date_str,
            "image_type":image_type,
            "alt":alt,
            "image":image
                 }        

    #print(page_data)
    try:
        print("Render Plant_GIF")
        return render_template('image/gif.html', data=page_data)
    except Exception as e:
        data = {"msg":"Failure getting gif", "err":e}
        return render_template('error.html', data=data)
    
@image_blueprint.route('/image/gallery', methods=['GET'])
def gallery():
    # gallery of all trial images
    trial = "GBE_T_3"    
    farm = "OpenAgBloom"
    field = "GBE_D_3"
    experiment = "E_3"
    title = "Gallery of Trial Images"
    description = "All images for a Trial"
    
    page_data = {"title":title, "description":description,
        "farm":farm,
        "field":field,
        "experiment":experiment,
        "trial":trial,
        "start_date": "",
        "end_date": "",
        "images":images,
        
        }        

    #print(page_data)
    try:
        print("Render Gallery")
        return render_template('image/ImageGallery.html', data=page_data)
    except Exception as e:
        data = {"msg":"Failure getting gallery", "err":e}
        return render_template('error.html', data=data)

@image_blueprint.route('/image/gallery3', methods=['GET'])
def gallery3():
    # gallery of all trial images
    trial = "GBE_T_3"    
    farm = "OpenAgBloom"
    field = "GBE_D_3"
    experiment = "E_3"
    title = "Gallery of Trial Images"
    description = "All images for a Trial"
    
    page_data = {"title":title, "description":description,
        "farm":farm,
        "field":field,
        "experiment":experiment,
        "trial":trial,
        }        

    #print(page_data)
    try:
        print("Render Gallery")
        return render_template('image/gallery3.html', data=page_data)
    except Exception as e:
        data = {"msg":"Failure getting gallery", "err":e}
        return render_template('error.html', data=data)
