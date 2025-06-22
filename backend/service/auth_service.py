from service.user_service import add_user
from repository.auth_repository import get_user_by_email

def login(email, password):
    return get_user_by_email(email, password)

#TODO revisar si el register tiene que estar en el servicio de auth.
# Agregar las validaciones antes de agregar y eso.
def register(email, password, first_name, last_name):
    return add_user(email, password, first_name, last_name)