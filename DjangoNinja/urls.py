from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from tasks.api import router as tasks_router
from commerce.api import router as com_router
from movies.api import router as movies_router
from blog.api import router as blogs_router
from monitoring.api import router as monitoring_router
from library.api import router as library_router
from education.api import router as education_router

api = NinjaAPI()

api.add_router("/tasks/", tasks_router)
api.add_router("/commerce/", com_router)
api.add_router("/movies/", movies_router)
api.add_router("/blog/", blogs_router)
api.add_router("/monitoring/", monitoring_router)
api.add_router("/library/", library_router)
api.add_router("/education/", education_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]

