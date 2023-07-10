from django.shortcuts import render,redirect
from library.models import FinancialBill
from datetime import datetime
from django.db.models import Sum  #方便计算流水

def SearchBill(request):
    total_income=0
    total_expense=0
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # 将日期字符串转换为 datetime 对象
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

        bill_list = FinancialBill.objects.filter(date__range=(start_date, end_date))
        
        #计算总收入和总支出
        total_income = bill_list.filter(type='I').aggregate(total=Sum('amount'))['total']
        total_expense = bill_list.filter(type='O').aggregate(total=Sum('amount'))['total']
        net_profit = total_income - total_expense if total_income and total_expense else None
        
    else:
        bill_list=FinancialBill.objects.all()
        #计算总收入和总支出
        total_income = bill_list.filter(type='I').aggregate(total=Sum('amount'))['total']
        total_expense = bill_list.filter(type='O').aggregate(total=Sum('amount'))['total']
        net_profit = total_income - total_expense if total_income and total_expense else None
        
    return render(request,'SearchBill.html',{'bill_list':bill_list,
                                             'total_income':total_income,
                                             'total_expense':total_expense,
                                             'net_profit':net_profit})