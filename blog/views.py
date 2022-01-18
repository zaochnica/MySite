from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.core.signing import BadSignature
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from blog.forms import ChangeUserInfoForm, RegisterUserForm
    # TrainingForm, AIFormSet
from blog.models import Training, User
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.shortcuts import get_object_or_404
from .utils import signer


def index(request):
    trs = Training.objects.all()
    context = {'trs': trs}
    return render(request, 'blog/index.html', context)


def by_format(request, format_id):
    tr = Training.objects.filter(format=format_id)
    context = {'tr': tr}
    return render(request, 'blog/by_format.html', context)


class UserLoginView(LoginView):
    template_name = 'blog/login.html'


@login_required
def profile(request):
    return render(request, 'blog/profile.html')


class UserLogoutView(LoginRequiredMixin, LogoutView):
    template_name = 'blog/logout.html'


class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'blog/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('blog:profile')
    success_message = 'Данные пользователя изменены'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'blog/password_change.html'
    success_url = reverse_lazy('blog:profile')
    success_message = 'Пароль пользователя изменен'


class RegisterUserView(CreateView):
    model = User
    template_name = 'blog/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('blog:register_done')


class RegisterDoneView(TemplateView):
    template_name = 'blog/register_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'blog/bad_signature.html')
    user = get_object_or_404(User, username=username)
    if user.is_activated:
        template = 'blog/user_is_activated.html'
    else:
        template = 'blog/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)


class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'blog/delete_user.html'
    success_url = reverse_lazy('blog:index')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id = None

    def setup(self, request, *args, **kwargs):
        return super().setup(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь удален')
        return super().post(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordResetView(PasswordResetView):
    template_name = 'blog/password_reset.html'
    subject_template_name = 'email/reset_letter_subject.txt'
    email_template_name = 'email/reset_letter_body.txt'
    success_url = reverse_lazy('blog:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'blog/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'blog/password_confirm.html'
    success_url = reverse_lazy('blog:password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'blog/password_complete.html'


# @login_required
# def profile_training_change(request, pk):
#     tr = get_object_or_404(Training, pk=pk)
#     if request.method == 'POST':
#         form = TrainingForm(request.POST, request.FILES, instance=bb)
#         if form.is_valid():
#             tr = form.save()
#             formset = AIFormSet(request.POST, request.FILES, instance=tr)
#             if formset.is_valid():
#                 formset.save()
#                 messages.add_message(request, messages.SUCCESS, 'Тренировка исправлена')
#                 return redirect('blog:profile')
#     else:
#         form = TrainingForm(instance=tr)
#         formset = AIFormSet(instance=tr)
#     context = {'form': form, 'formset': formset}
#     return render(request, 'blog/profile_tr_change.html', context)


@login_required
def profile_training_delete(request, pk):
    tr = get_object_or_404(Training, pk=pk)
    if request.method == 'POST':
        tr.delete()
        messages.add_message(request, messages.SUCCESS, 'Тренировка удалена')
        return redirect('blog:profile')
    else:
        context = {'tr': tr}
        return render(request, 'blog/profile_tr_delete.html', context)


# @login_required
# def profile_training_add(request):
#     if request.method == 'POST':
#         form = TrainingForm(request.POST, request.FILES)
#         if form.is_valid():
#             tr = form.save()
#             formset = AIFormSet(request.POST, request.FILES, instance=tr)
#             if formset.is_valid():
#                 formset.save()
#                 messages.add_message(request, messages.SUCCESS, 'Объявление добавлено')
#                 return redirect('blog:profile')
#     else:
#         form = TrainingForm(initial={'author': request.user.pk})
#         formset = AIFormSet()
#     context = {'form': form, 'formset': formset}
#     return render(request, 'blog/profile_tr_add.html', context)


@login_required
def profile_training_detail(request, pk):
    tr = get_object_or_404(Training, pk=pk)
    # ais = tr.additionalimage_set.all()
    # comments = Comment.objects.filter(bb=pk, is_active=True)
    context = {'tr': tr}
    # , 'ais': ais, 'comments': comments}
    return render(request, 'blog/profile_tr_detail.html', context)

# class UserInfo(SuccessMessageMixin, UpdateView):
#     model = User
#     template_name = 'blog/user_info.html'
#     form_class = UserForm
#     success_url = reverse_lazy('blog: index')
#     success_message = 'Данные отправлены'
#
#     def setup(self, request, *args, **kwargs):
#         self.user_id = request.user.pk
#         return super().setup(request, *args, **kwargs)
#
#     def get_object(self, queryset=None):
#         if not queryset:
#             queryset = self.get_queryset()
#         return get_object_or_404(queryset, pk=self.user_id)
