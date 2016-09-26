# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from models import Project

projects_blueprint = Blueprint('projects', __name__, template_folder='templates')


@projects_blueprint.route('/projects')
def projects():
    all_projects = Project.query.order_by(Project.priority, Project.name).all()
    return render_template("projects.html", projects=all_projects)


@projects_blueprint.route('/projects/<slug>')
def project(slug):
    current_project = Project.query.filter_by(slug=slug).first_or_404()
    return render_template("project.html", project=current_project)
