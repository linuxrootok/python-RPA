import random,sys
from django.db import models
from django.contrib import admin,messages
from django.forms import TextInput, Textarea
from django.forms.models import BaseInlineFormSet
from .models import Project,Page,Element
#from django_admin_json_editor.forms import JSONEditorWidget
#from django_json_widget.widgets import JSONEditorWidget
#from django_admin_json_editor import JSONEditorWidget

from django.contrib.postgres import fields

from django.utils.html import format_html

from django.templatetags.static import static

from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .forms import MyForm
from django.shortcuts import render

from django.urls import path

import logging
import pdb


#from liststyle import ListStyleAdminMixin
#from django_json_widget.widgets import JSONEditorWidget
_version = 'v1.0'
admin.site.site_header = f"工汇RPA核心配置系统{_version}"

class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Project._meta.fields] # 显示所有字段
    list_filter = [field.name for field in Project._meta.fields] # 过滤所有字段

class PageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Page._meta.fields] # 显示所有字段
    list_filter = [field.name for field in Page._meta.fields] # 过滤所有字段


class UpdateFieldForm(forms.Form):
    my_field = forms.CharField(label='New Value')


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST'   # 设置表单提交方式为POST
        self.helper.form_action = '/my/custom/url/'  # 设置表单提交的URL
        self.helper.add_input(Submit('submit', 'Submit'))  # 添加提交按钮

    def clean_my_field(self):
        value = self.cleaned_data['my_field']
        # 在此处可以添加一些验证逻辑
        return value

