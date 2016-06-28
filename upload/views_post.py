from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.forms.models import BaseInlineFormSet
from django.forms.models import inlineformset_factory as inline
from django.forms import ModelForm
from upload.forms import FileForm
from upload.models import File, get_collection_model
from upload import app_settings


class ColForm(ModelForm):
    class Meta:
        model = get_collection_model()
        exclude = ['user']


class FilesEditView(DetailView):
    model = get_collection_model()
    template_name = "upload/post.html"
    col_form = ColForm

    def file_set(self):
        return inline(self.model, File, FileForm, BaseInlineFormSet,
                      extra=4, can_delete=True, max_num=30)

    def post(self, request, pk=None, col=None):
        if pk:
            col = self.get_object()

        data = [request.POST]
        if request.FILES:
            data.append(request.FILES)

        form = self.col_form(*data, instance=col)
        files = self.file_set()(*data, instance=col)

        if form.is_valid():
            col = form.save()
            for file_form in files.forms:
                f = file_form.save(col, request)
                if file_form.cleaned_data.get('DELETE', False):
                    f.delete()
                elif f:
                    f.save()
            return redirect(col)
        return

    def get(self, request, pk=None, col=None):
        if pk:
            col = self.get_object()

        form = self.col_form(instance=col)
        files = self.file_set()(instance=col)

        return render(request, self.template_name, {
            'col': col,
            'form': form,
            'images': files,
            'upload_imap_enabled': app_settings.UPLOAD_IMAP_ENABLED,
            'upload_imap_email': app_settings.UPLOAD_IMAP_EMAIL
        })
