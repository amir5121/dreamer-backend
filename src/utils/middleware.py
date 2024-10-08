import traceback


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            print(request.user)

        if hasattr(request, "data"):
            print(request.data)
        path = request.get_full_path()  # Get the URL Path
        tb = traceback.format_exc()  # Get the traceback
        meta = request.headers  # Get request meta information
        print(path)
        print(tb)
        print(meta)
        response = self.get_response(request)
        if hasattr(response, "data"):
            print(response.data)
        return response
