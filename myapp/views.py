from django.shortcuts import render
from .forms import ResumeUploadForm
from django.contrib import messages
import streamlit as st
import pickle
import re
import nltk 
from django.http import  HttpResponse
# Create your views here.

import re
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)  
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText) 
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText
category_mapping = {
    15: "Java Developer",
    23: "Testing",
    8: "DevOps Engineer",
    20: "Python Developer",
    24: "Web Designing",
    12: "HR",
    13: "Hadoop",
    3: "Blockchain",
    10: "ETL Developer",
    18: "Operations Manager",
    6: "Data Science",
    22: "Sales",
    16: "Mechanical Engineer",
    1: "Arts",
    7: "Database",
    11: "Electrical Engineering",
    14: "Health and fitness",
    19: "PMO",
    4: "Business Analyst",
    9: "DotNet Developer",
    2: "Automation Testing",
    17: "Network Security Engineer",
    21: "SAP Developer",
    5: "Civil Engineer",
    0: "Advocate",
}

def index(request):
    knn = pickle.load(open('knn.pkl','rb'))
    tdif = pickle.load(open('tdif.pkl','rb'))
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = request.FILES['resume']
            try:
                resume_text = upload_file.read().decode('utf-8')
            except UnicodeDecodeError:
                resume_text = upload_file.read().decode('latin-1')
            
            clean_resume_text = cleanResume(resume_text)
            cleaned_resume = tdif.transform([clean_resume_text])
            pred = knn.predict(cleaned_resume)[0]
            category_name = category_mapping.get(pred, "Unknown")
            messages.success(request,' ')
            return render(request,'index.html', {'category_name':category_name ,'pred':pred })
    else:
        form = ResumeUploadForm()

    return render(request, 'index.html', {'form': form})
