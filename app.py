import streamlit as st
import pickle
import re
import nltk 

knn = pickle.load(open('knn.pkl','rb'))
tdif = pickle.load(open('tdif.pkl','rb'))


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

#web application
def main():
    st.title('Resume Screamin App')
    upload_file = st.file_uploader('Upload Your Resume',type=['txt','pdf'])
    if upload_file is not None:
        try:
            resume_bytes = upload_file.read()
            resume_text =    resume_bytes.decode('utf-8')
        except UnicodeDecodeError:
            resume_text =    upload_file.read().decode('latin-1')
        
        clean_resume = cleanResume(resume_text)
        cleaned_resume = tdif.transform([clean_resume])
        pred = knn.predict(cleaned_resume)[0]
        category_name = category_mapping.get(pred, "Unknown")
        st.write("Predicted Category:", category_name)
        st.write(pred)



if __name__ == "__main__":
    main()



