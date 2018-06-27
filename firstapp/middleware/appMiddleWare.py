from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, redirect

class appMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        print('>>>>>> process_request',request)
        gname = request.session.get('gname',None)
        if request.path in settings.LOGINREQUIRE_PATHS and not gname:
            return redirect(reverse('app:login'))


    def process_view(self,request, view_func, view_args, view_kwargs):
        print('>>>>>> process_view', request, view_func, view_args, view_kwargs)
        # request['test'] = 123
        return view_func(request, *view_args, **view_kwargs)

    def process_template_response(self, request, response):
        print('>>>>>> process_template_response', request, response)
        return response


    def process_exception(self,request, exception):
        print('>>>>>> process_exception', request, exception)

    def process_response(self, request, response):
        print('>>>>>> process_response', request, response)
        return response