from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review

@login_required
def add(request):
	if request.method == 'POST':
		review = Review()
		review.author = request.user
		form = ReviewForm(request.POST, instance=review)
		if form.is_valid():
			form.save()
			return redirect(reverse('reviews.index'), context_instance=RequestContext(request))
	else:
		form = ReviewForm()

	return render_to_response(
		'reviews/add.html',
		{ 'form': form, },
		context_instance=RequestContext(request)
	)

@login_required
def index_for_user(request, username):
	review_list = User.objects.get(username=username).review_set.all()

	return render_to_response(
		'reviews/index_for_user.html',
		{ 'review_list': review_list, },
		context_instance=RequestContext(request)
	)

@login_required
def edit(request, review_id):
	review = get_object_or_404(Review, pk=review_id)
	if request.user == review.author:
		if request.method == 'POST':
			form = ReviewForm(request.POST, instance=review)
			if form.is_valid():
				form.save()
				messages.success(request, 'Entry updated.')
		else:
			form = ReviewForm(instance=review)
	else:
		raise Http404
	return render_to_response(
		'reviews/edit.html',
		{ 'form': form, },
		context_instance=RequestContext(request)
	)

@login_required
def remove(request, review_id):
	review = get_object_or_404(Review, pk=review_id)
	if request.user == review.author:
		review.delete()
	else:
		raise Http404
	return redirect(reverse('reviews.index'), context_instance=RequestContext(request))
