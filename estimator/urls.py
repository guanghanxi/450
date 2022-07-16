from django.urls import path, reverse_lazy
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('estimators/', views.EstimatorView.as_view(), name='estimators'),
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