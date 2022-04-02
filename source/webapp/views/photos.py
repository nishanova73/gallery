from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404, render

from django.views.generic import (
                                  ListView,
                                  CreateView,
                                  DetailView,
                                  UpdateView,
                                  DeleteView
                                  )

from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.views import View
from django.utils.http import urlencode
import uuid
from webapp.models import Photo, Album, Link
from webapp.forms import PhotoForm


class GetPhoto(View):
    def get(self,request, *args, **kwargs):
        uuid = kwargs.get('uuid')
        photo = Photo.objects.get(link__link=uuid)
        context={}
        context['photo'] = photo
        return render(request,'photo/view.html', context=context )


class GetUUID(View):
    def get(self, request, *args, **kwargs):
        photo = get_object_or_404(Photo, id = kwargs.get('pk'))
        link = Link.objects.create(photo = photo, link=str(uuid.uuid4()))
        return redirect('webapp:photo-view', pk=photo.id)

class IndexView(LoginRequiredMixin, ListView):
    template_name = 'photo/index.html'
    model = Photo
    context_object_name = 'photos'
    ordering = ("-created_at")

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(Q(is_private=False) & (Q(album__is_private=False)) | Q(album__isnull=False))
        return queryset

class PhotoView(LoginRequiredMixin, DetailView):
    model = Photo
    template_name = 'photo/view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author']=self.object.author==self.request.user
        return context


class CreatePhotoView(LoginRequiredMixin, CreateView):
    template_name = 'photo/create.html'
    form_class = PhotoForm
    model = Photo
    success_url = reverse_lazy('webapp:photo-list')

    def get_form_kwargs(self):
        kwargs = super(CreatePhotoView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        self.photo = form.save(commit=False)

        self.photo.author = self.request.user
        self.photo.save()

        return  self.get_success_url()

    def get_success_url(self):
        return redirect('webapp:photo-view', pk = self.photo.id)

class PhotoUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = PhotoForm
    model = Photo
    template_name = 'photo/update.html'
    context_object_name = 'photo'
    permission_required = 'webapp.change_photo'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()

    def get_success_url(self):
        return reverse('webapp:photo-view', kwargs={'pk': self.kwargs.get('pk')})

    def get_form_kwargs(self):
        kwargs = super(PhotoUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

class PhotoDeleteView(PermissionRequiredMixin, DeleteView):
    model = Photo
    template_name = 'partial/delete.html'
    context_object_name = 'object'
    success_url = reverse_lazy('webapp:photo-list')
    permission_required = 'webapp.delete_photo'

    def has_permission(self):
        return self.get_object().author == self.request.user or super().has_permission()