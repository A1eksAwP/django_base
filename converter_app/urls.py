from django.urls import path, include

urlpatterns = [
    path('', include('converter_app.route.view_urls')),
    path('api/', include('converter_app.route.api_urls')),
]