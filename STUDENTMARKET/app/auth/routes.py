from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.auth import auth_bp
from app.auth.forms import RegistrationForm, LoginForm, ProfileForm
from app.models import User
from app import mail
from flask_mail import Message

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Create new user
        user = User(
            name=form.name.data,
            email=form.email.data.lower(),
            password_hash='',
            dob=form.dob.data,
            description=form.description.data
        )
        user.set_password(form.password.data)
        user.save()
        
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data.lower())
        
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            
            # Redirect to next page or home
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """View and edit user profile"""
    form = ProfileForm(obj=current_user)
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.dob = form.dob.data
        current_user.description = form.description.data
        current_user.save()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/profile.html', form=form, user=current_user)
@auth_bp.route("/verify/<token>")
def verify_email(token):
    error = User.verify_email(token)
    if error:
        flash(error, "danger")
        return redirect(url_for("auth.login"))

    flash("Your email has been verified!", "success")
    return redirect(url_for("auth.login"))

def send_verification_email(user):
    token = user.generate_verification_token()
    verify_url = url_for("auth.verify_email", token = token, _external = True)

    msg = Message(
        subject = "Verify your Email - FamilyRecipes",
        recipients = [user.email],
        body = (
            f"Hi {user.name}, \n\n"
            f"Please click the link below to verify your email:\n"
            f"{verify_url}\n\n"
            f"This link will expire in 1 hour!"
        ),
    )
    mail.send(msg)
    
