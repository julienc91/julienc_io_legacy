# -*- coding: utf-8 -*-

from flask import Blueprint, render_template
from models import Tag, Project, Article

tags_blueprint = Blueprint('tags', __name__, template_folder='templates')


@tags_blueprint.route('/tags')
def tags():
    all_tags = Tag.query.all()
    return render_template("tags.html", tags=all_tags)


@tags_blueprint.route('/tags/<slug>')
def tag(slug):
    current_tag = Tag.query.filter_by(slug=slug).first_or_404()

    articles = Article.query.join(Tag, Article.tags).filter(Tag.id == current_tag.id).all()
    projects = Project.query.join(Tag, Project.tags).filter(Tag.id == current_tag.id).all()

    return render_template("tag.html", tag=current_tag, articles=articles, projects=projects)
