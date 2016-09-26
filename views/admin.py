# -*- coding: utf-8 -*-

import re
import os
import json
from http import HTTPStatus
from flask import Blueprint, render_template, request, url_for, redirect, current_app, jsonify, flash
from flask_login import login_required
from flask_principal import Permission, RoleNeed
from werkzeug.utils import secure_filename
from extensions import sqlalchemy as db
from models import Article, Project, Tag

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')
admin_permission = Permission(RoleNeed("admin"))


@admin_blueprint.route('/admin')
@login_required
@admin_permission.require()
def admin():
    return render_template("admin.html")


# --- News ---


@admin_blueprint.route('/admin/articles')
@login_required
@admin_permission.require()
def admin_articles():

    articles = Article.query.all()
    return render_template("admin_articles.html", articles=articles)


@admin_blueprint.route('/admin/articles/new')
@admin_blueprint.route('/admin/articles/<int:article_id>')
@login_required
@admin_permission.require()
def admin_article(article_id=None, title="", content="", tag_ids=None):
    article = None
    if article_id:
        article = Article.query.get_or_404(article_id)
    tags = Tag.query.all()
    return render_template("admin_article.html", article=article, tags=tags,
                           title=title, content=content, tag_ids=tag_ids or [])


@admin_blueprint.route('/admin/articles/new', methods=['POST'])
@admin_blueprint.route('/admin/articles/<int:article_id>', methods=['POST'])
@login_required
@admin_permission.require()
def admin_article_update(article_id=None):

    if article_id:
        article = Article.query.get_or_404(article_id)
    else:
        article = Article()

    title = request.form['title'].strip()
    content = request.form['content'].strip()
    try:
        tag_ids = json.loads(request.form["tag-ids"])
    except (ValueError, TypeError):
        flash("Les tags ne sont pas valides", "error")
        return admin_article(article_id, title, content)

    if not title:
        flash("Le titre est vide", "error")
        return admin_article(article_id, title, content, tag_ids)

    if not content:
        flash("Le contenu est vide", "error")
        return admin_article(article_id, title, content, tag_ids)

    slug = re.sub('[^A-Za-z0-9]+', '_', title.lower())

    tags = []
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        if not tag:
            flash("Les tags ne sont pas valides", "error")
            return admin_article(article_id, title, content, tag_ids)
        tags.append(tag)

    image = request.files.get("image")
    if image.filename:
        _, extension = os.path.splitext(image.filename)
        filename = os.path.join('images', 'articles', secure_filename(slug) + extension)
        image.save(os.path.join(current_app.static_folder, filename))
        article.image = filename
    elif not article.image:
        flash("L'image n'est pas renseignée", "error")
        return admin_article(article_id, title, content, tag_ids)

    article.title = title
    article.slug = slug
    article.content = content
    article.tags = tags

    db.session.add(article)
    db.session.commit()

    return redirect(url_for('admin.admin_article', article_id=article.id))


@admin_blueprint.route('/admin/article/<int:article_id>/delete')
@login_required
@admin_permission.require()
def admin_article_delete(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('admin.admin_articles'))


# --- Projects ---


@admin_blueprint.route('/admin/projects')
@login_required
@admin_permission.require()
def admin_projects():

    projects = Project.query.all()
    return render_template("admin_projects.html", projects=projects)


@admin_blueprint.route('/admin/projects/new')
@admin_blueprint.route('/admin/projects/<int:project_id>')
@login_required
@admin_permission.require()
def admin_project(project_id=None, name="", url="", description="", tag_ids=None):
    project = None
    if project_id:
        project = Project.query.get_or_404(project_id)

    tags = Tag.query.all()

    return render_template("admin_project.html", project=project, tags=tags,
                           name=name, url=url, description=description, tag_ids=tag_ids or [])


