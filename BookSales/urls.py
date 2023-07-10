"""BookSales URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
import library.views.account as account
import library.views.books as books
import library.views.bills as bills
import library.views.orders as orders


urlpatterns = [
    path('admin/', admin.site.urls),
    
    #账户登录与退出
    path('login/',account.Login),
    path('logout/',account.LogOut),
    
    
    #管理员页面，会根据用户身份进行跳转
    path('admin_judge/',account.admin),
    
    #超级管理员——账号管理
    path('super_admin/',account.super_admin),  #超级管理员登录首页
    path('super_admin/user_list/',account.user_list),#用户列表页面
    path('super_admin/user_info/',account.user_info),#查询单个用户信息
    path('super_admin/user_delete/',account.user_delete),
    path('super_admin/user_add/',account.user_add),
    
    #普通管理员——信息编辑
    path('norm_admin/',account.norm_admin),#普通管理员登录首页
    path('norm_admin/user_edit/',account.user_edit),#普通管理员信息编辑页面
    
    
    
    #books管理
    path('books/',books.FirstPage),#首页
    path('books/search_book/',books.SearchBook),#库存书籍查询
    path('books/<int:id>/book_edit/',books.book_edit),#库存书籍信息编辑
    path('books/<int:id>/book_retail/',books.book_retail),#库存书籍零售
    
    
    #orders管理
    path('orders/order_list/',orders.order_list), #订单列表
    path('orders/order_list/<str:state>/', orders.order_list,name='order_list_by_state'), #订单分类查询
    path('orders/<int:book_id>/make_order/',orders.make_order),#创建库存书籍的订单
    path('orders/<int:order_id>/pay_order/',orders.pay_order),#订单付款
    path('orders/<int:order_id>/cancel_order/',orders.cancel_order),#订单退货
    path('orders/<int:order_id>/add_book/',orders.add_book),#到货订单加入库存
    path('orders/new_book_order/',orders.new_book_order),#为不在库存中的书籍创建订单
    
    #账单查询
    path('bills/',bills.SearchBill),
]
