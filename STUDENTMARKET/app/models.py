from app import mongo
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from datetime import datetime
import markdown
import bleach


class User(UserMixin):
    """User model with all required fields"""
    
    def __init__(self, name, email, password_hash, is_email_verified=False, 
                 is_admin=False, dob=None, description='', _id=None):
        self.id = str(_id) if _id else None
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.is_email_verified = is_email_verified
        self.is_admin = is_admin
        self.dob = dob  # Date of birth
        self.description = description
        self.created_at = datetime.utcnow()
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary for MongoDB"""
        return {
            'name': self.name,
            'email': self.email,
            'password_hash': self.password_hash,
            'is_email_verified': self.is_email_verified,
            'is_admin': self.is_admin,
            'dob': self.dob,
            'description': self.description,
            'created_at': self.created_at
        }
    
    def save(self):
        """Save user to database"""
        data = self.to_dict()
        if self.id:
            mongo.db.users.update_one({'_id': ObjectId(self.id)}, {'$set': data})
        else:
            res = mongo.db.users.insert_one(data)
            self.id = str(res.inserted_id)
        return self.id
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        try:
            data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
            if data:
                return User(
                    name=data['name'],
                    email=data['email'],
                    password_hash=data['password_hash'],
                    is_email_verified=data.get('is_email_verified', False),
                    is_admin=data.get('is_admin', False),
                    dob=data.get('dob'),
                    description=data.get('description', ''),
                    _id=data['_id']
                )
        except Exception:
            return None
        return None
    
    @staticmethod
    def get_by_email(email):
        """Get user by email"""
        data = mongo.db.users.find_one({'email': email})
        if data:
            return User(
                name=data['name'],
                email=data['email'],
                password_hash=data['password_hash'],
                is_email_verified=data.get('is_email_verified', False),
                is_admin=data.get('is_admin', False),
                dob=data.get('dob'),
                description=data.get('description', ''),
                _id=data['_id']
            )
        return None
    
    @staticmethod
    def get_all():
        """Get all users"""
        users = []
        for data in mongo.db.users.find():
            users.append(User(
                name=data['name'],
                email=data['email'],
                password_hash=data['password_hash'],
                is_email_verified=data.get('is_email_verified', False),
                is_admin=data.get('is_admin', False),
                dob=data.get('dob'),
                description=data.get('description', ''),
                _id=data['_id']
            ))
        return users
    
    @staticmethod
    def create_admin(name, email, password):
        """Create an admin user"""
        admin = User(
            name=name,
            email=email,
            password_hash='',
            is_admin=True,
            is_email_verified=True
        )
        admin.set_password(password)
        return admin.save()
    
    def delete(self):
        """Delete user and all their ads"""
        if not self.id:
            return False
        
        # Delete all ads created by this user
        for ad_data in mongo.db.ads.find({'created_by': self.id}):
            ad = Ad.from_dict(ad_data)
            ad.delete()
        
        mongo.db.users.delete_one({'_id': ObjectId(self.id)})
        return True


class Ad:
    """Ad model with all required fields"""
    
    # Category choices
    CATEGORIES = [
        ('books', 'Books'),
        ('electronics', 'Electronics'),
        ('scripts', 'Scripts'),
        ('clothes', 'Clothes'),
        ('furniture', 'Furniture'),
        ('sports', 'Sports & Outdoors'),
        ('other', 'Other')
    ]
    
    def __init__(self, title, description, category, created_by,
                 description_html='', _id=None, created_at=None):
        self.id = str(_id) if _id else None
        self.title = title
        self.description = description
        self.description_html = description_html or self._markdown_to_html(description)
        self.category = category
        self.created_by = created_by  # User ID
        self.created_at = created_at or datetime.utcnow()
    
    @staticmethod
    def _markdown_to_html(markdown_text):
        """Convert markdown to sanitized HTML"""
        if not markdown_text:
            return ''
        
        # Convert markdown to HTML
        html = markdown.markdown(markdown_text, extensions=['nl2br', 'fenced_code'])
        
        # Sanitize HTML to prevent XSS
        allowed_tags = [
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'a', 'blockquote', 'code', 'pre', 'hr', 'table',
            'thead', 'tbody', 'tr', 'th', 'td'
        ]
        allowed_attributes = {
            'a': ['href', 'title'],
            'code': ['class']
        }
        
        return bleach.clean(html, tags=allowed_tags, attributes=allowed_attributes)
    
    def to_dict(self):
        """Convert ad to dictionary for MongoDB"""
        return {
            'title': self.title,
            'description': self.description,
            'description_html': self.description_html,
            'category': self.category,
            'created_by': self.created_by,
            'created_at': self.created_at
        }
    
    def save(self):
        """Save ad to database"""
        # Regenerate HTML from markdown
        self.description_html = self._markdown_to_html(self.description)
        
        data = self.to_dict()
        if self.id:
            mongo.db.ads.update_one({'_id': ObjectId(self.id)}, {'$set': data})
        else:
            res = mongo.db.ads.insert_one(data)
            self.id = str(res.inserted_id)
        return self.id
    
    @staticmethod
    def from_dict(ad_data):
        """Create Ad instance from dictionary"""
        return Ad(
            title=ad_data.get('title'),
            description=ad_data.get('description'),
            category=ad_data.get('category'),
            created_by=ad_data.get('created_by'),
            description_html=ad_data.get('description_html', ''),
            _id=ad_data.get('_id'),
            created_at=ad_data.get('created_at')
        )
    
    @staticmethod
    def get_by_id(ad_id):
        """Get ad by ID"""
        try:
            data = mongo.db.ads.find_one({'_id': ObjectId(ad_id)})
            if data:
                return Ad.from_dict(data)
        except Exception:
            return None
        return None
    
    @staticmethod
    def get_all(category=None, search=None, page=1, per_page=12):
        """Get all ads with optional filtering and pagination"""
        query = {}
        
        if category and category != 'all':
            query['category'] = category
        
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        total = mongo.db.ads.count_documents(query)
        cursor = mongo.db.ads.find(query).sort('created_at', -1).skip((page - 1) * per_page).limit(per_page)
        ads = [Ad.from_dict(a) for a in cursor]
        
        return ads, total
    
    @staticmethod
    def get_by_user(user_id, category=None, search=None, page=1, per_page=12):
        """Get all ads by a specific user"""
        query = {'created_by': user_id}
        
        if category and category != 'all':
            query['category'] = category
        
        if search:
            query['$or'] = [
                {'title': {'$regex': search, '$options': 'i'}},
                {'description': {'$regex': search, '$options': 'i'}}
            ]
        
        total = mongo.db.ads.count_documents(query)
        cursor = mongo.db.ads.find(query).sort('created_at', -1).skip((page - 1) * per_page).limit(per_page)
        ads = [Ad.from_dict(a) for a in cursor]
        
        return ads, total
    
    def delete(self):
        """Delete ad"""
        if not self.id:
            return False
        
        mongo.db.ads.delete_one({'_id': ObjectId(self.id)})
        return True
    
    def get_creator(self):
        """Get the user who created this ad"""
        return User.get_by_id(self.created_by)
