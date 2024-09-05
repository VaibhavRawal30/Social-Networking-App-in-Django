from django.shortcuts import render, redirect
from .forms import TweetForm, UserRegistrationForm
from .models import Tweet, Comment, Like
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login 
from django.http import JsonResponse
# Create your views here.


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('tweet_list') 
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')

    for tweet in tweets:
        tweet.user_liked = tweet.likes.filter(user=request.user).exists() if request.user.is_authenticated else False
    return render(request, 'tweet_list.html', {'tweets' : tweets})

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm()
    return render(request, 'tweet_form.html', {'form' : form})

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance = tweet)
        if form.is_valid():
            tweet = form.save(commit = False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance = tweet)
    return render(request, 'tweet_form.html', {'form': form})

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk = tweet_id, user = request.user)
    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})




def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id = tweet_id)
    comments = tweet.comments.all().order_by('-created_at')
    return render(request, 'post_detail.html', {'tweet': tweet, 'comments': comments})


@login_required
def add_comment(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        if comment_text:
            # Create a new comment and associate it with the tweet and the user
            Comment.objects.create(
                tweet=tweet,
                user=request.user,
                comment_text=comment_text
            )
        return redirect('tweet_list')  # Redirect to the tweet list after adding the comment

    return render(request, 'tweet_list.html', {'tweet': tweet})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, user=request.user)
    tweet_id = comment.tweet.id
    comment.delete()
    return redirect('tweet_detail', tweet_id=tweet_id)


# Like Post

@login_required
def like_tweet(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)
    liked = Like.objects.filter(tweet=tweet, user=request.user).exists()

    if liked:
        # Unlike the tweet
        Like.objects.filter(tweet=tweet, user=request.user).delete()
    else:
        # Like the tweet
        Like.objects.create(tweet=tweet, user=request.user)

    # Redirect back to the tweet_list page
    return redirect('tweet_list')