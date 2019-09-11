from django.shortcuts import render, redirect
from django.views.generic import ListView, View, CreateView, UpdateView, DeleteView, RedirectView
from .models import JobOpening
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CreateJobForm
# Create your views here.




class AllJobs(ListView):
    
    ordering = ['-date_posted']
    context_object_name = 'posts'
    paginate_by = 30

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['model'] = self.model
        return context
    
    def get_queryset(self):
        posts = JobOpening.objects.all()
        return posts
    

class CreateJobOpening(LoginRequiredMixin, CreateView):
    model = JobOpening
    paginate_by = 30

    def get(self, request):
        form = CreateJobForm()
        context = {
            'form': form,
        }
        return render(request, 'blog/post_form.html', context)
    
    def post(self, request):
        if request.method == 'POST':
            form = CreateJobForm(request.POST, request.FILES or None)
            if form.is_valid():
                print('Valid form')
                job_title = form.cleaned_data['job_title']
                method_of_application = form.cleaned_data['method_of_application']
                field = form.cleaned_data['field']
                education = form.cleaned_data['education']
                industry = form.cleaned_data['industry']
                image = form.cleaned_data['image']  # request.POST.get('image')
                job_description = form.cleaned_data['job_description']
                send_cv_directly = form.cleaned_data['send_cv_directly']
                experience = form.cleaned_data['experience']
                job_create =  JobOpening.objects.create(user= request.user, job_title= job_title, 
                                                        job_description= job_description, 
                                                        industry= industry, field= field, 
                                                        education= education, experience=experience,
                                                        send_cv_directly=send_cv_directly,
                                                        method_of_application= method_of_application, 
                                                        image= image)
                job_create.save()            
                return redirect('blog-home')
            else:
                print('Invalid')    
        else:

            form = CreateJobForm()

        context = {
            'form': form 
        }
        return render(request, 'blog/post_form.html', context)
