import time

def logging_middleware(request, next):
    print(f'[LOG] {request.method} {request.path}')
    response = next(request)
    print(f'[LOG] Response sent')
    return response

def timing_middleware(request, next):
    start_time = time.time()
    response = next(request)
    duration= time.time()-start_time
    print(f'[TIMING] Request took {duration:.4f} seconds')
    return response