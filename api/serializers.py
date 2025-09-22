from django.contrib.auth import get_user_model
from tutorials.models import Category, Comment, Post
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'bio', 'avatar')

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirmation', 'bio')

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')
        
        if password != password_confirmation:
            raise serializers.ValidationError("Passwords do not match.")
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        
        password = validated_data.pop('password')
        
        user = User.objects.create(**validated_data)
        
        user.set_password(password)
        
        user.save()
        
        return user
    def check_password(password, password_confirmation):
        if password == password_confirmation:
            return 
        


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'updated_at', 'author_name')
        read_only_fields = ('created_at', 'updated_at')

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    category_names = serializers.SlugRelatedField(
         source='categories',
         many=True,
         read_only=True,
         slug_field='name'
     )

    def create(self, validated_data):
        author = self.context.get('author')
        # 1. Remove categories from validated_data before creating post
        categories_data = validated_data.pop('categories', [])
        
        # 2. Create the post without categories
        post = Post.objects.create(author=author, **validated_data)
        
        # 3. Now set the categories using .set()
        post.categories.set(categories_data)
        
        return post
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 
                 'author', 'author_name', 'categories', 'category_names', 'comments') 
        read_only_fields = ('created_at', 'updated_at', 'author_name', 'author', 'comments')

