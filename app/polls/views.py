from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Poll, Question, Choice, UserResponse, Answer

from .services import get_sorted_by_ranks

# Create your views here.


@csrf_exempt
@login_required(login_url="/login")
def poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = list(Question.objects.filter(poll=poll))
    user_responses = UserResponse.objects.filter(poll=poll).filter(
        user_id=request.user.id
    )
    for user_resp in user_responses:
        user_answers = Answer.objects.filter(user_response=user_resp)
        for user_answer in user_answers:
            questions.remove(user_answer.question)

    if request.method == "POST":
        user_response, created = UserResponse.objects.get_or_create(
            poll=poll, user_id=request.user.id
        )
        for question in questions:
            choice_id = request.POST.get(f"question_{question.id}")
            if choice_id:
                choice = get_object_or_404(Choice, pk=choice_id)
                Answer.objects.create(
                    user_response=user_response, question=question, choice=choice
                )
        return redirect("polls:poll_result", poll_id=poll_id)

    return render(request, "poll.html", {"poll": poll, "questions": questions})


@csrf_exempt
def poll_result(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    questions = Question.objects.filter(poll=poll)
    question_ranks = []
    question_stats = []
    for question in questions:
        answered_question = Answer.objects.filter(question=question)
        total_answered = len(answered_question)
        choice_stats = []
        question_user_stats = []
        for choice in question.choice_set.all():
            choice_answered = answered_question.filter(choice=choice)

            for user_choice in choice_answered:
                if user_choice.user_response.id not in question_user_stats:
                    question_user_stats.append(user_choice.user_response.user_id)

            if len(choice_answered) != 0 and total_answered != 0:
                choice_ratio = f"{round((len(choice_answered) / total_answered) * 100, 2)}% ({len(choice_answered)})"
            else:
                choice_ratio = 0
            choice_stats.append({"choice": choice.text, "ratio": choice_ratio})

        question_ranks.append({"question_id": question.id})
        question_stats.append(
            {
                "question": question.text,
                "total_answered": total_answered,
                "number": question.id,
                "choices": choice_stats,
            }
        )
    return render(
        request,
        "poll_result.html",
        {"poll": poll, "question_stats": get_sorted_by_ranks(question_stats)},
    )
