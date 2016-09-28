# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for
from models import Article

articles_blueprint = Blueprint('articles', __name__, template_folder='templates')


@articles_blueprint.route('/')
@articles_blueprint.route('/articles', alias=True)
def articles():
    all_articles = Article.query.all()
    return render_template("articles.html", articles=all_articles)


@articles_blueprint.route('/<int:article_id>', defaults={'slug': None})
@articles_blueprint.route('/<int:article_id>/<slug>', strict_slashes=False)
@articles_blueprint.route('/articles/<int:article_id>', defaults={'slug': None}, alias=True)
@articles_blueprint.route('/articles/<int:article_id>/<slug>', alias=True)
def article(article_id, slug):
    current_article = Article.query.get_or_404(article_id)
    if current_article.slug != slug:
        return redirect(url_for('articles.article', article_id=article_id, slug=current_article.slug))

    return render_template("article.html", article=current_article)
