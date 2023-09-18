from django.core.paginator import Paginator as Paginate, EmptyPage, PageNotAnInteger


class Paginator(object):
    queryset = None
    page_kwargs = "page"
    paginate_by = 10
    context_object_name = "paginator"
    
    def gq_queryset(self, **kwargs):
        return self.queryset.objects.all()
    
    def get_context_data(self, **kwargs):
        context = {}
        page_num = self.request.GET.get(self.page_kwargs, 1)
        paginator = Paginate(self.gq_queryset(**kwargs), self.paginate_by)

        try:
            page_obj = paginator.page(page_num)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            page_obj = paginator.page(1)

        if page_obj.has_previous():
            prev_url = "?{kw}={n}".format(
                kw=self.page_kwargs, n=page_obj.previous_page_number()
            )
        else:
            prev_url = None

        if page_obj.has_next():
            next_url = "?{kw}={n}".format(
                kw=self.page_kwargs, n=page_obj.next_page_number()
            )
        else:
            next_url = None
        context['is_paginated'] = page_obj.has_other_pages()
        context[self.context_object_name] = page_obj
        context["next_url"] = next_url
        context["prev_url"] = prev_url
        return context
