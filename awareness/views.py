from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Choice, Attempt, Answer
from .forms import TFForm, MCQForm, NameForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import random

def home(request):
    total_attempts = Attempt.objects.count()
    total_users = Attempt.objects.values('user').distinct().count()
    return render(request, 'awareness/home.html', {
        'total_attempts': total_attempts,
        'total_users': total_users
    })

def theory(request):
    return render(request, 'awareness/theory.html')

def contacts(request):
    return render(request, 'awareness/contacts.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .models import Question, Choice, Attempt, Answer
from .forms import TFForm, MCQForm
import random

# Головна сторінка
def home(request):
    total_attempts = Attempt.objects.count()
    total_users = Attempt.objects.values('user').distinct().count()
    return render(request, 'awareness/home.html', {
        'total_attempts': total_attempts,
        'total_users': total_users
    })

# Теоретичний матеріал
def theory(request):
    return render(request, 'awareness/theory.html')

# Контакти
def contacts(request):
    return render(request, 'awareness/contacts.html')

# Реєстрація користувача
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('awareness:home')
    else:
        form = UserCreationForm()
    return render(request, 'awareness/signup.html', {'form': form})

# Результати останніх 50 спроб
@login_required
def results(request):
    attempts = Attempt.objects.order_by('-created_at')[:50]
    return render(request, 'awareness/results.html', {'attempts': attempts})

# Початок тесту
@login_required
def quiz_start(request):
    qs = list(Question.objects.all())
    if not qs:
        return render(request, 'awareness/empty_quiz.html')

    selected = random.sample(qs, min(10, len(qs)))
    request.session['quiz_qids'] = [q.id for q in selected]
    request.session['quiz_index'] = 0
    request.session['quiz_score'] = 0
    request.session['quiz_answers'] = {}
    request.session.modified = True
    return redirect('awareness:quiz_question')

# Питання тесту
@login_required
def quiz_question(request):
    ids = request.session.get('quiz_qids')
    if not ids:
        return redirect('awareness:home')

    idx = request.session.get('quiz_index', 0)
    if idx >= len(ids):
        # Завершення тесту
        score = request.session.get('quiz_score', 0)
        total = len(ids)
        percent = round(score / total * 100, 2) if total > 0 else 0.0

        attempt = Attempt.objects.create(user=request.user, score=score, total=total, percent=percent)

        # Зберігаємо відповіді
        answers = request.session.get('quiz_answers', {})
        for qid, ans in answers.items():
            q = Question.objects.get(id=int(qid))
            if q.qtype == Question.TYPE_MCQ:
                choice_obj = Choice.objects.filter(id=int(ans)).first()
                Answer.objects.create(attempt=attempt, question=q, selected_choice=choice_obj)
            else:
                tf_val = True if ans == 'True' else False
                Answer.objects.create(attempt=attempt, question=q, tf_answer=tf_val)

        # Очищуємо сесію
        for key in ['quiz_qids', 'quiz_index', 'quiz_score', 'quiz_answers']:
            request.session.pop(key, None)
        request.session.modified = True

        return redirect('awareness:quiz_result_detail', attempt_id=attempt.id)

    # Поточне питання
    q = Question.objects.get(id=ids[idx])
    if q.qtype == Question.TYPE_MCQ:
        form = MCQForm(choices_list=[(c.id, c.text) for c in q.choices.all()])
    else:
        form = TFForm()

    if request.method == 'POST':
        if q.qtype == Question.TYPE_MCQ:
            form = MCQForm(request.POST, choices_list=[(c.id, c.text) for c in q.choices.all()])
            if form.is_valid():
                choice_id = int(form.cleaned_data['choice'])
                choice_obj = Choice.objects.filter(id=choice_id).first()
                if choice_obj and choice_obj.is_correct:
                    request.session['quiz_score'] += 1
                request.session['quiz_answers'][str(q.id)] = choice_id
                request.session['quiz_index'] += 1
                request.session.modified = True
                return redirect('awareness:quiz_question')
        else:
            form = TFForm(request.POST)
            if form.is_valid():
                ans = form.cleaned_data['choice']  # <-- виправлено
                correct = bool(q.tf_correct_answer)
                if (ans == 'True' and correct) or (ans == 'False' and not correct):
                    request.session['quiz_score'] += 1
                request.session['quiz_answers'][str(q.id)] = ans
                request.session['quiz_index'] += 1
                request.session.modified = True
                return redirect('awareness:quiz_question')

    return render(request, 'awareness/quiz.html', {
        'question': q,
        'form': form,
        'index': idx + 1,
        'total': len(ids)
    })

# Деталі результату
@login_required
def quiz_result_detail(request, attempt_id):
    attempt = get_object_or_404(Attempt, id=attempt_id)
    answers = attempt.answers.select_related('question', 'selected_choice').all()
    return render(request, 'awareness/quiz_result_detail.html', {
        'attempt': attempt,
        'answers': answers
    })

# Логаут
def logout_view(request):
    logout(request)
    return redirect('awareness:home')

