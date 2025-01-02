from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from .decorators import unauthenticated_user,allowed_users
from django.template.loader import get_template
from xhtml2pdf import pisa
# Create your views here.
@allowed_users(allowed_roles=['ADMIN'])
def thatpdf(request):
    lima = Wakulima.objects.all()
    template = get_template('farmers/repo.html')
    content = template.render({'lima':lima})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(content.encode("ISO-8859-1")),result)
    if not pdf.err:
        return HttpResponse(result.getvalue(),content_type='application/pdf')

def index(request):
    return render(request, 'farmers/index.html')
@login_required
@allowed_users(allowed_roles=['ADMIN'])
def crops(request):
    crops = Crop.objects.order_by('date_added')
    context = {'crops': crops}
    return render(request, 'farmers/crops.html', context)
    

@login_required 
@allowed_users(allowed_roles=['ADMIN'])  
def wakulima(request):
    if request.method == 'POST':
        form = WakulimaForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('farmers:wakulima')
    else:
        form = WakulimaForm()

    return render(request, 'farmers/wakulima.html', {'form':form})

def news(request):
    posts = Post.objects.all()

    return render(request, 'farmers/news.html',{'posts':posts})

def post_detail(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

            return redirect('farmers:post_detail', slug=post.slug)

    else:
        form = CommentForm()

    return render(request, 'farmers/post_detail.html',{'post':post, 'form':form})

def contact(request):
    if request.method=="POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subcounty = request.POST.get('subcounty')
        location = request.POST.get('location')
        subject = request.POST.get('subject')
        contact.name=name
        contact.email=email
        contact.subcounty=subcounty
        contact.location=location
        contact.subject=subject
        contact.save()
        #return HttpResponse("<h1>THANKS FOR CONTACTING US")
    return render(request, 'farmers/contact.html')


@login_required
def crop(request, crop_id):
    """ show a single crop and all its entries."""
    crop = Crop.objects.get(id=crop_id)
    entries = crop.entry_set.order_by('-date_added')
    context = {'crop': crop, 'entries': entries}

    return render(request, 'farmers/crop.html', context)
@login_required
def new_crop(request):
    """ Add a new crop. """
    #if crop.owner != request.user:
        #raise Http404
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = CropForm()
    else:
        # POST data submitted; process data
        form = CropForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmers:crops')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'farmers/new_crop.html', context)
@login_required
def new_entry(request, crop_id):
    """ Add a new entry for a particular crop."""
    crop = Crop.objects.get(id=crop_id)

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.crop = crop
            new_entry.save()
            return redirect('farmers:crop', crop_id=crop_id)

    # Display a blank or invalid form.
    context = {'crop': crop, 'form': form}
    return render(request, 'farmers/new_entry.html', context)
@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    crop = entry.crop

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('farmers:crop', crop_id=crop.id)

    context = {'entry': entry, 'crop': crop, 'form':form}
    return render(request, 'farmers/edit_entry.html', context)

