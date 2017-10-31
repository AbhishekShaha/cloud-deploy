from flask import Flask, render_template
from . import main as main_blueprint


@main_blueprint.route('/', methods=['GET'])
def index():
	return render_template('main/index.html')