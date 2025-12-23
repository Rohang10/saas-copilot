import time
from fastapi import Request


async def log_requests(request: Request, call_next):
    start = time.time()

    response = await call_next(request)

    duration = round(time.time() - start, 3)
    trace_id = request.headers.get("x-trace-id", "internal")

    print(
        f"[{request.method}] {request.url.path} | "
        f"status={response.status_code} | "
        f"time={duration}s | "
        f"trace_id={trace_id}"
    )

    return response
