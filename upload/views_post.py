from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.forms import generic_inlineformset_factory
from django.forms.models import inlineformset_factory
from django.forms import ModelForm
from upload.forms import FileForm
from upload.models import File, get_collection_model, get_content_object
from upload import app_settings

Col = get_collection_model()


class ColForm(ModelForm):
    class Meta:
        model = Col
        fields = []


class FilesEditView(DetailView):
    model = Col
    template_name = "upload/post.html"
    col_form = ColForm

    def file_set(self, generic=False):
        if generic:
            return generic_inlineformset_factory(File, FileForm)
        else:
            return inlineformset_factory(self.model, File, FileForm)

    def post(self, request, pk=None, app_label=None, model=None, object_id=None):
        col = self.get_object() if pk else None
        obj = get_content_object(app_label, model, object_id)
        instance = obj or col

        data = [request.POST]
        if request.FILES:
            data.append(request.FILES)

        form = self.col_form(*data, instance=col)
        files = self.file_set(generic=bool(obj))(*data, instance=instance)

        if form.is_valid():
            if not obj:
                col = form.save(commit=False)
                col.user = request.user
                col.save()
            for file_form in files.forms:
                f = file_form.save(col, request)
                if file_form.cleaned_data.get('DELETE', False):
                    f.delete()
                elif f:
                    f.content_object = instance
                    f.save()
            return redirect(instance)
        return

    def get(self, request, pk=None, app_label=None, model=None, object_id=None):
        col = self.get_object() if pk else None
        obj = get_content_object(app_label, model, object_id)

        form = self.col_form(instance=col)
        files = self.file_set(generic=bool(obj))(instance=obj or col)

        if not col and not obj:
            url = reverse('xhr_up')
        elif col:
            url = reverse('xhr_up_col', kwargs={'pk': col.pk}) 
        elif obj:
            url = reverse('xhr_up_gfk', kwargs={'app_label': app_label,
                                                'model': model,
                                                'object_id': object_id})

        return render(request, self.template_name, {
            'col': col,
            'form': form,
            'images': files,
            'instance': obj,
            'xhr_upload_url': url,
            'upload_imap_enabled': app_settings.UPLOAD_IMAP_ENABLED,
            'upload_imap_email': app_settings.UPLOAD_IMAP_EMAIL
        })
