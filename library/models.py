from django.db import models

# Create your models here.

class BookInfo(models.Model):
    isbn = models.CharField(verbose_name='ISBN',max_length=13,unique=True)
    title = models.CharField(verbose_name='书名',max_length=50)
    publisher = models.CharField(verbose_name='出版社',max_length=50,null = True,blank = True)
    author =models.CharField(verbose_name='作者', max_length=50)    
    retail_price = models.DecimalField(max_digits=10,decimal_places=2)
    amount = models.BigIntegerField()
    def  __str__(self):
        return self.title
    

class Administrator(models.Model):
    username = models.CharField(verbose_name='用户名',max_length=50,unique=True)
    password = models.CharField(verbose_name='密码',max_length=50)
    employee_id = models.CharField(verbose_name='工号',max_length=11, null=True, blank=True)
    real_name = models.CharField(verbose_name='姓名',max_length=50, null=True, blank=True)
    Gender_Choices=(
        ('M','男'),
        ('F','女'),
    )
    gender = models.CharField(max_length=1,choices=Gender_Choices, null=True, blank=True)
    age = models.PositiveIntegerField( null=True, blank=True)
    Identity_Choices=(
        ('S','超级管理员'),
        ('N','普通管理员'),
    )
    identity = models.CharField(max_length=1,choices=Identity_Choices)
    
    def __str__(self):
        return self.username
    
class Order(models.Model):
    book = models.ForeignKey(BookInfo, on_delete=models.CASCADE)
    purchase_price=models.DecimalField(verbose_name='进货价格',max_digits=10,decimal_places=2)
    amount=models.PositiveBigIntegerField()
    State_Choices=(
        ('未付款','未付款'),
        ('已付款','已付款'),
        ('已退货','已退货'),
        ('已添加','已添加')
    )
    state = models.CharField(max_length=6,choices=State_Choices)
    
    def __str__(self):
        return f'{self.book.title}-{self.state}'
    
class FinancialBill(models.Model):
    type_choices=(
        ('I','收入'),#顾客购买书籍
        ('O','支出'),#库存进货
    )
    type=models.CharField(verbose_name='类型',max_length=1,choices=type_choices)
    amount=models.DecimalField(verbose_name='金额',max_digits=20,decimal_places=2)
    date = models.DateField(verbose_name='日期')
    def __str__(self):
        return f'{self.type}{self.amount}'
    
