from django.db import models
from django.utils.translation import gettext_lazy as _
from django_stubs_ext.db.models import TypedModelMeta


class Role(models.IntegerChoices):
    OWNER = 1, _("Owner")
    MANAGER = 2, _("Manager")
    DEVELOPER = 3, _("Developer")
    TESTER = 4, _("Tester")


class Project(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.TextField(verbose_name=_("Name"))

    def try_delete(self) -> tuple[bool, str]:
        try:
            self.delete()
        except Exception as e:
            return False, repr(
                e
            )  # TODO: Treat possible reasons and return meaningful messages

        return True, ""


class ProjectMember(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    role = models.IntegerField(choices=Role.choices, default=Role.DEVELOPER)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

    class Meta(TypedModelMeta):
        constraints = [
            models.UniqueConstraint(
                fields=["project", "user"],
                name="unique_project_member",
            ),
        ]


class Team(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.TextField(verbose_name=_("Name"))

    def try_delete(self) -> tuple[bool, str]:
        try:
            self.delete()
        except Exception as e:
            return False, repr(
                e
            )  # TODO: Treat possible reasons and return meaningful messages

        return True, ""


class TeamMember(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    member = models.ForeignKey(ProjectMember, on_delete=models.CASCADE)

    class Meta(TypedModelMeta):
        constraints = [
            models.UniqueConstraint(
                fields=["team", "member"],
                name="unique_team_member",
            ),
        ]
