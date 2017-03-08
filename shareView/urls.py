"""shareAnalysis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
from .views import ShareListView,SupervisionListView

app_name = 'shareView'
urlpatterns = [

    url(r'^$', ShareListView.as_view(), name='share-list'),
    url(r'^add$', views.addShare, name='share-add'),
    url(r'^delete$', views.deleteShare, name='share-del'),

    url(r'^supervision$', SupervisionListView.as_view(), name='share-supervision'),
    url(r'^supervision/update', views.updateSupervision, name='supervision-update'),

]
