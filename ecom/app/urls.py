from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .forms import LoginForm, ChangePasswordForm, ResetPasswordForm, PasswordSetForm
urlpatterns = [

    # Products and Info
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<product_id>', views.ProductDetailView.as_view(), name='product-detail'),
    path('buy/', views.buy_now, name='buy-now'),

    # Products in user cart
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removeitem/', views.removeitem),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('orders/', views.orders, name='orders'),

    # Profile and Addresses
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('address/<addr_id>', views.delete_address, name='delete_address'),

    # Within-site password change
    path('changepassword/', auth_view.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=ChangePasswordForm, success_url='/passwordupdated/'), name='changepassword'),
    path('passwordupdated/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchanged.html'), name='passwordupdated'),
    
    # Password reset through email
    path('resetpassword/', auth_view.PasswordResetView.as_view(template_name='app/resetpassword.html', form_class=ResetPasswordForm), name='password_reset'),
    path('resetpassword/emailsent/', auth_view.PasswordResetDoneView.as_view(template_name='app/resetpassworddone.html'), name='password_reset_done'),
    path('resetpassword/confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name='app/resetpasswordconfirm.html', form_class=PasswordSetForm), name='password_reset_confirm'),
    path('resetpassword/complete/', auth_view.PasswordResetCompleteView.as_view(template_name='app/resetpasswordcomplete.html'), name='password_reset_complete'),

    # Authentication & Authorization
    path('accounts/login/', auth_view.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    # Adding products to categories & organised through filters
    path('phone/', views.phone, name='phone'),
    path('phone/<data>', views.phone, name='phonedata'),
    path('topwears/', views.topwear, name='shirts'),
    path('topwears/<data>', views.topwear, name='shirtsdata'),
    path('bottomwears/', views.bottomwear, name='jeans'),
    path('bottomwears/<data>', views.bottomwear, name='jeansdata'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
