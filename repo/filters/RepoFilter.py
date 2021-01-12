from django_filters import rest_framework as filters

from repo.models import RepoIn, SendOut


class RepoInFilter(filters.FilterSet):

    class Meta:                                                                                   
        model = RepoIn
        fields = ['shop_num']


class SendOutFilter(filters.FilterSet):
    
    class Meta:
        model = SendOut
        fields = ['name', 'status']
