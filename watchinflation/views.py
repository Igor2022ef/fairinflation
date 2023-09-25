from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .utils import *
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

from .forms import *
from .models import *

from plotly.graph_objs import Scatter
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots



class ArticlesHome(DataMixin, ListView):
    model = Articles
    template_name = 'watchinflation/home.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    def get_queryset(self):
        # select_related('cat') сбор всех связанных данных с ForeignKey для уменьшения SQL запросов (оптимизация)
        return Articles.objects.filter(is_published=True).select_related('cat')

# @login_required                             # декоратор ограничивает доступ не авторизованных пользователей
# def about(request):
#     user_menu = menu.copy()
#     if not request.user.is_authenticated:
#         user_menu.pop(1)
#     return render(request, 'firstpart/about.html', {'menu': user_menu, 'title': 'О сайте'})

class About(DataMixin, DetailView):
    template_name = 'watchinflation/about.html'
    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_user_context(title="О сайте"))



class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'watchinflation/addpage.html'
    extra_context = {'title': 'Добавить статью'}
    success_url = reverse_lazy('home')                   #Иначе работает метод get_absolute_url
    login_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавить статью")
        return dict(list(context.items()) + list(c_def.items()))


class ShowPost(DataMixin, DetailView):
    model = Articles
    template_name = 'watchinflation/post.html'
    context_object_name = 'post'
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = context['post'])
        return dict(list(context.items()) + list(c_def.items()))

class ArticlesCategory(DataMixin, ListView):
    model = Articles
    template_name = 'watchinflation/home.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Articles.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class Graph(DataMixin, TemplateView):
    model = Buildgraph
    template_name = 'watchinflation/graph.html'

    def get_context_data(self, * , object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Построение графиков")
        context.update(c_def)

        graph_inf = Buildgraph.objects.all()
        date_list = []
        potrebl_1 = 0
        for g in graph_inf:
            date_list.append(g.date_numb.year)
        res = date_list[0]
        potrebl_moneu = []
        years_potrebl = []
        ipc_cepnoy = []
        ipc_base = []
        infl_bas = []
        infl_cep = []
        for g in graph_inf:
            if g.date_numb.year == res:
                potrebl_1 += g.sum_money
            else:
                years_potrebl.append(res)
                res += 1
                potrebl_moneu.append(potrebl_1)
                potrebl_1 = 0
        potrebl_moneu.append(potrebl_1)
        years_potrebl.append(res)
        ipc_base.append(1)
        for i in range(len(potrebl_moneu)-1):
            ipc_cepnoy_j = (potrebl_moneu[i+1])/(potrebl_moneu[i])
            infl_cep_i = (ipc_cepnoy_j - 1) * 100
            infl_cep.append(infl_cep_i)
            ipc_cepnoy.append(ipc_cepnoy_j)
            IPC_base_j = (potrebl_moneu[i+1])/(potrebl_moneu[0])
            infl_bas_i = (IPC_base_j - 1)*100
            infl_bas.append(infl_bas_i)
            ipc_base.append(IPC_base_j)
        ipc_cepnoy.insert(0, 1)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years_potrebl, y=ipc_base, name='ИПЦ базовый'))

        frames = []
        for i in range(1, len(years_potrebl)):
            frames.append(go.Frame(data=[go.Scatter(x=years_potrebl[:i + 1], y=ipc_base)]))
        fig.frames = frames


        years_potrebl.pop(0)
        fig.add_trace(go.Scatter(x=years_potrebl, y=ipc_cepnoy, name='ИПЦ цепной'))
        fig.add_trace(go.Scatter(x=years_potrebl, y=infl_bas, name='Инфляция по базовому'))
        fig.add_trace(go.Scatter(x=years_potrebl, y=infl_cep, name='Инфляция по цепному'))
        fig.update_xaxes(range=[2017, 2022])

        fig.update_layout(legend_orientation="h",margin=dict(l=0, r=100, t=0, b=0), updatemenus=[
            dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None])])], height=500)
        fig.update_traces(hoverinfo="all", hovertemplate="Год: %{x}<br>Инфляция: %{y}")

        context['graph'] = fig.to_html()
        return context

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'watchinflation/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'watchinflation/login.html'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))
    def get_success_url(self):
        return reverse_lazy('home')

def logout_user(request):
    logout(request)
    return redirect('login')

def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

