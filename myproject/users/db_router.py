from .middleware import RequestURL

class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users' and model._meta.model_name == 'User':
            return 'shard_a'  # Replace with your actual database aliases
        return None

    def db_for_write(self, model, **hints):
        url = RequestURL.get_current_url()
        if hints:
            if 'shard' in url:
                if hints.get('instance').id % 2 == 0:
                    return 'shard_a'  # Replace with your actual database aliases
                else:
                    return 'shard_b'
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'users' and model_name == 'User':
            return True
        return None