class ElementAdmin(admin.ModelAdmin):
    #list_display = [field.name for field in Element._meta.fields] # 显示所有字段
    #list_filter = [field.name for field in Element._meta.fields] # 过滤所有字段
    #list_display = ['id','descriptAndStatus','myOffset', 'mark','mySequence','text','before_delay','after_delay','xpath','is_actived','updated_at'] # 显示所有字段
    
    ordering = ['sequence']


    def mySequence(self, obj):
        return obj.sequence  # or any other representation you want
    mySequence.short_description = '顺序'

    def myOffset(self, obj):
        return obj.offset  # or any other representation you want
    myOffset.short_description = '偏移'

    def descriptAndStatus(self, obj):

        color = self.get_row_css(obj)

        if not obj.is_actived:
            return format_html('<span style="text-decoration: line-through;">{}</span>', obj)
        else:
            if not obj.check:

                is_bold = ''

                if obj.offset:
                    is_bold = 'font-weight: bold'

                if not obj.text:
                    icon_path = static('admin/img/icon-viewlink.svg')
                else:
                    icon_path = static('admin/img/icon-addlink.svg')

                return format_html('<img src="{}" alt="True"> <span style="color:{};{}">{}</span>', icon_path, color, is_bold, obj.descript)
            else:
                icon_path = static('admin/img/search.svg')
                
                return format_html('<img src="{}" alt="True"> <span style="color:{};font-weight: bold;">{}</span>', icon_path, color, obj.descript)

    descriptAndStatus.allow_tags = True
    descriptAndStatus.short_description = '是否检测?+动作(点击+输入?)'

    def get_row_css(self, obj):
        css_class = ''
        if obj.offset < -10:
            css_class = self.get_color_by_value(obj.offset)
        return css_class

    def get_color_by_value(self, value):
        if not hasattr(self, '_value_colors'):
            # 初始化值-颜色字典
            self._value_colors = {}

        if value in self._value_colors:
            # 如果已有相同的值，则返回已有的颜色
            return self._value_colors[value]
        else:
            # 否则随机选择一种颜色并添加到字典中
            while True:
                color = self.select_random_color()
                if color not in self._value_colors.values():
                    self._value_colors[value] = color
                    break
            return color

    def select_random_color(self):

        # 随机选择一种颜色
        #case 1
        #color_list = ['darkmagenta', 'blue', 'orange', 'deeppink', 'brown', 'violet','green','gold', 'maroon', 'PaleGodenrod', 'darkslategray']
        '''case 2
        color_list = ["DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkGray", "DarkGreen", "DarkMagenta", "DarkOliveGreen", "DarkOrange", "DarkOrchid", "DarkRed", "DarkSlateBlue", "PaleGodenrod", "DarkTurquoise", "DarkViolet", "Indigo", "Maroon", "MidnightBlue", "Navy","Purple"]
        #color_list = []
        new_colors = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(len(color_list))]
        # 将 new_colors 中的 RGB 颜色转换为对应的十六进制字符串
        hex_colors = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in new_colors]

        # 将 color_list 中的颜色替换成新的随机颜色
        for i in range(len(color_list)):
            color_list[i] = hex_colors[i]
        '''
        #case 3
        def generate_color():
            """
            生成一个随机鲜艳的 RGB 颜色元组
            """
            r = random.randint(128, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            return (r, g, b)

        # 生成50种随机颜色
        color_list_base = [generate_color() for _ in range(50)]

        # 将 RGB 颜色转换为对应的十六进制字符串
        color_list = [f"#{r:02x}{g:02x}{b:02x}" for r, g, b in color_list_base]
        return random.choice(color_list)


    # 将CSS样式表添加到页面中
    class Media:
        css = {
            'all': ('css/custom.css',),
        }
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            del actions['duplicate_selected']
            del actions['swap_sequence']
        return actions


    def get_list_display(self, request):
        if request.user.is_superuser:
            return ['id','descriptAndStatus','myOffset', 'mark','mySequence','text','before_delay','after_delay','xpath','is_actived','updated_at']
        else:
            return ['id','descript','offset', 'mark','sequence','text','before_delay','after_delay','xpath','is_actived','updated_at']

    list_filter = ['page__project__name', 'page', 'check'] # 过滤所有字段

    search_fields = ['mark', 'descript','xpath', 'offset']

    actions = ['duplicate_selected', 'swap_sequence', 'update_offset', 'duplicate_reverse_selected']

    def duplicate_selected(self, request, queryset):
        success_count = 0
        error_count = 0
        random_mark = 'CP'+random.randint(100000, 200000).__str__()
        for obj in queryset:
            try:
                # 复制原始对象，并将主键设置为None，以便Django知道这是一个新对象
                new_obj = obj
                new_obj.pk = None
                new_obj.sequence = obj.sequence+2
                new_obj.mark = obj.mark+'-'+random_mark
                # 保存新对象
                new_obj.save()
                success_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(request, f"复制对象失败：{e}", level=messages.ERROR)

        if success_count > 0:
            self.message_user(request, f"已经成功复制了{success_count}个对象")
        if error_count > 0:
            self.message_user(request, f"复制对象过程中出现了{error_count}个错误，请查看详细信息", level=messages.WARNING)

    def duplicate_reverse_selected(self, request, queryset):
        success_count = 0
        error_count = 0
        random_mark = 'CP'+random.randint(100000, 200000).__str__()
        for obj in queryset:
            try:
                # 复制原始对象，并将主键设置为None，以便Django知道这是一个新对象
                new_obj = obj
                new_obj.pk = None
                sign = -1 if obj.offset < 0 else 1  
                new_offset = int(str(abs(obj.offset))[::-1])
                new_offset *= sign
                new_obj.offset = new_offset
                new_obj.sequence = obj.sequence+3
                new_obj.mark = obj.mark+'-'+random_mark
                # 保存新对象
                new_obj.save()
                success_count += 1
            except Exception as e:
                error_count += 1
                self.message_user(request, f"复制对象失败：{e}", level=messages.ERROR)

        if success_count > 0:
            self.message_user(request, f"已经成功复制了{success_count}个对象")
        if error_count > 0:
            self.message_user(request, f"复制对象过程中出现了{error_count}个错误，请查看详细信息", level=messages.WARNING)

    def swap_sequence(self, request, queryset):
        if queryset.count() != 2:
            self.message_user(request, "You can only select two rows for this action.")
            return
        obj1, obj2 = queryset
        obj1.sequence, obj2.sequence = obj2.sequence, obj1.sequence
        obj1.save()
        obj2.save()
        self.message_user(request, "Fields swapped successfully.")


    def update_offset(self, request, queryset):
        if 'POST' == request.method:
            form = UpdateFieldForm(request.POST)
            if form.is_valid():
                pass
            else:
                self.message_user(request, "Ready to update offset!")

        else:
            self.message_user(request, "Ready to update offset!")
            form = UpdateFieldForm()

        selected_ids = ','.join(str(obj.id) for obj in queryset)
        filters = request.GET.urlencode()
        context = {
            'queryset': queryset,
            'form': form,
            'action_name': 'Update branch',
            'ids': selected_ids,
            'filters': filters,
        }

        #request.session['selected_ids'] = list(queryset.values_list('id', flat=True))

        return TemplateResponse(request, 'admin/update_offset.html', context)

    '''
    urlpatterns = [
        path('update_offset', update_offset, name='my_custom_function'),
    ]
    '''
admin.site.register(Page, PageAdmin)
admin.site.register(Element, ElementAdmin)
admin.site.register(Project, ProjectAdmin)
