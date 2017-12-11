from rest_framework import serializers
from django.contrib.auth.models import User
from snippets.models import Contact, ContactUser, Attendee

# class UserSerializer(serializers.ModelSerializer):
#     snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
#
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'snippets')
#
#
# class SnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     linenos = serializers.BooleanField(required=False)
#     language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
#     style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
#     owner = serializers.ReadOnlyField(source='owner.username')
#
#     class Meta:
#         model = Snippet
#         fields = ('id', 'highlight', 'owner',
#                   'title', 'code', 'linenos', 'language', 'style')
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Snippet.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.code = validated_data.get('code', instance.code)
#         instance.linenos = validated_data.get('linenos', instance.linenos)
#         instance.language = validated_data.get('language', instance.language)
#         instance.style = validated_data.get('style', instance.style)
#         instance.save()
#         return instance
#


class ContactUserSerializerModel(serializers.ModelSerializer):
    contact_id = serializers.ReadOnlyField(source='contact_id.id')
    class Meta:
        model = ContactUser
        fields = ('username', 'password','contact_id')

class ContactSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'status')


class AttendeeListSerializer(serializers.ListSerializer):
   # def create(self,validated_data):
   def update(self, instance, validated_data):
       # return self.update(validated_data, **instance)
       # Maps for id->instance and id->data item.
       book_mapping = {book.id: book for book in instance}
       data_mapping = {item['id']: item for item in validated_data}

       # # Perform creations and updates.
       ret = []
       # for contact_id, data in data_mapping.items():
       #     book = book_mapping.get(contact_id, None)
       #     if book is None:
       #         ret.append(self.child.create(data))
       #     else:
       #         ret.append(self.child.update(book, data))
       #
       # # Perform deletions.
       # for book_id, book in book_mapping.items():
       #     if book_id not in data_mapping:
       #         book.delete()

       return ret

   # def delete(self,instance):
class AttendeeSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField()
    class Meta:
      model = Attendee
      list_serializer_class= AttendeeListSerializer
      fields = ('id','name', 'school','contact_id','attribute_key','attribute_value',)

   # def create(self,validated_data):
   # def update(self,instance,validated_data):
   # def delete(self,instance):