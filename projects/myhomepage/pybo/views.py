from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question, Answer
from django.http import HttpResponseNotAllowed
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator

# Create your views here.
def index(request):
    page = request.GET.get('page', 1) # 페이지
    # 질문 목록 데이터 얻기
    question_list = Question.objects.order_by('-create_date')
    paginator = Paginator(question_list, 10) # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'pybo/question_detail.html', context)

def question_create(request):
    if request.method == 'POST':
        # request.POST를 인수로 QuestionForm을 생성할 경우에는
        # request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        form = QuestionForm(request.POST)
        if form.is_valid():
            # commit=False는 임시 저장을 의미
            # question객체 리턴받음
            question = form.save(commit=False)
            # create_date 설정. create_date 속성은 데이터 저장 시점에 생성해야 하는 값이므로 QuestionForm에 등록하여 사용하지 않는다.
            question.create_date = timezone.now()
            # form에 저장된 데이터로 Question 데이터를 저장하기 위한 코드
            # QuestionForm이 Question 모델과 연결된 모델 폼이기 때문에 이와 같이 사용할 수 있다.
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)
