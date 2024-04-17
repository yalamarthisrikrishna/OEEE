# oee_app/urls.py

from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('oee/', views.oee_data_all, name='oee_data_all'),
    path('oee/<int:machine_id>/', views.oee_data_by_machine, name='oee_data_by_machine'),
    path('oee/filter/', csrf_exempt(views.filter_oee_data), name='filter_oee_data'),
    path('', views.main, name='main'),
    path('machineview/machines/', csrf_exempt(views.add_machine), name='add_machine'),
    path('machineview/',views.machine_view, name='machine_view'),
    path('logsview/',views.logs_view, name='logs_view'),
    path('logsview/add_log/',csrf_exempt(views.add_log), name='add_log')
]
