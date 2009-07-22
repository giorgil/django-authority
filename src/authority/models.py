from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

from authority.managers import PermissionManager

class Permission(models.Model):
    """
    A granular permission model, per-object permission in other words.
    This kind of permission is associated with a user/group and an object
    of any content type.
    """
    codename = models.CharField(_('codename'), max_length=100)
    content_type = models.ForeignKey(ContentType, related_name="row_permissions")
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, null=True, blank=True, related_name='granted_permissions')
    group = models.ForeignKey(Group, null=True, blank=True)
    creator = models.ForeignKey(User, null=True, blank=True, related_name='created_permissions')

    approved = models.BooleanField(default=False)

    objects = PermissionManager()

    def __unicode__(self):
        return self.codename

    class Meta:
        unique_together = ("codename", "object_id", "content_type", "user", "group")
        verbose_name = _('permission')
        verbose_name_plural = _('permissions')
        permissions = (
            ('change_foreign_permissions', 'Can change foreign permissions'),
            ('delete_foreign_permissions', 'Can delete foreign permissions'),
            ('approve_permission_request', 'Can approve permission requests'),
        )


    def approve_perm_request(self, creator):
        """
        Approve granular permission request setting a Permission entry as
        approved=True for a specific action from an user on an object instance.
        """
        self.approved=True
        self.creator=creator
        self.save()
