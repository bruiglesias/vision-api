from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView  # noqa
from application.views import ModelAPIView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', ModelAPIView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('api/predict', ModelAPIView.as_view(), name='model_predict'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # noqa
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # noqa
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
