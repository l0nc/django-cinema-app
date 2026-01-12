from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from apps.accounts.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователя"""
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password_confirm', 'email')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError(
                {"password": "Password fields didnt match"}
            )
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
    
class UserLoginSerializer(serializers.Serializer):
    """Сериализатор для входа пользователя по email/username"""
    login = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)   
    
    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        
        if login and password:
            user = authenticate(request=self.context.get('request'), username=login, password=password)
            
            if not user:
                raise serializers.ValidationError('Невереный логин или пароль')
            
            if not user.is_active:
                raise serializers.ValidationError('Аккаунт заблокирован')
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('Необходимо ввести логин или пароль')
        
        
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    ratings_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        
    def get_ratings_count(self, obj):
        try:
            return obj.ratings.count()
        except AttributeError:
            return 0
    
    def get_comments_count(self, obj):
        try:
            return obj.comments.count()
        except AttributeError:
            return 0
    
class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления профиля пользователя"""
    
    class Meta:
        model = User
        fields = ('avatar', 'bio')
        
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value) # Example (user, 'avatar', 'new_photo')
        instance.save()
        return instance
    
    
class ChangePasswordSerializer(serializers.Serializer):
    """Сериализатор для смены пароля"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Старый пароль некорректный.')
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError(
                {'new_password': 'Пароли не одинаковые'}
            )
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
            