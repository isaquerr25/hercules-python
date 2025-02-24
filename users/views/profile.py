import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.http import require_POST, require_safe
from PIL import Image

from core.htmx import render_htmx, show_message
from core.typing import HttpRequest, HttpResponse
from users.decorators import login_required
from users.forms.edit import AlterProfileForm
from users.forms.picture import PictureForm


@login_required
@require_safe
def profile(request: HttpRequest):
    user_data_form = AlterProfileForm(instance=request.user)

    return render_htmx(
        request,
        "users/profile/profile.html",
        {
            "user_data_form": user_data_form,
        },
    )


@login_required
@require_POST
def upload_picture(request: HttpRequest):
    form = PictureForm(request.POST, request.FILES)
    if not form.is_valid():
        return show_message(
            HttpResponseBadRequest(),  # type: ignore
            "error",
            _("The uploaded file is not a valid image."),
        )

    picture = form.cleaned_data["picture"]

    request.user.picture = picture
    request.user.save()

    image = Image.open(request.user.picture.path)

    width, height = image.size
    size = min(image.size)
    xoffset = int((width - size) / 2)
    yoffset = int((height - size) / 2)

    image = image.crop(
        (
            xoffset,
            yoffset,
            xoffset + size,
            yoffset + size,
        )
    )

    image.save(request.user.picture.path)

    return render_htmx(request, "users/profile/picture-img.html", {"oob": True})


@login_required
@require_POST
def update_user_data(request: HttpRequest):
    form = AlterProfileForm(request.POST, instance=request.user)
    is_valid = form.is_valid()

    if is_valid:
        form.save()

    response = render_htmx(
        request,
        "users/profile/user-data.html",
        {
            "oob": is_valid,
            "form": form,
        },
    )

    if is_valid:
        response = show_message(response)

    return response


class ChangePassword(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest):
        response = render(
            request,
            "users/profile/change-password.html",
            {
                "form": PasswordChangeForm(request.user),
            },
        )

        response.headers["HX-Trigger"] = json.dumps(
            {"form:showModal": "#change-password-dialog"}
        )

        return response

    @method_decorator(login_required)
    def post(self, request: HttpRequest):
        form = PasswordChangeForm(request.user, data=request.POST)
        is_valid = form.is_valid()

        if is_valid:
            form.save()
            update_session_auth_hash(request, form.user)

            response = HttpResponse(b"")
            response.headers["HX-Trigger"] = json.dumps(
                {
                    "form:hideModal": "#change-password-dialog",
                },
            )

            return response

        return render(
            request,
            "users/profile/change-password.html",
            {
                "form": form,
            },
        )
