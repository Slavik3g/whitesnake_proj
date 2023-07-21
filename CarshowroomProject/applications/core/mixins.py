from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action


class SafeDeleteModelMixin:
    @action(methods=['delete'], detail=True)
    def safe_delete(self, request, pk=None):
        instance = self.queryset.get(pk=pk)
        instance.safe_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
