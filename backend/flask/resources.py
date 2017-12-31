#     __             _
#  __|  |_ _ ___ ___| |___
# |  |  | | |   | . | | -_|
# |_____|___|_|_|_  |_|___|
#              |___|
#
# App-Resources
# Last Revision: 12/20/16

import hashlib
from flask import jsonify, Blueprint, g, request
from flask_httpauth import HTTPBasicAuth
from flask_restful import Resource, reqparse
from app.api.models import User, Post, Media, \
    user_schema, post_schema, media_schema
from app import db


auth = HTTPBasicAuth()

api_blueprint = Blueprint('apiblueprint', __name__)


@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)
    if not user:
        user = User.query.filter_by(email=email_or_token).first()
        if not hasattr(user, 'password') or hashlib.sha224(password).hexdigest() not in user.password:
            return False
    g.user = user
    return True


class UserData(Resource):
    decorators = [auth.login_required]

    def get(self, user_id=None):
        if user_id is None:
            # Return a list of all the users
            usr = User.query.all()
        else:
            usr = User.query.filter_by(id=user_id).all()

        # If no data matches our query send a 404
        if len(usr) is 0:
            return jsonify({'response': None, 'status': 404})

        res = user_schema.dump(usr)
        if len(res.data) is 1:
            return jsonify({'response': res.data[0], 'status': 200})
        return jsonify({'response': res.data, 'status': 200})

    def post(self):
        data = request.get_json()

        if not data:
            return jsonify({'response': 'Missing POST request arguments for User',
                            'status': 400})
        if 'email' not in data:
            return jsonify({'response': 'Missing \'email\' argument in POST request',
                            'status': 422})
        elif 'password' not in data:
            return jsonify({'response': 'Missing \'password\' argument in POST request',
                            'status': 422})
        email, password, name, location = data['email'], data['password'], None, None

        # Check if we have a name or location
        if 'name' in data:
            name = data['name']
        if 'location' in data:
            location = data['location']

        # Now we check for a duplicate user-- Must be unique email!
        dup = User.query.filter_by(email=email).first()
        if not dup:
            new_user = User(email, hashlib.sha224(password).hexdigest(), name, location)
            try:
                db.session.add(new_user)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return jsonify({'response': str(e), 'status': 422})
            q = User.query.filter_by(email=email)

            # If we pass all the checks we're golden!
            return jsonify({'response': user_schema.dump(q).data[0], 'status': 200})
        else:
            return jsonify({'response': 'Duplicate User for email \'' + email + '\'', 'status': 422})

    def put(self, user_id=None):
        data = request.get_json()
        if not user_id:
            if 'email' not in data:
                # We need some form of identification-- either id or email!
                return jsonify({'response': 'Missing user_id/email argument for PUT \'User\'',
                                'status': 400})
            else:
                usr = User.query.filter_by(email=data['email'])
        else:
            usr = User.query.filter_by(id=user_id)

        for n in data.keys():
            setattr(usr, n, data[n])

        try:
            db.session.commit()
        except Exception as e:
            return jsonify({'response': str(e), 'status': 422})

        return jsonify({'response': user_schema.dump(usr).data[0], 'status': 200})


    def delete(self, user_id=None):
        if not user_id:
            return jsonify({'response': 'Missing user_id argument for DELETE \'User\'', 'status': 400})
        u = User.query.filter_by(id=user_id)
        try:
            db.session.delete(u)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'response': str(e), 'status': 422})
        # Return the User entry we just removed
        return jsonify({'response': user_schema.dump(u).data[0], 'status': 200})

