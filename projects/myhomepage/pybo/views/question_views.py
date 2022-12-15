from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from PIL import Image, ImageFilter

from ..forms import QuestionForm
from ..models import Question


@login_required(login_url='common:login')
def question_create(request, check=None):
    check = None
    if request.method == 'POST':
        # request.POST를 인수로 QuestionForm을 생성할 경우에는
        # request.POST에 담긴 subject, content 값이 QuestionForm의 subject, content 속성에 자동으로 저장되어 객체가 생성
        form = QuestionForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=False는 임시 저장을 의미
            # question객체 리턴받음
            # image1 = form.
            # print(image1)
            question = form.save(commit=False)
            question.author = request.user
            # print(question.imgfile)
            # image1 = Image.open(question.imgfile)
            # image1 = image1.filter(ImageFilter.BLUR)
            # question.imgfile = image1.
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


@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')


@login_required(login_url='common:login')
def question_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        question.voter.add(request.user)
    return redirect('pybo:index')
