from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login, authenticate, logout
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Folder
import json
from django.http import HttpResponse

User = get_user_model()

def index_view(request):
    return render(request, 'index.html')

def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Already registered, please login.')
            return redirect('login')
        else:
            user = User.objects.create_user(username=email, email=email, password=password)
            messages.success(request, 'Signup successful! Please login.')
            return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    context = {'timestamp': timezone.now().timestamp()}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('select')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'login.html', context)

@login_required
def select_view(request):
    return render(request, 'select.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def code_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'code.html')


@login_required
def create_view(request):
    folders = Folder.objects.filter(user=request.user)
    return render(request, 'create.html', {'folders': folders})

@login_required
def create_folder(request):
    if request.method == 'POST':
        folder_name = request.POST.get('folder_name')
        
        if folder_name:
            # ✅ Ensure same user can create multiple folders with different names
            folder, created = Folder.objects.get_or_create(user=request.user, name=folder_name)
            
            if created:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Folder already exists'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@login_required
def custom_view(request, folder_name):
    try:
        folder = Folder.objects.get(user=request.user, name=folder_name)
        return render(request, 'folder_template.html', {'folder': folder})
    except Folder.DoesNotExist:
        return HttpResponse("Folder not found", status=404)

@login_required
def custom_quiz_view(request, folder_name):
    try:
        folder = Folder.objects.get(user=request.user, name=folder_name)
        return render(request, 'custom.html', {'folder': folder})
    except Folder.DoesNotExist:
        return HttpResponse("Folder not found", status=404)
    






import json
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Quiz, Question, Folder
from django.contrib.auth.decorators import login_required

@login_required
def save_quiz(request):
    if request.method == "POST":
        data = json.loads(request.body)
        folder_name = data.get("folder_name")
        questions = data.get("questions", [])

        folder = get_object_or_404(Folder, name=folder_name, user=request.user)

        # ✅ Check if quiz already exists before creating a new one
        quiz, created = Quiz.objects.get_or_create(folder=folder, created_by=request.user)

        for q in questions:
            Question.objects.create(
                quiz=quiz,
                text=q["question"],
                options=json.dumps({"A": q["optionA"], "B": q["optionB"], "C": q["optionC"]}),  # ✅ Ensure JSON storage
                correct_option=q["correct"]
            )

        return JsonResponse({"success": True, "quiz_code": quiz.quiz_code})

import logging

logger = logging.getLogger(__name__)

@login_required
def save_quiz(request):
    logger.info(f"Received request with body: {request.body}")


import json
import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os

openai.api_type = "azure"
openai.api_base = "Enter your endpoint URL"
openai.api_key = os.getenv("Enter your API key)
openai.api_version = "2024-02-15-preview"

@csrf_exempt
def generate_questions(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            topic = data.get("topic")

            if not topic:
                return JsonResponse({"success": False, "error": "Topic is required."}, status=400)

            response = openai.ChatCompletion.create(
                engine="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that always responds with JSON."
                    },
                    {
                        "role": "user",
                        "content": (
                            f"Generate 10 multiple-choice quiz questions on the topic '{topic}'.\n"
                            "Each question must have 3 options and a correct answer (A, B, or C).\n"
                            "Respond ONLY in this exact JSON format:\n"
                            "[\n"
                            "  {\n"
                            "    \"question\": \"...\",\n"
                            "    \"options\": [\"Option A\", \"Option B\", \"Option C\"],\n"
                            "    \"correct\": \"A\"\n"
                            "  },\n"
                            "  ...\n"
                            "]"
                        )
                    }
                ]
            )

            return JsonResponse({"success": True, "questions": response["choices"][0]["message"]["content"]})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "error": "Invalid JSON input."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Only POST requests are allowed."}, status=405)
