from django.shortcuts import render,redirect
from django.http import HttpResponse
from library.models import BookInfo,Order,FinancialBill
from datetime import datetime

from django import forms


#为图书编辑定义一个modelForm
class BookEditMForm(forms.ModelForm):
    class Meta:
        model = BookInfo 
        fields = ['title','author','publisher','retail_price']



#------和图书管理有关的函数都在这个文件里-------

def FirstPage(request):
    return render(request,'FirstPage.html')


def SearchBook(request):
    """图书查询列表"""
    if request.method == "GET":
        book_list=BookInfo.objects.order_by('id')
        return render(request,'SearchBook.html',{'book_list':book_list})

    else:
        #用户提交查询信息时，找到对应的书籍
        value=request.POST.get('value')
        key=request.POST.get('key')
        field=''
        dict={}
        if key=='书籍编号':
            field='id'
        elif key=='ISBN':
            field='isbn__contains'
        #下面的内容只需要输入一部分即可查询到
        elif key=='书籍名称':
            field='title__contains'
        elif key=='作者':
            field='author__contains'
        else:
            field='publisher__contains'
            
        #有时用户会什么都不填，直接提交，此时我们的value为none,这样创造出的dict传入filter后会报错            
        if value:
            #只有当用户提交了内容，才创建dict
           dict[field]=value
           
        book_list=BookInfo.objects.filter(**dict).order_by('id')
        
        return render(request,'SearchBook.html',{"book_list":book_list})
    
    
def book_edit(request,id):
    
    """图书信息编辑,参数为图书id    """
    
    book=BookInfo.objects.filter(id=id).first()
    if request.method == "GET":
        #book_id=request.GET.get('nid')

        form=BookEditMForm(instance=book)
        return render(request,'book_edit.html',{'form':form})
    else:
        form = BookEditMForm(data = request.POST,instance=book)
        if form.is_valid():
            form.save()
            return redirect('/books/search_book/')
        return render(request,'book_edit.html',{"form":form})
    
    
def book_retail(request,id):
    '''图书零售:参数为图书id'''
    book=BookInfo.objects.filter(id=id).first()
    if request.method == 'GET':
        return render(request,'book_retail.html',{"book":book})
    else:
        retail_amount=None
        retail_amount=int(request.POST.get('quantity'))
        
        if not retail_amount:
            error='零售数量需要输入正整数'
            return render(request,'book_retail.html',{"book":book,"error":error})
            
        
        #当零售数量不合理时，返回错误提示
        if retail_amount>book.amount:
            error='库存余量不足,需要补货'
            return render(request,'book_retail.html',{"book":book,"error":error})
        elif retail_amount<=0:
            error='零售数量应为正数'
            return render(request,'book_retail.html',{"book":book,"error":error})
        
        
        #零售成功，更新BookInfo，新增一条bill
        book.amount=book.amount-retail_amount
        book.save()
        FinancialBill.objects.create(
            type='I',
            amount=book.retail_price*retail_amount,
            date=datetime.now().date()  #当前日期
        )
        return redirect('/books/search_book/')