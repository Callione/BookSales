from django.shortcuts import render,redirect
from library.models import BookInfo,Order,FinancialBill
from datetime import datetime


def make_order(request,book_id):
    """传入BookInfo的id,然后创建一条订单"""
    
    book=BookInfo.objects.filter(id=book_id).first()
    if request.method == 'POST':
        purchase_price=float(request.POST.get('purchase_price'))
        amount=int(request.POST.get('amount'))
        
        #检查输入是否合理
        if amount<=0:
            error='进货数量必须大于0'
            return render(request,'MakeOrder.html',{'error':error})
        elif purchase_price<0:
            error='进货价格异常,请重新填写'
            return render(request,'MakeOrder.html',{'error':error})
        
        
        #输入正常，则添加一条订单
        Order.objects.create(book=book,purchase_price=purchase_price,amount=amount,state='未付款')
        #返回订单列表，以便实时地进行付款或者退货
        return redirect('/orders/order_list/')

    return render(request,'MakeOrder.html')


def new_book_order(request):
    if request.method == 'POST':
        # 获取表单数据
        isbn = request.POST.get('isbn')
        title = request.POST.get('title')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        purchase_price = request.POST.get('purchase_price')
        amount = request.POST.get('amount')
        
        # 检查库存中是否已有该书籍信息
        book = BookInfo.objects.filter(isbn=isbn).first()
        
        if book:
            # 库存中已有该书籍信息，直接将其列入进货清单
            Order.objects.create(book=book, purchase_price=purchase_price, amount=amount, state='未付款')
        else:
            # 库存中没有该书籍信息，需要创建新的BookInfo并添加到进货清单
            new_book = BookInfo.objects.create(isbn=isbn, title=title, author=author, publisher=publisher, retail_price=0, amount=0)
            Order.objects.create(book=new_book, purchase_price=purchase_price, amount=amount, state='未付款')
        
        return redirect('/orders/order_list/')  # 重定向到订单列表页面
    return render(request,'NewBookOrder.html')


def order_list(request,state=None):
    '''显示订单列表'''
    
    if state:
        #筛选某一状态的订单
        order_list=Order.objects.filter(state=state)
    else:    
        #显示所有订单
        order_list=Order.objects.all()
    return render(request,'order_list.html',{'order_list':order_list})



def pay_order(request,order_id):
    """  为订单付款 """
    
    order=Order.objects.filter(id=order_id).first()
    #首先检查是不是未付款的订单
    if order.state !='未付款':
        return redirect('/orders/order_list')
    #如果是未付款的订单,那么改变订单状态，并且添加一条支出的bill
    order.state='已付款'
    order.save()
    #付款成功，创建一条支出的账单
    FinancialBill.objects.create(
        type='O',
        amount=order.amount*order.purchase_price,
        date=datetime.now().date()  #当前日期
    )
    return redirect('/orders/order_list/')


def cancel_order(request,order_id):
    """

    订单退货
    """
    order=Order.objects.filter(id=order_id).first()
    
    #首先检查是不是未付款的订单
    if order.state != '未付款':
        return redirect('/orders/order_list/')
    
    #如果是未付款的订单，那么修改状态
    order.state='已退货'
    order.save()
    return redirect('/orders/order_list/')



def add_book(request,order_id):
    '''对于已付款的订单,将新书添加到库存中'''
    order=Order.objects.filter(id=order_id).first()
    
    #首先检查是不是已付款的订单
    if order.state != '已付款':
        return redirect('/orders/order_list/')
    
    #如果用户设置好了retail_price，则去更新BookInfo
    if request.method=='POST':
        #更新BookInfo,需要修改amount和retail_price
        new_retail_price = float( request.POST.get('retail_price') )
        
        if new_retail_price > 0:
            
            book = order.book
            book.amount += order.amount
            book.retail_price  = new_retail_price
            book.save()
        
            #更改订单的状态
            order.state = '已添加'
            order.save()
        
            return redirect('/orders/order_list/')
        else:
            error='零售价应该设置为正整数'
            return render(request,'add_book.html',{'order':order,'error':error})    
    return render(request,'add_book.html',{'order':order})