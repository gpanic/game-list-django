from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.template import RequestContext
from django.core.urlresolvers import reverse

from apps.reviews.forms import ReviewForm
from apps.reviews.models import Review

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