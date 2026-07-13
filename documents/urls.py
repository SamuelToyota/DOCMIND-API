from rest_framework.routers import DefaultRouter

from .views import DocumentViewSet,DocumentChunkViewSet

router = DefaultRouter()
router.register("documents", DocumentViewSet, basename="documents")


urlpatterns = router.urls
