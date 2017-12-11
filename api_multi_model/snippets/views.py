from django.shortcuts import render
from snippets.models import Contact, ContactUser, Attendee
from snippets.serializers import ContactSerializerModel, ContactUserSerializerModel, AttendeeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ContactList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = Contact.objects.all()
        serializer = ContactSerializerModel(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactSerializerModel(data=request.data)
        if serializer.is_valid():
            contact_id = serializer.save()
            # request.data['contact_id'] = serializer._creation_counter
            serializer_user = ContactUserSerializerModel(data=request.data)
            if serializer_user.is_valid():
                serializer_user.save(contact_id=contact_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactUserList(APIView):
    """
    List all snippets, or create a new snippet.
    """

    def get(self, request, format=None):
        snippets = ContactUser.objects.all()
        serializer = ContactUserSerializerModel(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ContactUserSerializerModel(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttendeeView(APIView):
    """
        List all snippets, or create a new snippet.
        """

    def get(self, request, format=None):
        snippets = Attendee.objects.all()
        serializer = AttendeeSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AttendeeSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AttendeeViewDetail(APIView):
    serializer_class = AttendeeSerializer
    """
    Retrieve, update or delete a snippet instance.
    """

    # def get_object(self, pk):
    #     try:
    #         return Attendee.objects.get(pk=pk)
    #     except Attendee.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = AttendeeSerializer(snippet)
    #     return Response(serializer.data)

    def put(self, request, contact_id, format=None):
        snippet = Attendee.objects.filter(contact_id=contact_id)
        serializer = AttendeeSerializer(instance=snippet, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     snippet.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def put(self, request):
    #     instances =  Attendee.objects.all()
    #     serializer = AttendeeSerializer(data=request.data, instance=instances, many=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)