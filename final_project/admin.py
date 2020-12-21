from django.contrib import admin
from final_project.models import GroupSubjectTeacher, Exam, Mark, Subject, Group, User

# Регистрация моделей
admin.site.register(Group)
admin.site.register(User)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(Mark)
admin.site.register(GroupSubjectTeacher)