@admin_blueprint.route('/admin/projects/new', methods=['POST'])
@admin_blueprint.route('/admin/projects/<int:project_id>', methods=['POST'])
@login_required
@admin_permission.require()
def admin_project_update(project_id=None):

    if project_id:
        project = Project.query.get_or_404(project_id)
    else:
        project = Project()

    name = request.form['name']
    url = request.form['url']
    description = request.form['description']
    try:
        tag_ids = json.loads(request.form["tag-ids"])
    except (ValueError, TypeError):
        flash("Les tags ne sont pas valides", "error")
        return admin_project(project_id, name, url, description)

    if not name:
        flash("Le nom est vide", "error")
        return admin_project(project_id, name, url, description, tag_ids)
    if not url:
        flash("L'url n'est pas valide", "error")
        return admin_project(project_id, name, url, description, tag_ids)
    if not description:
        flash("La description est vide", "error")
        return admin_project(project_id, name, url, description, tag_ids)

    slug = re.sub('[^A-Za-z0-9]+', '_', name.lower())

    tags = []
    for tag_id in tag_ids:
        tag = Tag.query.get(tag_id)
        if not tag:
            flash("Les tags ne sont pas valides", "error")
            return admin_project(project_id, name, url, description, tag_ids)
        tags.append(tag)

    image = request.files.get("image")
    if image.filename:
        _, extension = os.path.splitext(image.filename)
        filename = os.path.join('images', 'projects', secure_filename(slug) + extension)
        image.save(os.path.join(current_app.static_folder, filename))
        project.image = filename
    elif not project.image:
        flash("L'image n'est pas renseignée", "error")
        return admin_project(project_id, name, url, description, tag_ids)

    project.name = name
    project.slug = slug
    project.url = url
    project.description = description
    project.tags = tags

    db.session.add(project)
    db.session.commit()

    return redirect(url_for('admin.admin_project', project_id=project.id))


@admin_blueprint.route('/ajax/admin/projects/priority', methods=['POST'])
@login_required
@admin_permission.require()
def ajax_admin_projects_update_priority():

    project_ids = request.form.getlist("project_ids", type=int)
    all_projects = Project.query.all()

    if len(all_projects) != len(set(project_ids)):
        result = jsonify(message="Il manque des projets")
        result.status_code = HTTPStatus.BAD_REQUEST
        return result

    projects_by_id = {project.id: project for project in all_projects}
    for priority, project_id in enumerate(project_ids, start=1):
        if project_id not in projects_by_id:
            result = jsonify(message="Le projet n'est pas valide")
            result.status_code = HTTPStatus.BAD_REQUEST
            return result
        projects_by_id[project_id].priority = priority

    db.session.commit()
    return jsonify(message="Les priorités ont été mises à jour")


@admin_blueprint.route('/admin/projects/<int:project_id>/delete')
@login_required
@admin_permission.require()
def admin_project_delete(project_id):
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('admin.admin_projects'))


# --- Tags ---


@admin_blueprint.route('/admin/tags')
@login_required
@admin_permission.require()
def admin_tags():

    tags = Tag.query.all()
    return render_template("admin_tags.html", tags=tags)


@admin_blueprint.route('/admin/tags/new')
@admin_blueprint.route('/admin/tags/<int:tag_id>')
@login_required
@admin_permission.require()
def admin_tag(tag_id=None, name=""):
    tag = None
    if tag_id:
        tag = Tag.query.get_or_404(tag_id)
    return render_template("admin_tag.html", tag=tag, name=name)


@admin_blueprint.route('/admin/tags/new', methods=['POST'])
@admin_blueprint.route('/admin/tags/<int:tag_id>', methods=['POST'])
@login_required
@admin_permission.require()
def admin_tag_update(tag_id=None):

    if tag_id:
        tag = Tag.query.get_or_404(tag_id)
    else:
        tag = Tag()

    name = request.form['name']
    if not name:
        flash("Le nom n'est pas valide", "error")
        return admin_tag(tag_id)

    slug = re.sub('[^A-Za-z0-9]+', '_', name.lower())

    image = request.files.get("image")
    if image.filename:
        _, extension = os.path.splitext(image.filename)
        filename = os.path.join('images', 'tags', secure_filename(slug) + extension)
        image.save(os.path.join(current_app.static_folder, filename))
        tag.image = filename
    elif not tag.image:
        flash("L'image n'est pas renseignée", "error")
        return admin_tag(tag_id)

    tag.name = name
    tag.slug = slug

    db.session.add(tag)
    db.session.commit()

    return redirect(url_for('admin.admin_tag', tag_id=tag.id))


@admin_blueprint.route('/admin/tags/<int:tag_id>/delete')
@login_required
@admin_permission.require()
def admin_tag_delete(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for('admin.admin_tags'))
