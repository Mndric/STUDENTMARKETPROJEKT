from flask import render_template
from app.main import main_bp
from app.models import Ad


@main_bp.route('/')
def index():
    """Home page showing recent ads"""
    ads, total = Ad.get_all(page=1, per_page=6)
    return render_template('main/index.html', ads=ads, total=total)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('main/about.html')
