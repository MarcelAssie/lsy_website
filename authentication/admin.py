from django.contrib import admin
from .models import User, Student, Teacher, Parent

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_student', 'is_teacher', 'is_parent', 'is_staff')
    list_filter = ('is_student', 'is_teacher','is_parent', 'is_staff')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classe')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'matiere', 'display_classes')
    filter_horizontal = ('classes',)

    def display_classes(self, obj):
        return ", ".join([cls.get_name_display() for cls in obj.classes.all()])
    display_classes.short_description = 'Classes'

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('user',)
