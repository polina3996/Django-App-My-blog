class DataMixin:
    """Common attributes for several Cass Based Views"""
    paginate_by = 3
    # at the beginning these params are empty
    title_page = None
    cat_selected = None
    extra_context = {}

    def __init__(self):
        # if title and cat_selected are not empty in CBV
        if self.title_page:
            self.extra_context['title'] = self.title_page

        if self.cat_selected is not None:
            self.extra_context['cat_selected'] = self.cat_selected

    def get_mixin_context(self, context, **kwargs):
        context['cat_selected'] = None
        context.update(kwargs)
        return context