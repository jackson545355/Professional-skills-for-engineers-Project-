from django.shortcuts import render,get_object_or_404,redirect
from .models import Item
from django.contrib.auth.decorators import login_required
from .forms import NewItemForm,EditItemForm

# Create your views here.

def detail(request,pk):
    item = get_object_or_404(Item,pk=pk)
    ralated_items = Item.objects.filter(category = item.category,is_sold=False).exclude(pk=pk)[0:3]

    return render(request,'item/detail.html',{
        'item' : item,
        'ralated_items' : ralated_items
    })

@login_required
def new(request):
    if request.method == "POST":
        form = NewItemForm(request.POST,request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            
            return redirect('item:detail',pk=item.id)
    else:
        form = NewItemForm()

    return render(request,'item/forms.html',{
        'form':form,
        'title':'New Item'
    })

@login_required
def edit(request,pk):
    item = get_object_or_404(Item,pk=pk,created_by=request.user)
    if request.method == "POST":
        form = EditItemForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            
            return redirect('item:detail',pk=item.id)
    else:
        form = NewItemForm(instance=item)

    return render(request,'item/forms.html',{
        'form':form,
        'title':'Edit Item'
    })

@login_required
def delete(request,pk):
    item = get_object_or_404(Item,pk=pk,created_by=request.user)
    item.delete()
    return redirect('dashboard:index')
