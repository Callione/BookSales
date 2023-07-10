from django.shortcuts import render,redirect
from django.http import HttpResponse
from library.models import Administrator,BookInfo,Order,FinancialBill
from library.encrypt import md5

# Create your views here.


from django import forms

class login_Form(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required= True
    )
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)

class UserMForm(forms.ModelForm):
    class Meta:
        model = Administrator
        fields =['username','password','employee_id','real_name','gender','age']  #'__all__' 
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #给所有的插件添加 class='form-control'
        for name,field in self.fields.items():
            field.widget.attrs={'class':"form-control",'placeholder':field.label}
    def clean_password(self):
        pwd=self.cleaned_data.get('password')
        return md5(pwd)


#登录界面的html不应该套用母版，不需要导航栏和退出按钮
def Login(request):
    if request.method == 'GET': 
        form = login_Form()
        return render(request,'login.html',{'form':form})
    
  
    if request.method == 'POST':
        form = login_Form(data=request.POST)
        if form.is_valid():
            admins=Administrator.objects.filter(**form.cleaned_data)
            if admins.exists():
                admin=admins.first()
                request.session['info']={'id':admin.id,'role':admin.identity}
                if admin.identity == 'S':
                    return redirect('/super_admin/')
                else :
                    return redirect('/norm_admin/')
                
        form.add_error('password','用户名或密码错误')            
        return render(request,'login.html',{'form':form})


def LogOut(request):
    '''退出'''
    request.session.clear()
    
    return redirect('login/')
    


def admin(request):
    if request.session['info']['role']=='S':
        return redirect('/super_admin/')
    return redirect('/norm_admin/')

#------------------超级管理员-------------------
def super_admin(request):
    return render(request,'SuperAdmin.html')

#查看用户列表
def user_list(request):
    user_list=Administrator.objects.filter(identity='N')
    return render(request,'user_list.html',{'user_list':user_list})

#查看单个用户的全部信息
def user_info(request):
    nid=request.GET.get('nid')
    user=Administrator.objects.filter(id=int(nid)).first()
    form=UserMForm(instance=user)
    return render(request,'user_info.html',{'form':form})

def user_delete(request):
    nid = request.GET.get('nid')
    Administrator.objects.filter(id=int(nid)).delete()
    return redirect('/super_admin/user_list')

def user_add(request):
    if request.method == 'GET':
        return render(request,'user_add.html')
    user=request.POST.get('user')
    pwd=request.POST.get('pwd')
    md5_pwd=md5(pwd)
    Administrator.objects.create(username=user,password=md5_pwd,identity='N')
    return redirect('/super_admin/user_list')



#------------------------普通管理员--------------------------

def norm_admin(request):
    return render(request,'NormalAdmin.html')

def user_edit(request):
    """编辑自己的信息"""
    
    #根据session里存的id值，找到对应的数据
    user_id=request.session['info']['id']
    userInfo=Administrator.objects.filter(id=user_id).first()
    
    if request.method == "GET":
        
        #创建一个对应的form，字段里没有identity(防止权限被改变)
        form = UserMForm(instance = userInfo)
        return render(request,'user_edit.html',{"form":form})
    
    else:
        #创建对应的form
        form = UserMForm(data = request.POST,instance=userInfo)
        if form.is_valid():
            form.save()
            return redirect('/norm_admin/')
        return render(request,'user_edit.html',{"form":form})



