from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .models import MyUser, Coord, Level, Images, Pereval
from .serializers import CoordSerializer, UserSerializer, LevelSerializer, ImagesSerializer, PerevalSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class CoordsViewSet(viewsets.ModelViewSet):
    queryset = Coord.objects.all()
    serializer_class = CoordSerializer


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImagesSerializer


class PerevalViewSet(viewsets.ModelViewSet):
    queryset = Pereval.objects.all()
    serializer_class = PerevalSerializer

    def create(self, request, *args, **kwargs):
        serializer = PerevalSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': None,
                'id': serializer.data,
            })
        if status.HTTP_400_BAD_REQUEST:
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': 'Bad Request',
                'id': None,
            })
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response({
                'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'message': 'Ошибка подключения к базе данных',
                'id': None,
            })

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != 'new':
            return Response({'state': '0', 'message': 'Можно редактировать только записи со статусом "new"'})

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'state': '1', 'message': 'Успешно удалось отредактировать запись в базе данных'})

    def get_queryset(self):
        queryset = Pereval.objects.all()
        user = self.request.query_params.get('user__email', None)
        if user is not None:
            queryset = queryset.filter(user__email=user)
        return queryset