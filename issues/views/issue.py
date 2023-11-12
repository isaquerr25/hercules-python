import json
from django.http.request import QueryDict
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django_htmx.http import HttpResponseClientRefresh

from core.htmx import render_htmx, show_message
from core.typing import HttpRequest
from issues.models import History, Issue, Message
from users.decorators import login_required, project_required


@login_required
@project_required
def issue(request: HttpRequest, number: int):
    issue = get_object_or_404(
        Issue, project=request.selected_project.project, number=number
    )
    history = History.objects.filter(issue=issue).select_related(
        'assignment__user',
        'assignment__team',
        'message',
        'user',
    ).order_by("created_at")

    return render_htmx(
        request,
        "issues/issue.html",
        {
            "issue": issue,
            "history": history,
            "HistoryType": History.Type,
        },
    )


class Rename(View):
    @method_decorator(login_required)
    @method_decorator(project_required)
    def get(self, request: HttpRequest, number: int):
        issue = get_object_or_404(
            Issue, project=request.selected_project.project, number=number
        )

        can_rename = issue.created_by_id == request.user.pk  # type: ignore
        can_rename = can_rename or request.selected_project.can_rename_issues
        if not can_rename:
            return show_message(
                HttpResponseForbidden(),  # type: ignore
                "error",
                "Only the owner of a project can rename it.",
            )

        return render_htmx(
            request,
            "issues/issue.html",
            {
                "renaming": True,
                "issue": issue,
            },
        )

    @method_decorator(login_required)
    @method_decorator(project_required)
    def put(self, request: HttpRequest, number: int):
        issue = get_object_or_404(
            Issue, project=request.selected_project.project, number=number
        )

        can_rename = issue.created_by_id == request.user.pk  # type: ignore
        can_rename = can_rename or request.selected_project.can_rename_issues
        if not can_rename:
            return show_message(
                HttpResponseForbidden(),  # type: ignore
                "error",
                "Only the owner of a project can rename it.",
            )

        data = QueryDict(request.body, True)
        new_title = str(data.get("issue-title") or "")
        if not new_title:
            return show_message(
                HttpResponseBadRequest(),  # type: ignore
                "error",
                "The issue title can't be empty",
            )

        if issue.title != new_title:
            issue.title = new_title
            issue.save()

            History.objects.create(
                issue=issue,
                user=request.user,
                type=History.Type.TITLE,
                title=new_title,
            )

        return render_htmx(
            request,
            "issues/issue.html",
            {
                "issue": issue,
            },
        )


@login_required
@project_required
def comment(request: HttpRequest, number: int):
    issue = get_object_or_404(
        Issue, project=request.selected_project.project, number=number
    )
    comment_json = request.POST.get("comment")

    try:
        assert comment_json is not None
        comment: dict = json.loads(comment_json)
    except:
        return show_message(
            HttpResponseForbidden(),  # type: ignore
            "error",
            "The comment body is required.",
        )

    try:
        message = Message.objects.create(
            issue=issue,
            created_by=request.user,
            body=comment,
        )
        History.objects.create(
            issue=issue,
            user=request.user,
            type=History.Type.MESSAGE,
            message=message,
        )
    except:
        return show_message(
            HttpResponseForbidden(),  # type: ignore
            "error",
            "Server error",
        )

    return HttpResponseClientRefresh()
