from rest_framework.permissions import BasePermission 


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешаем получение всем
        if request.method == 'GET':
            return True
        # Для остальных методов проверяем, что пользователь — автор
        return request.user == obj.creator
