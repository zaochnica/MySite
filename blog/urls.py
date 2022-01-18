from django.urls import path
from django.views.generic import detail

from blog.views import (
    index,
    user_activate,
    RegisterDoneView,
    RegisterUserView,
    UserLogoutView,
    UserPasswordChangeView,
    DeleteUserView,
    ChangeUserInfoView,
    profile,
    profile_training_delete,
    # profile_training_change,
    # profile_training_add,
    profile_training_detail,
    UserPasswordResetDoneView,
    UserPasswordResetView,
    UserPasswordResetCompleteView,
    UserPasswordResetConfirmView,
    UserLoginView,
)

app_name = 'blog'

urlpatterns = [
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/logout/', UserLogoutView.as_view(), name='logout'),
    path('accounts/password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('accounts/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    # path('accounts/profile/change/<int:pk>/', profile_training_change, name='profile_bb_change'),
    path('accounts/profile/delete/<int:pk>/', profile_training_delete, name='profile_tr_delete'),
    # path('accounts/profile/add/', profile_training_add, name='profile_bb_add'),
    path('accounts/profile/<int:pk>/', profile_training_detail, name='profile_tr_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/password/reset/done/', UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('accounts/password/reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('accounts/password/confirm/complete/', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('accounts/password/confirm/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/login/', UserLoginView.as_view(), name='login'),
    # path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    # path('', index, name='index'),
    path('', index, name='index'),
]

# path('<int:pk>/', by_rubric, name='by_rubric'),
    # path('<str:page>/', other_page, name='other'),
# path('<int:by_format>/', by_format, name='by_format'),
