from django.contrib.auth.models import Group, User
from rest_framework import serializers

from .models import Machine, Ticket, TicketUpdate

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = ['code', 'name', 'description', 'status']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class TicketUpdateSerlializer(serializers.ModelSerializer):
    class Meta:
        model = TicketUpdate
        fields = 'update_text'