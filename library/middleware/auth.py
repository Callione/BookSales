from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class AuthMiddleware(MiddlewareMixin):
    def process_request(self,request):
        #login界面不需登录就可以访问
        if request.path_info == '/login/':
            return
        
        #读取session信息，判断是否登录过
        info_dict= request.session.get('info')
        if info_dict:
            return
        
        #没有登录过，返回login
        return redirect('/login')
    
class AuthSuperAdmin(MiddlewareMixin):
    def process_request(self,request):
        if '/super_admin/' in request.path_info:
            info_dict = request.session.get('info')
            if info_dict['role'] == 'S':
                return
            else:
                return redirect('/login/')