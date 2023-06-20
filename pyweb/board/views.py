from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from board.models import Question
from board.forms import QuestionForm, AnswerForm


def index(request):
    return render(request, 'board/index.html')      # import
    # return HttpResponse("<h1>웹 메인페이지 입니다.</h1>")


def question_list(request):
    question_list = Question.objects.all()      # import
    context = {'question_list': question_list}
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'board/detail.html', context)


# 질문 등록
def question_create(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)   # 입력된 데이터가 있는 폼
        if form.is_valid():     # 폼이 유효성 검사를 통과했다면
            question = form.save(commit=False)      # 가저장(날짜가 없음)
            question.create_date = timezone.now()   # 등록일 생성    # import
            form.save()     # 실제저장
            return redirect('board:quesiton_list')     # 질문 목록 페이지 이동  # import # 콜론 뒤에 띄어쓰면 안됨
    else:
        form = QuestionForm()   # 폼 객체 생성(빈 폼)   # import
    context = {'form': form}
    return render(request, 'board/question_form.html', context)  # get 방식


# 답변 등록
def answer_create(request, question_id):
    # 질문이 1개 지정되어야 답변을 등록할 수 있음
    question = Question.objects.get(id=question_id)
    if request.method == "POST":    # 소문자(post)이면 답변이 등록되지 않음
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)        # content만 저장
            answer.create_date = timezone.now()     # 답변등록일
            answer.question = question  # 외래키 생성
            form.save()
            return redirect('board:detail', question_id=question.id)    # question.id 주의
    else:
        form = AnswerForm()     # 빈 폼 생성
    context = {'question': question, 'form': form}
    return render(request, 'board/detail.html', context)

