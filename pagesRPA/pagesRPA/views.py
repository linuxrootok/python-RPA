from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.messages import constants as messages
from django.contrib import messages as django_messages
from .models import Element

def my_form_view(request):

	if 'POST' == request.method:

		filters = request.POST.get('filters', '')

		target_offset = request.POST.get('my_field', '')

		selected_ids_str = request.POST.get('ids', '')

		selected_ids = tuple(map(int, selected_ids_str.split(',')))

		Element.objects.filter(id__in=selected_ids).update(offset=target_offset)

		# 使用success消息级别发送消息
		django_messages.add_message(request, messages.SUCCESS, f"{len(selected_ids)} objects were updated")	

		return HttpResponseRedirect(reverse('admin:pagesRPA_element_changelist')+ '?' + filters)
