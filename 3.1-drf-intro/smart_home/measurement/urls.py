from django.urls import path
from .views import SensorView, MeasurementView, start_api_view, UpgradeSensorView

urlpatterns = [
    # TODO: зарегистрируйте необходимые маршруты
    path('', start_api_view),
    path('sensors/', SensorView.as_view()), #метод as_view превращает класс в views функцию
    path('measurements/', MeasurementView.as_view()),
    path('sensors/<pk>/', UpgradeSensorView.as_view()),
]
