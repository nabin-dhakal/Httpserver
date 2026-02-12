def home_handlers(request):
    return "Welcome to Homepage"

def about_handlers(request):
    return "This is about page"

def user_handlers(request):
    return "User list:Alice, Bob, Charlie"

routes = {
    "/": home_handlers,
    "/about":about_handlers,
    "/api/users":user_handlers
}