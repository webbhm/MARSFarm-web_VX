from flask import Flask
from example_blueprint import example_blueprint

print("Test2 Blueprint")

from flask import Flask
from example_blueprint import example_blueprint
from admin.admin_blueprint import admin_blueprint
from trial_charts.trial_charts_blueprint import trial_charts_blueprint
from exp_charts.exp_charts_blueprint import exp_charts_blueprint
from gbe_charts.gbe_charts_blueprint import gbe_charts_blueprint
from gbet_charts.gbet_charts_blueprint import gbet_charts_blueprint
from test.test_blueprint import test_blueprint
from adv.adv_blueprint import adv_blueprint
print("Test2 Blueprint - Dev")

app = Flask(__name__)
app.register_blueprint(example_blueprint)
app.register_blueprint(admin_blueprint)
app.register_blueprint(trial_charts_blueprint)
app.register_blueprint(exp_charts_blueprint)
app.register_blueprint(gbe_charts_blueprint)
app.register_blueprint(gbet_charts_blueprint)
app.register_blueprint(test_blueprint)
app.register_blueprint(adv_blueprint)
#print("Map:", app.url_map)
#print("example Path", example_blueprint.root_path)
#print("trial_charts Path", trial_charts_blueprint.root_path)
#print("exp_chart Path", exp_charts_blueprint.root_path)
#print("gbe_chart Path", gbe_charts_blueprint.root_path)
#print("gbet_chart Path", gbet_charts_blueprint.root_path)
#print("test Path", test_blueprint.root_path)
#print("adv Path", adv_blueprint.root_path)
#print("admin Path", admin_blueprint.root_path)
# debug must be False to work with Gunicorn in production

# debug must be False to work with Gunicorn in production
#app.run(host='0.0.0.0', port=5000, debug=False)