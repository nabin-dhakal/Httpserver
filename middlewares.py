def logging_middlewares(request, next):
    print(f'[LOG] {request.method} {request.path}')
    response = next(request)
    print(f'[LOG] Response sent')
    return response