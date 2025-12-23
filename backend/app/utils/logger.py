import time
from fastapi import Request


async def log_requests(request: Request, call_next):
    # 🔑 IMPORTANT: Let CORS preflight requests pass untouched
    if request.method == "OPTIONS":
        return await call_next(request)

    start = time.time()

    try:
        response = await call_next(request)
    except Exception as exc:
        # Optional: log error here if you want
        raise exc

    duration = round(time.time() - start, 3)
    trace_id = request.headers.get("x-trace-id", "internal")

    print(
        f"[{request.method}] {request.url.path} | "
        f"status={response.status_code} | "
        f"time={duration}s | "
        f"trace_id={trace_id}"
    )

    return response
