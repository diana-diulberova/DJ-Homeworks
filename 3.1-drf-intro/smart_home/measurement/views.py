# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView

from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer, FullSensorSerializer
from rest_framework.response import Response
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class SensorView(ListAPIView):

    '''Возвращает данные на все датчики. Метод GET'''

    queryset = Sensor.objects.all() #список объектов
    serializer_class = SensorSerializer #с помощью чего этот набор надо превратить в json

    def post(self, request):

        '''Создание датчика. Метод POST'''

        title = request.data.get('title')
        description = request.data.get('description')
        Sensor(title=title, description=description).save()
        return Response({'status': 'Датчик добавлен'})


class MeasurementView(ListAPIView):

    '''Показывает все измерения для счетчиков. Метод GET'''

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request):

        '''Добавление измерения для счетчика. Метод POST'''

        sensor = Sensor.objects.get(id=request.data.get('sensor'))
        temperature = request.data.get('temperature')
        if request.data.get('image_model'):
            image_model = request.data.get('image_model')
            Measurement(sensor=sensor, temperature=temperature, image_model=image_model).save()
        else:
            Measurement(sensor=sensor, temperature=temperature).save()
        return Response({'status': 'Измерения добавлены'})


class UpgradeSensorView(RetrieveAPIView): # если надо получить данные по одному объекту

    '''Возвращает данные датчика по его pk номеру. Метод GET'''

    queryset = Sensor.objects.all()
    serializer_class = FullSensorSerializer

    def patch(self, request, pk):

        '''Обновляет данные датчика по его pk номеру. Метод PATCH'''

        object = Sensor.objects.get(id=pk) # 1-й вариант (обновляет все поля, даже не измененные)
        if request.data.get('title'):
            object.title = request.data.get('title')
        if request.data.get('description'):
            object.description = request.data.get('description')
        object.save()
        # Sensor.objects.filter(id=pk).update(description=description) # 2-й вариант (обновление указанного поля)
        return Response({'status': 'Датчик обновлен'})


def start_api_view(request):

    '''Показывает список команд '''

    list_commands = [
        {'title': 'Sensors', 'description': 'GET - получить список датчиков. POST - добавляет новый датчик'},
        {'title': 'Measurements', 'description': 'Список всех измерений'},
        {'title': 'Sensors/<pk>/', 'description': 'GET - показывает данные датчика по его номеру. PATCH - обновление описания датчика'},
    ]
    context = {'pages': list_commands}
    return render(request, 'api.html', context)

from django.http import HttpResponse
def images(request):
    data = Measurement.objects.get(id=1, image_model='image_model')
    return HttpResponse(data)
