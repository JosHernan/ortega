from django.shortcuts import get_object_or_404, render,  render_to_response
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from .models import Casos
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment
from comments.forms import CommentForm
from app.forms import LoginForm,RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from ortega.settings import URL_LOGIN

def principal(request):
	return render(request,"index.html")


def post(request):
	post_list=Casos.objects.all()
	paginator = Paginator(post_list, 6) # Show 25 contacts per page
	page = request.GET.get('page')
	try:
		casos = paginator.page(page)
	except PageNotAnInteger:
		casos = paginator.page(1)
	except EmptyPage:
		casos = paginator.page(paginator.num_pages)
	return render(request,'post.html', {"casos": casos})


def detalle_post(request, caso_id=None):
	instance=get_object_or_404(Casos,pk=caso_id)
	try:
		detalle = Casos.objects.get(pk=caso_id)
		cat=detalle.categoria.all() # Obteniendo las categorias del producto encontrado relacion many to many
		it=Casos.objects.all()
		content_type=ContentType.objects.get_for_model(Casos)
		initial_data ={
				"content_type": instance.get_content_type,
				"object_id": instance.id


		}
		form=CommentForm(request.POST or None, initial=initial_data)
		if form.is_valid():
			c_type = form.cleaned_data.get("content_type")
			content_type = ContentType.objects.get(model=c_type)
			obj_id = form.cleaned_data.get('object_id')
			content_data = form.cleaned_data.get("content")
			parent_obj = None
			try:
				parent_id = int(request.POST.get("parent_id"))
			except:
				parent_id = None
			if parent_id:
					parent_qs = Comment.objects.filter(id=parent_id)
					if parent_qs.exists() and parent_qs.count() == 1:
							parent_obj = parent_qs.first()

			new_comment, created = Comment.objects.get_or_create(
							user = request.user,
							content_type= content_type,
							object_id = obj_id,
							content = content_data,
							parent = parent_obj
						)
			return HttpResponseRedirect(new_comment.content_object.get_absolute_url())
		comments=instance.comments	
	except Casos.DoesNotExist:
		raise Http404("Not Caso does not exist")
	return render(request, 'detalle_post.html', {'detalle': detalle,'categoria':cat,'itera':it,'instance':instance,"comments":comments,"comment_form":form})



def login_view(request):
	mensaje = ""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect("/")
				else:
					mensaje = "usuario y/o password incorrecto"
		
		form = LoginForm()
		ctx = {'form':form,'mensaje':mensaje}
		return render_to_response('login.html',ctx,context_instance=RequestContext(request))


def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			usuario = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=usuario,email=email,password=password_one)
			u.save() # Guardar el objeto
			return render_to_response('thanks_register.html',context_instance=RequestContext(request))
		else:
			ctx = {'form':form}
			return 	render_to_response('registrarse.html',ctx,context_instance=RequestContext(request))
	ctx = {'form':form}
	return render_to_response('registrarse.html',ctx,context_instance=RequestContext(request))	

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')