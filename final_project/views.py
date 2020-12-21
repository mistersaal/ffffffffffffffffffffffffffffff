from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Mark, Exam, GroupSubjectTeacher, Subject, Group

User = get_user_model()


@login_required
def main_page(request):
    """Определение на какую страницу надо перенаправить"""
    if request.user.is_superuser:
        return redirect('/rector/')
    elif request.user.is_teacher:
        return redirect('/teacher/')
    else:
        return redirect('/student/')


@login_required
def student_main_page(request):
    """Страница с информацией о студенте"""
    if not request.user.is_student:
        return redirect('/')
    exams = Exam.objects.filter(group=request.user.group)
    for exam in exams:
        try:
            mark = Mark.objects.get(student=request.user, exam=exam)
            exam.mark = mark.mark
        except Mark.DoesNotExist:
            exam.mark = '-'
    return render(request, 'student_main.html', {'exams': exams})


@login_required
def subject_page(request, id):
    """Информация о предмете"""
    exam = Exam.objects.get(pk=id)
    subject = exam.subject
    relation = GroupSubjectTeacher.objects.get(subject=subject, group=request.user.group)
    teacher = relation.teacher
    return render(request, 'subject.html', {'exam': exam, 'subject': subject, 'teacher': teacher})


@login_required
def teacher_main_page(request):
    """Главная страница преподавателя"""
    relations = GroupSubjectTeacher.objects.filter(teacher=request.user)
    exams = []
    for relation in relations:
        try:
            exams.append(Exam.objects.get(group=relation.group, subject=relation.subject))
        except Exam.DoesNotExist:
            exams
    return render(request, 'teacher_main.html', {'exams': exams})


@login_required
def exam_page(request, id):
    """Страница с экзаменом"""
    exam = Exam.objects.get(pk=id)
    subject = exam.subject
    group = exam.group
    students = User.objects.filter(group=group)
    for student in students:
        try:
            mark = Mark.objects.get(exam=exam, student=student)
        except Mark.DoesNotExist:
            mark = None
        id = 0
        if mark:
            id = mark.id
            mark = mark.mark
        else:
            mark = ''
        student.mark = mark
        student.mark_id = id
    return render(request, 'exam.html', {'exam': exam, 'subject': subject, 'group': group, 'students': students})


@login_required
def mark(request, id):
    """Редактирование отметки"""
    if request.method == 'POST':
        mark = Mark.objects.get(pk=id)
        mark.mark = request.POST['mark']
        mark.save()
        return redirect('/exams/' + str(mark.exam_id) + '/')


@login_required
def new_mark(request):
    """Создание отметки"""
    if request.method == 'POST':
        mark = Mark(student_id=request.POST['student'], exam_id=request.POST['exam'], mark=request.POST['mark'])
        mark.save()
        return redirect('/exams/' + str(mark.exam_id) + '/')


@login_required
def new_exam(request):
    """Создание экзамена"""
    if request.method == 'GET':
        relations = GroupSubjectTeacher.objects.filter(teacher=request.user)
        return render(request, 'new_exam.html', {'relations': relations})
    else:
        relation = request.POST['relation'].split('_')
        group_id = relation[0]
        subject_id = relation[1]
        exam = Exam(subject_id=subject_id, group_id=group_id, classroom=request.POST['classroom'],
                    datetime=request.POST['datetime'])
        exam.save()
        relations = GroupSubjectTeacher.objects.filter(teacher=request.user)
        return render(request, 'new_exam.html', {'relations': relations})


@login_required
def edit_exam(request, id):
    """Редактирование экзамена"""
    if request.method == 'GET':
        exam = Exam.objects.get(pk=id)
        relations = GroupSubjectTeacher.objects.filter(teacher=request.user)
        return render(request, 'edit_exam.html', {'relations': relations, 'exam': exam})
    else:
        relation = request.POST['relation'].split('_')
        group_id = relation[0]
        subject_id = relation[1]
        exam = Exam.objects.get(pk=id)
        exam.subject_id = subject_id
        exam.group_id = group_id
        exam.classroom = request.POST['classroom']
        exam.datetime = request.POST['datetime']
        exam.save()
        exam = Exam.objects.get(pk=id)
        relations = GroupSubjectTeacher.objects.filter(teacher=request.user)
        return render(request, 'edit_exam.html', {'relations': relations, 'exam': exam})


