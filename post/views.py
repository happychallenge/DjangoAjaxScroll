from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
# Create your views here.
from .models import Post


def post_list(request):
	post_list = Post.objects.all().order_by('-created_date')
	paginator = Paginator(post_list, 10)
	page = request.POST.get('page')

	try:
		post_list = paginator.page(page)
	except PageNotAnInteger:
		post_list = paginator.page(1)
	except EmptyPage:
		post_list = paginator.page(paginator.num_pages)
		
	context = {'post_list':post_list}
	return render(request, 'post/post_list.html', context)

def post_list_ajax(request):
	post_list = Post.objects.all().order_by('-created_date')
	paginator = Paginator(post_list, 10)
	page = request.POST.get('page')

	try:
		post_list = paginator.page(page)
	except PageNotAnInteger:
		post_list = paginator.page(1)
	except EmptyPage:
		post_list = paginator.page(paginator.num_pages)

	context = {'post_list':post_list}
	return render(request, 'post/post_list_ajax.html', context)


def post_create(request):
	pass

def post_detail(request,post_id):
	post = get_object_or_404(Post, pk=post_id)
	post.read += 1
	post.save()
	context = {'post':post}
	return render(request, 'post/post_detail.html', context)

def post_update(request,post_id):
	pass

def post_delete(request,post_id):
	pass

def post_search(request):
	if request.method == 'POST':
		search_text = request.POST['search_text']
	else:
		search_text = ''
	post_list = Post.objects.filter(Q(title__contains = search_text) | Q(content__contains = search_text))
	context = { 'post_list': post_list }
	return render(request, 'post/ajax_result.html', context)

def post_likes(request, post_id):
	if post_id:
		post = Post.objects.get(id = post_id)
		post.likes += 1
		post.save()
	context = { 'post': post }
	return render(request, 'post/post_likes.html', context )	