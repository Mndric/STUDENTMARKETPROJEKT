from flask import render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from app.ads import ads_bp
from app.ads.forms import AdForm
from app.models import Ad, User


@ads_bp.route('/')
def list_ads():
    """List all ads with filtering and pagination"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    per_page = current_app.config.get('ITEMS_PER_PAGE', 12)
    
    ads, total = Ad.get_all(category=category, search=search, page=page, per_page=per_page)
    
    # Calculate pagination
    total_pages = (total + per_page - 1) // per_page
    
    return render_template(
        'ads/list.html',
        ads=ads,
        total=total,
        page=page,
        total_pages=total_pages,
        category=category,
        search=search,
        categories=Ad.CATEGORIES
    )


@ads_bp.route('/<ad_id>')
def view_ad(ad_id):
    """View single ad"""
    ad = Ad.get_by_id(ad_id)
    if not ad:
        abort(404)
    
    creator = ad.get_creator()
    return render_template('ads/view.html', ad=ad, creator=creator)


@ads_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_ad():
    """Create new ad"""
    form = AdForm()
    
    if form.validate_on_submit():
        ad = Ad(
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            created_by=current_user.id
        )
        ad.save()
        
        flash('Ad created successfully!', 'success')
        return redirect(url_for('ads.view_ad', ad_id=ad.id))
    
    return render_template('ads/create.html', form=form)


@ads_bp.route('/<ad_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_ad(ad_id):
    """Edit existing ad"""
    ad = Ad.get_by_id(ad_id)
    if not ad:
        abort(404)
    
    # Check if user owns the ad or is admin
    if ad.created_by != current_user.id and not current_user.is_admin:
        abort(403)
    
    form = AdForm(obj=ad)
    
    if form.validate_on_submit():
        ad.title = form.title.data
        ad.description = form.description.data
        ad.category = form.category.data
        ad.save()
        
        flash('Ad updated successfully!', 'success')
        return redirect(url_for('ads.view_ad', ad_id=ad.id))
    
    return render_template('ads/edit.html', form=form, ad=ad)


@ads_bp.route('/<ad_id>/delete', methods=['POST'])
@login_required
def delete_ad(ad_id):
    """Delete ad"""
    ad = Ad.get_by_id(ad_id)
    if not ad:
        abort(404)
    
    # Check if user owns the ad or is admin
    if ad.created_by != current_user.id and not current_user.is_admin:
        abort(403)
    
    ad.delete()
    flash('Ad deleted successfully!', 'success')
    return redirect(url_for('ads.my_ads'))


@ads_bp.route('/my-ads')
@login_required
def my_ads():
    """List current user's ads"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', None)
    per_page = current_app.config.get('ITEMS_PER_PAGE', 12)
    
    ads, total = Ad.get_by_user(
        current_user.id,
        category=category,
        search=search,
        page=page,
        per_page=per_page
    )
    
    # Calculate pagination
    total_pages = (total + per_page - 1) // per_page
    
    return render_template(
        'ads/my_ads.html',
        ads=ads,
        total=total,
        page=page,
        total_pages=total_pages,
        category=category,
        search=search,
        categories=Ad.CATEGORIES
    )
