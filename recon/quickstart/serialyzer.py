from rest_framework import serializers
from django import subdomain


class subdomain(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = subdomain
        fields = ['Target', 'Subdomain', 'IP', 'ASN', 'ISP', 'Organization', 'Country', 'Region', 'City', 'Latitude', 'Longuitude', 'TimeZone', 'User', 'date_found', 'last_seen']