class MediaData(Resource):
    decorators = [auth.login_required]

    def get(self, media_id=None):
        if media_id is None:
            md = Media.query.all()
        else:
            md = Media.query.filter_by(id=media_id).all()

        # If no data matches our query send a 404
        if len(md) is 0:
            return jsonify({'response': None, 'status': 404})

        res = media_schema.dump(md)

        if len(res.data) is 1:
            return jsonify({'response': res.data[0], 'status': 200})
        return jsonify({'response': res.data, 'status': 200})

    def post(self):
        data = request.get_json()

        if not data:
            return jsonify({'response': 'Missing POST request arguments for Media',
                            'status': 400})
        if 'post_id' not in data:
            return jsonify({'response': 'Missing \'post_id\' argument in POST request',
                            'status': 422})
        if 'user_id' not in data:
            return jsonify({'response': 'Missing \'user_id\' argument in POST request',
                            'status': 422})
        if 'path' not in data:
            return jsonify({'response': 'Missing \'path\' argument in POST request',
                            'status': 422})

        post_id, user_id, path = data['post_id'], data['user_id'], data['path']

        new_media = Media(post_id, user_id, path)
        try:
            db.session.add(new_media)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'response': str(e), 'status': 422})
        # TODO: find a way to retrieve a query from database immediately

        # If we pass all the checks we're golden!
        return jsonify({'response': {'post_id': post_id, 'user_id': user_id, 'path': path}, 'status': 200})

    def put(self, media_id=None):
        data = request.get_json()
        if not media_id:
            return jsonify({'response': 'Missing \'media_id\' query argument in PUT request',
                            'status': 422})
        med = Media.query.filter_by(id=media_id)
        if not med:
            return jsonify({'response': 'Media with id \'' + med.id + '\' not found', 'status': 404})

        # Go through each attribute and modify it
        for n in data.keys():
            setattr(med, n, data[n])

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'response': str(e), 'status': 422})

        # Return updated Media if successful
        return jsonify({'response': media_schema.dump(med).data[0], 'status': 200})

    def delete(self, media_id=None):
        if not media_id:
            return jsonify({'response': 'Missing \'media_id\' query argument in DELETE request',
                            'status': 400})
        med = Media.query.filter_by(id=media_id)
        try:
            db.session.delete(med)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'response': str(e), 'status': 422})
        # Return the Media entry we just removed
        return jsonify({'response': post_schema(med).dump[0], 'status': 200})

@api_blueprint.route('/api/testuser')
def adduser_api():
    usr = User('jrbartola@gmail.com', hashlib.sha224('pass123').hexdigest(), 'Jesse Bartola', 'Amherst')
    usr2 = User('johnny@gmail.com', hashlib.sha224('thisisabadpassword').hexdigest(), 'Johnny Depp', 'Slamherst')
    usr3 = User('jimmyjones@bones.com', hashlib.sha224('abcdefg').hexdigest(), 'JimmyJones III')
    usrs = [usr, usr2, usr3]
    for u in usrs:
        tried = db.session.query(User).filter_by(email=u.email).first()
        if not tried:
            try:
                db.session.add(u)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return 'Rollback because of ' + str(e)
    return 'Success!'


@api_blueprint.route('/api/testpost')
def addpost_api():
    p1 = Post(19, '''Hello all! I have finally guaranteed a housing appointment at...''')
    p2 = Post(19, '''Today a very tragic event occurred-- one that will plague us for eternity''')
    p3 = Post(21, '''Another post made by me myself and I''')
    ps = [p1, p2, p3]
    for p in ps:
        tried = db.session.query(Post).filter_by(id=p.id).first()
        if not tried:
            try:
                db.session.add(p)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return 'Rollback because of ' + str(e)
    return 'Success!'

@api_blueprint.route('/api/testmedia')
def addmedia_api():
    m1 = Media(4, 20, '/var/log/supervisor/test.txt')
    m2 = Media(5, 20, '/home/www/flaskapp/hi.jpeg')
    m3 = Media(6, 19, '/root/home/logging/profile.gif')
    marr = [m1, m2, m3]
    for m in marr:
        tried = db.session.query(Media).filter_by(id=m.id).first()
        if not tried:
            try:
                db.session.add(m)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                return 'Rollback because of ' + str(e)
    return 'Success!'