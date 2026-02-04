import os
import pickle
import pandas as pd

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings

from .models import Prediction

BASE_DIR = settings.BASE_DIR

MODEL_PATH = os.path.join(BASE_DIR, 'ml_assets', 'job_fit_model.pkl')
FEATURES_PATH = os.path.join(BASE_DIR, 'ml_assets', 'job_fit_features.pkl')

model = None
feature_columns = None


def load_model():
    global model, feature_columns
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        with open(FEATURES_PATH, 'rb') as f:
            feature_columns = pickle.load(f)

        print("✅ ML Model Loaded")
    except Exception as e:
        print("❌ Model Load Error:", e)


load_model()




@login_required
def home(request):
    return render(request, 'predictor/home.html')


@login_required
def predict_job_fit(request):

    if model is None or feature_columns is None:
        messages.error(request, "ML Model not loaded. Contact Admin.")
        return redirect('home')

    if request.method == "POST":
        try:
            cgpa = float(request.POST['cgpa'])
            skills_score = int(request.POST['skills_score'])
            projects = int(request.POST['projects'])
            internship = int(request.POST['internship'])
            certifications = int(request.POST['certifications'])

            if not (5.0 <= cgpa <= 10.0):
                messages.error(request, "CGPA must be between 5 and 10")
                return redirect('predict')

            input_df = pd.DataFrame(
                [[cgpa, skills_score, projects, internship, certifications]],
                columns=feature_columns
            )

            prediction_value = model.predict(input_df)[0]

            pred = Prediction.objects.create(
                user=request.user,
                cgpa=cgpa,
                skills_score=skills_score,
                projects=projects,
                internship=internship,
                certifications=certifications,
                predicted_score=round(prediction_value, 2)
            )

            return render(request, 'predictor/result.html', {'prediction': pred})

        except Exception as e:
            messages.error(request, str(e))

    return render(request, 'predictor/predict.html')


@login_required
def prediction_history(request):
    predictions = Prediction.objects.filter(user=request.user)
    return render(request, 'predictor/history.html', {'predictions': predictions})
