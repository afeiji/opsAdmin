#encoding:utf-8


from rest_framework.routers import DefaultRouter
from .views import PublishViewSet, BookViewSet, AuthorViewSet

router = DefaultRouter()
router.register('publish',PublishViewSet,base_name="publish")
router.register('book',BookViewSet,base_name="book")
router.register('author',AuthorViewSet,base_name="author")