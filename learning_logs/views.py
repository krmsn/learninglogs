from django.shortcuts import render, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def index(request):
    return render(request, 'learning_logs/index.html')


# Restrict access to anyone other than admin  with "@login_required"
# to get all topics
@login_required
def topics(request):
    # same as a "where" clause in a SQL statement
    # filters topics to only show topics that a user owns
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}

    return render(request, 'learning_logs/topics.html', context)


# Get individual topics
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id = topic_id)

    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added') # the "-" before date added translates to "descending."

    context = {'topic': topic, 'entries': entries}

    return render(request, 'learning_logs/topic.html', context)

### Test interview question

# If this is a "post" request,
@login_required
def new_topic(request):
    if request.method != "POST":
        form = TopicForm()
    else:
        form = TopicForm(data = request.POST)

        if form.is_valid():
            new_topic = form.save(commit = False)
            new_topic.owner = request.user
            new_topic.save()

            return redirect("learning_logs:topics")

    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id = topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data = request.POST)

        if form.is_valid():
            # When we call save(), we include the argument commit = False to tell Django to create
            # a new entry object and assign it to new_entry without saving it to the databse yet
            new_entry = form.save(commit = False)
            # Assign the topic of the new entry based on the topic we pulled from topic_id
            new_entry.topic = topic
            new_entry.save()
            form.save()
            return redirect("learning_logs:topic", topic_id = topic.id)

    context = {"form": form, "topic": topic}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id = entry_id)
    topic = entry.topic

    if topic.owner != request.user:
        raise Http404

    if request.method != "POST":
        form = EntryForm(instance = entry)
    else:
        form = EntryForm(instance = entry, data = request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic_id = topic.id)


    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)

