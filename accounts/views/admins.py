from ..decorators import must_be_type_of
from ..forms import AdminSignUpForm
from django.contrib.auth import login
from ..models import User, Role
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class AdminSignUpView(CreateView):
    model = User
    form_class = AdminSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'admin'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        if request.session.is_empty():
            print('session is empty')
        login(self.request, user)
        return redirect('quiz_list')
        # return HttpResponse('form created and validated.')


@method_decorator([login_required, must_be_type_of(Role.ADMIN)], name='dispatch')
class QuizListView(ListView):
    model = User
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'accounts/admins/admin.html'

    def get_queryset(self):
        user = self.request.user
        users = User.objects.all()
        # student_interests = student.interests.values_list('pk', flat=True)
        # taken_quizzes = student.quizzes.values_list('pk', flat=True)
        # queryset = Quiz.objects.filter(subject__in=student_interests) \
        #     .exclude(pk__in=taken_quizzes) \
        #     .annotate(questions_count=Count('questions')) \
        #     .filter(questions_count__gt=0)
        # return queryset
        return users