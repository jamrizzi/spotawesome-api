from api.exceptions.user_exceptions import UserNotFound, UserWithEmailExists
from api.exceptions.auth_exceptions import RoleInvalid
from api.models import User
from api.services.peewee_service import query_from_dict
from api.services.auth_service import get_authed_user_model
from playhouse.shortcuts import model_to_dict

def update(id, data):
    authed_user = get_authed_user_model()
    user = User.select().where(User.id == id).first()
    if not user:
        raise UserNotFound('id', id)
    if 'email' in data:
        user = User.select().where(User.email == data['email']).first()
        if user:
            raise UserWithEmailExists(data['email'])
    if 'role' in data:
        if authed_user.role != 'super_admin':
            raise RoleInvalid('super_admin')
    if 'password' in data:
        user.hash_password(data['password'])
        del data['password']
        user.save()
    user = User.update(**data).where(User.id == id)
    user.execute()
    user = User.select().where(User.id == id).first()
    user_dict = model_to_dict(user)
    del user_dict['password']
    return user_dict

def find_one(data):
    user = User.select().where(*query_from_dict(User, data)).first()
    if not user:
        raise UserNotFound(data.keys()[0], data[data.keys()[0]])
    user_dict = model_to_dict(user)
    del user_dict['password']
    return user_dict
