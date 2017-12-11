from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .renderers import UserJSONRenderer
from .serializers import LoginSerializer, RegistrationSerializer, ContactsUserSerializer, ContactsSerializer, ContactsAttributesSerializer
from api.authentication.models import User, Contacts, ContactsAttributes

class RegistrationAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    # serializer_class = RegistrationSerializer


    def post(self, request, format=None):
        serializer_contacts = ContactsSerializer(data=request.data)
        registration_response = {}
        # Get the admin user for create_uid and update_uid
        # admin username is "admin"
        admin_user_id = User.objects.get(username="admin")
        # Serialize data for contacts table
        if serializer_contacts.is_valid():
            contact_id = serializer_contacts.save(created_uid=admin_user_id, updated_uid=admin_user_id)
            serializer_user = RegistrationSerializer(data=request.data)
            # Serialize data for user table
            if serializer_user.is_valid():
                serializer_user.save(contact_id=contact_id,created_uid=admin_user_id, updated_uid=admin_user_id)
            # Save data for contacts attributes table
            contacts_attributes_data = {
                    'contacts_attribute':[
                        {'contact_id': contact_id, 'attribute_key': 'wear_glass', 'attribute_value': False, 'created_uid': admin_user_id, 'updated_uid': admin_user_id },
                        {'contact_id': contact_id, 'attribute_key': 'last_eye_checkup_date', 'attribute_value': '', 'created_uid': admin_user_id, 'updated_uid': admin_user_id },
                        {'contact_id': contact_id, 'attribute_key': 'regular_dental_checkup', 'attribute_value': False, 'created_uid': admin_user_id, 'updated_uid': admin_user_id },
                        {'contact_id': contact_id, 'attribute_key': 'last_dental_checkup_date', 'attribute_value': '', 'created_uid': admin_user_id, 'updated_uid': admin_user_id },
                        {'contact_id': contact_id, 'attribute_key': 'is_drug_use', 'attribute_value': False, 'created_uid': admin_user_id, 'updated_uid': admin_user_id },
                        {'contact_id': contact_id, 'attribute_key': 'is_smoke', 'attribute_value': False, 'created_uid': admin_user_id, 'updated_uid': admin_user_id },
                        {'contact_id': contact_id, 'attribute_key': 'is_alcoholic', 'attribute_value': False, 'created_uid': admin_user_id, 'updated_uid': admin_user_id },
                    ]
                }
            for data in contacts_attributes_data['contacts_attribute']:
                serializer_contacts_attributes = ContactsAttributesSerializer(data=data)
                serializer_contacts_attributes.create(data)
            # Get all contacts attribute
            serializer_contacts_attribute = ContactsAttributesSerializer(
                    ContactsAttributes.objects.filter(contact_id=contact_id), many=True)

            registration_response['contacts'] = serializer_contacts.data
            if registration_response['contacts']['profile_photo'] is None:
                registration_response['contacts']['profile_photo'] =""
            registration_response['token'] = serializer_user.data['token']
            registration_response['users'] = serializer_user.data
            del registration_response['users']['password']
            del registration_response['users']['token']
            registration_response['status'] = status.HTTP_201_CREATED
            registration_response['success'] = True
            registration_response['contacts_attribute'] = serializer_contacts_attribute.data
            return Response(registration_response, status.HTTP_201_CREATED)

        # If Phone number or Email address already exists then following message given
        if serializer_contacts.errors.get('username', False):
            registration_response['message'] = "This Phone Number Alreday Exists"
        elif serializer_contacts.errors.get('email', False):
            registration_response['message'] = "This Email Address Already Exists"
        else:
            registration_response['message'] = serializer_contacts.errors
        registration_response['status'] = status.HTTP_400_BAD_REQUEST
        registration_response['success'] = False
        return Response(registration_response, status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    # serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't actually have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        registration_response = {}
        if serializer.is_valid():
            registration_response['success'] = True
            registration_response['status'] = status.HTTP_200_OK

            # Get all the necessary data as response
            user_id = User.objects.get(username=serializer.data['username'])
            serializer_user = ContactsUserSerializer(User.objects.filter(pk=user_id.id), many=True)
            serializer_contacts = ContactsSerializer(Contacts.objects.filter(pk=user_id.contact_id.id), many=True)
            serializer_contacts_attribute = ContactsAttributesSerializer(ContactsAttributes.objects.filter(contact_id=user_id.contact_id), many=True)

            registration_response['contacts'] = serializer_contacts.data[0]
            if registration_response['contacts']['profile_photo'] is None:
                registration_response['contacts']['profile_photo'] = ""
            registration_response['users'] = serializer_user.data[0]
            del registration_response['users']['password']
            # registration_response['users']['token'] = serializer.data['token']
            registration_response['contacts_attribute'] = serializer_contacts_attribute.data
            registration_response['token'] = serializer.data['token']
            return Response(registration_response, status=status.HTTP_200_OK)

        # If Phone number and Password is incorrect then following message given
        if serializer.errors.get('non_field_errors', False):
            registration_response['message'] = "Phone Number and Password is Incorrect"
        else:
            registration_response['message'] = serializer.errors
        registration_response['status'] = status.HTTP_401_UNAUTHORIZED
        registration_response['success'] = False
        return Response(registration_response, status=status.HTTP_401_UNAUTHORIZED)

    # def post(self, request):
    #     user = request.data.get('user', {})
    #
    #     # Notice here that we do not call `serializer.save()` like we did for
    #     # the registration endpoint. This is because we don't actually have
    #     # anything to save. Instead, the `validate` method on our serializer
    #     # handles everything we need.
    #     serializer = self.serializer_class(data=user)
    #     serializer.is_valid(raise_exception=True)
    #
    #     return Response(serializer.data, status=status.HTTP_200_OK)

class CustomUserAPIView(APIView):
    # Allow any user (authenticated or not) to hit this endpoint.
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    # serializer_class = RegistrationSerializer

    def post(self, request, format=None):
        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = ContactsUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes = (IsAuthenticated,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = UserSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         # There is nothing to validate or save here. Instead, we just want the
#         # serializer to handle turning our `User` object into something that
#         # can be JSONified and sent to the client.
#         serializer = self.serializer_class(request.user)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def update(self, request, *args, **kwargs):
#         user_data = request.data.get('user', {})
#
#         serializer_data = {
#             'username': user_data.get('username', request.user.username),
#             'email': user_data.get('email', request.user.email),
#
#             'profile': {
#                 'bio': user_data.get('bio', request.user.profile.bio),
#                 'image': user_data.get('image', request.user.profile.image)
#             }
#         }
#
#         # Here is that serialize, validate, save pattern we talked about
#         # before.
#         serializer = self.serializer_class(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
