import threading

_thread_locals = threading.local()

class RequestURL:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.url = request.path
        return self.get_response(request)

    @staticmethod
    def get_current_url():
        return getattr(_thread_locals, 'url', None)
