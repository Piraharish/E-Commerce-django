from django.urls import path
from django.contrib.auth import views as auth_view
from .form import MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm
from . import views
 
urlpatterns= [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart/',views.cart_page,name="cart"),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('collections',views.collections,name="collections"),
    path('collections/<str:name>',views.collectionsview,name="collections"),
    path('collections/<str:cname>/<str:pname>',views.product_details,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    path('collections/<str:cname>/<str:pname>/', views.product_detail, name='product_detail'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('save_address/', views.save_address, name='save_address'),
    path('saved_addresses/', views.saved_addresses, name='saved_addresses'),
    path('edit_address/<int:address_id>/', views.editAddress, name='edit_address'),
    path('update_cart_quantity/<int:item_id>/<int:new_quantity>/', views.update_cart_item_quantity, name='update_cart_quantity'),
    #path('payment/', views.payment, name='payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/failure/', views.payment_failure, name='payment_failure'),

    # Passwords
     path("passwordchange/",auth_view.PasswordChangeView.as_view(template_name="password/changepassword.html",form_class=MyPasswordChangeForm, success_url="/passwordchangedone"),name="passwordchange"),
    path("passwordchangedone/",auth_view.PasswordChangeDoneView.as_view(template_name="password/passwordchangedone.html"),name="passwordchangedone"),
    path("password-reset/",auth_view.PasswordResetView.as_view(template_name="password/password_reset.html", form_class=MyPasswordResetForm),name="password_reset"),
    path("password-reset/done/",auth_view.PasswordResetDoneView.as_view(template_name="password/password_reset_done.html"),name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",auth_view.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html",form_class=MySetPasswordForm),name="password_reset_confirm"),
    path("password-reset-complete/",auth_view.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"),name="password_reset_complete"),

]
 
