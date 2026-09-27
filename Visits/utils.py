from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist

def get_model_instance(app_name, model_name, table_id):
    try:
        if not table_id or not str(table_id).isdigit():
            return None
        ModelClass = apps.get_model(app_name, model_name)
        if ModelClass is None:
            return None
        
        return ModelClass.objects.get(id=int(table_id))

    except ObjectDoesNotExist:
        return None




def get_model_class(app_name, model_name):
    try:
        ModelClass = apps.get_model(app_name, model_name)
        if ModelClass is None:
            return None
        return ModelClass
    except LookupError:
        return None