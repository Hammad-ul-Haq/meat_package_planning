from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
def capacity(request):



    cap = pd.read_excel("files/Activities_adjust.xlsx", sheet_name='Activity Cap')
    cap_html= cap.to_html(classes='table',justify='left')
    context={
        "cap_html":cap_html,
        "active": "cap"
    }

    return render(request,'input_data/input_data.html',context)

def prodMeat(request):

    # Products and Meat Relationship Table
    ProdMeat = pd.read_excel("files/Activities.xlsx", sheet_name='Products and Meat')
    ProdMeat_html = ProdMeat.to_html(classes='table',justify='left')
    context={
        "cap_html":ProdMeat_html,
        "active": "prodmeat"
    }

    return render(request,'input_data/input_data.html',context)


def sequence(request):
    # Sequence table
    seq = pd.read_excel("files/Activities.xlsx", sheet_name='Product Seqeunce')
    seq_html = seq.to_html(classes='table',justify='left')
    context={
        "cap_html":seq_html,
        "active": "seq"
    }

    return render(request,'input_data/input_data.html',context)

def requirement(request):
    # Four Priority Requirement
    req = pd.read_excel("files/req wihtout byproducts.xlsx")
    req_html = req.to_html(classes='table',justify='left')
    context={
        "cap_html":req_html,
        "active": "req"
    }
    return render(request, 'input_data/input_data.html', context)

def meat(request):

    # Priority Meat Input
    # meat=pd.read_excel("Files/Meats.xlsx",  sheet_name ='Priority Meat Input') #delected the byproduct,
    meat = pd.read_excel("files/Meats_adjust_v3.xlsx", sheet_name='Priority Meat Input')  # delected the byproduct,
    meat_html = meat.to_html(classes='table',justify='left')
    context={
        "cap_html":meat_html,
        "active": "meat"
    }
    return render(request, 'input_data/input_data.html', context)

def meat_hourly(request):

    # Hourly Meat Input
    meat_hourly = pd.read_excel("files/hourly_meat_input.xlsx",index_col = 0)
    meat_hourly_html = meat_hourly.to_html(classes='table',justify='left')
    context={
        "cap_html":meat_hourly_html,
        "active": "meat_hourly"
    }
    return render(request, 'input_data/input_data.html',context)


