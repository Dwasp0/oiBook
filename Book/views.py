from django.shortcuts import render, get_object_or_404
from django.db.models import F;
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from pygments import highlight
from pygments.lexers import guess_lexer
from pygments.formatters import HtmlFormatter

import datetime
import markdown
import re

from .models import Comment, Page

def index(request):
    latest_page_list = Page.objects.order_by("pub_date")[:50]
    context = {"latest_page_list": latest_page_list}
    return render(request, "Book/index.html", context)

def change_formula(matched):
    formula = matched.group(0)
    formula = formula.replace('_', ' _')
    return '\n<p>'+formula+'</p>\n'


def detail(request, page_id):
    if (request.method == 'GET'):
        try:
            page = Page.objects.get(pk=page_id)
            # content = highlight(page.page_text, guess_lexer(page.page_text), HtmlFormatter())
            content = markdown.markdown(re.sub(r'\$\$(.+?)\$\$', 
                                        change_formula, 
                                        page.page_text),
                                        extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                         #'mdx_math',
                                      ])
            # content = markdown.markdown(page.page_text,
            #                             extensions=[
            #                              'markdown.extensions.extra',
            #                              'markdown.extensions.codehilite',
            #                              'markdown.extensions.toc',
            #                           ])
        except Page.DoesNotExist:
            raise Http404("Page does not exist")
        return render(request, "Book/detail.html", {"page": page, "content": content})
    else:
        page = get_object_or_404(Page, pk=page_id)
        try:
            comment = Comment(comment_text=request.POST["enter_comment"], author_name=request.user.username, page_id=page_id)
            comment.pub_date=timezone.now()

            content = markdown.markdown(re.sub(r'\$\$(.+?)\$\$', 
                                        change_formula, 
                                        page.page_text),
                                        extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                         'markdown.extensions.toc',
                                      ])

            if comment.comment_text.strip()=="":
                return render(request, "Book/detail.html", {"page":page, "content":content, "error_message":"请填写评论之后提交..."})
        except (KeyError, Page.DoesNotExist):
            # Redisplay the question voting form.
            return render(
                request,
                "Book/detail.html",
                {
                    "page": page,
                    "content":content,
                    "error_message": "请填写评论之后提交...",
                },
            )
        else:
            comment.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse("Book:detail", args=(page.id,)))

@login_required(login_url="/login/")
def exercise(request, page_id):
    page = Page.objects.get(pk=page_id)
    return render(request, "Book/exercises.html", {"page":page})
    
def register(request):
    if request.method == 'GET':
        return render(request, "Book/register.html")
    else:
        user = User(username=request.POST["username"], email=request.POST["e-mail"], password=request.POST["password"])
        user.password=make_password(user.password)
        try:
            user.save()
        except Exception:
            return render(request, "Book/register.html", {"error_message":"似乎已经注册过了..."})
        login(request, user)
        return HttpResponseRedirect("/")

def loginview(request):
    if request.method == 'GET':
        return render(request, "Book/login.html")
    else:
        user = authenticate(username=request.POST["username"], password=request.POST["password"])

        if (user):
            login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, "Book/login.html", {"error_message":"用户名或密码错误..."})

def logoutview(request):
    logout(request)
    latest_page_list = Page.objects.order_by("-pub_date")[:5]
    context = {"latest_page_list": latest_page_list}
    return HttpResponseRedirect("/")

def search(request):
    result = Page.objects.filter(page_title__icontains=request.POST["search_content"])
    context = {"result": result}
    return render(request, "Book/search.html", context)