import re
from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin


class ValidPermission(MiddlewareMixin):
    """
    权限验证中间件类
    """
    def process_request(self, request):
        # 间件内容start
        path = request.path_info
        # 查看是否属于白名单
        valid_url_list = ['/login/', '/register/', '/admin/.*']
        for valid_url in valid_url_list:
            ret = re.match(valid_url, path)
            if ret:
                return None
        # 获取session键值，如果不存在，不报错，返回[]
        permission_list = request.session.get('permission_list', [])
        # print(permission_list)

        # print(path)
        flag = False
        for permission in permission_list:
            permission = "^%s$" % permission
            ret = re.match(permission, path)
            if ret:
                flag = True
                break
        # print(flag)
        if not flag:
            return HttpResponse('无访问权限！')
        # 中间件内容end
        return None
