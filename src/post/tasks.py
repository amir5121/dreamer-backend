from dreamer.celery import app


@app.task
def health_check():
    print("OK")
