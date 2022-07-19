from django.urls import path, reverse_lazy
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('estimators/', views.EstimatorView.as_view(), name='estimators'),
    path('materials/', views.MaterialListView.as_view(), name='materials'),
    path('trans/', views.TransportationListView.as_view(), name='transportation'),
    path('energy/', views.EnergyListView.as_view(), name='energy'),
    path('machine/', views.MachineListView.as_view(), name='machine'),
    path('machine/<int:pk>', views.MachineDetailView.as_view(), name='machine_detail'),
]

import os
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {
        'document_root': os.path.join(BASE_DIR, 'estimator/static'),
    }),
]