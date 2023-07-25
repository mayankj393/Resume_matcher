import os
from processing import resume_matcher
from utils import file_utils
import numpy as np
import warnings
import pandas as pd

# Ignore all warnings
warnings.filterwarnings("ignore")

job_desc = "C:/Users/admin/Documents/resume_rating/Data/JobDesc/AI-ML Engineer.docx"
resume_loc="C:/Users/admin/Documents/NLP/Naive-Resume-Matching-master/Naive-Resume-Matching-master/Data/Resumes"
title=job_desc.split("/")
sub_title = title[-1].split(".")
print("Job Description: ", sub_title[0])
ab_path=[]
for res in os.listdir(resume_loc):
    fname=os.path.join(resume_loc,res)
    ab_path.append(fname)
#print(ab_path)
ndarray=np.asarray(ab_path)
resumes=np.asarray(ndarray)
print("Shape of job_desc array:", len(job_desc))
print("Shape of resumes array:", resumes.shape)

result = resume_matcher.process_files(job_desc,resumes)
data = pd.DataFrame(result)
data = data.rename(columns={0:'Resumes',1:'Percentage'})
print(data)
#for i in range(len(result)):
#    print(result[i])