@login_required
def delete_exam(request, id):
    """Удаление экзамена"""
    if request.method == 'POST':
        exam = Exam.objects.get(pk=id)
        exam.delete()
        return redirect('/teacher/')


@login_required
def rector_main_page(request):
    """Главная страница ректора"""
    teachers = User.objects.filter(is_teacher=True)
    students = User.objects.filter(is_student=True)
    subjects = Subject.objects.all()
    groups = Group.objects.all()
    return render(request, 'rector_main_page.html',
                  {'teachers': teachers, 'students': students, 'subjects': subjects, 'groups': groups})


@login_required
def new_teacher(request):
    """Создание нового преподавателя"""
    if request.method == 'GET':
        return render(request, 'new_teacher.html')
    else:
        teacher = User.objects.create_user(
            request.POST['username'], request.POST['email'], request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            middle_name=request.POST['middle_name'],
            is_teacher=True
        )
        return render(request, 'new_teacher.html')


@login_required
def new_subject(request):
    """Создание нового предмета"""
    if request.method == 'GET':
        return render(request, 'new_subject.html')
    else:
        subject = Subject(
            name=request.POST['name'],
            code=request.POST['code'],
        )
        subject.save()
        return render(request, 'new_subject.html')


@login_required
def new_student(request):
    """Создание нового студента"""
    if request.method == 'GET':
        return render(request, 'new_student.html')
    else:
        student = User.objects.create_user(
            request.POST['username'], request.POST['email'], request.POST['password'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            middle_name=request.POST['middle_name'],
            is_student=True
        )
        return render(request, 'new_student.html')


@login_required
def new_group(request):
    """Создание новой группы"""
    if request.method == 'GET':
        return render(request, 'new_group.html')
    else:
        group = Group(
            name=request.POST['name'],
            course=request.POST['course'],
        )
        group.save()
        return render(request, 'new_group.html')


@login_required
def group(request, id):
    """Список студентов в группе"""
    group = Group.objects.get(pk=id)
    students = User.objects.filter(group=group)
    free_students = User.objects.filter(group=None, is_student=True)
    relations = GroupSubjectTeacher.objects.filter(group_id=id)
    subjects = Subject.objects.all()
    teachers = User.objects.filter(is_teacher=True)
    return render(request, 'group.html',
                  {'group': group, 'students': students, 'free_students': free_students, 'relations': relations,
                   'subjects': subjects, 'teachers': teachers})


@login_required
def add_student_to_group(request, group_id):
    """Добавить студента в группу"""
    student_id = request.POST['student']
    student = User.objects.get(pk=student_id)
    student.group_id = group_id
    student.save()
    return redirect('/groups/' + str(group_id) + '/')


@login_required
def delete_student_from_group(request, group_id):
    """Удалить студента из группы"""
    student_id = request.POST['student']
    student = User.objects.get(pk=student_id)
    student.group_id = None
    student.save()
    return redirect('/groups/' + str(group_id) + '/')


@login_required
def add_subject_to_group(request, group_id):
    """Добавить предмет в группу"""
    relation = GroupSubjectTeacher(subject_id=request.POST['subject'], group_id=group_id,
                                   teacher_id=request.POST['teacher'])
    relation.save()
    return redirect('/groups/' + str(group_id) + '/')


@login_required
def delete_subject_from_group(request, group_id):
    """Удалить предмет из группы"""
    relation = GroupSubjectTeacher.objects.get(subject_id=request.POST['subject'], group_id=group_id,
                                               teacher_id=request.POST['teacher'])
    relation.delete()
    return redirect('/groups/' + str(group_id) + '/')
