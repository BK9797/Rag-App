# Celery configuration (optional - disabled for development without Redis)
# When Redis is available, uncomment and configure below

# from celery import Celery
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# celery_app = Celery(
#     "rag_system",
#     broker=os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0"),
#     backend=os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0"),
# )
#
# celery_app.conf.update(
#     task_serializer="json",
#     accept_content=["json"],
#     result_serializer="json",
#     timezone="UTC",
#     enable_utc=True,
# )

# Dummy celery_app for development mode (no Redis required)
class DummyCeleryApp:
    pass

celery_app = DummyCeleryApp()
