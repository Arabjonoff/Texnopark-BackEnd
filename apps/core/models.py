from django.db import models


class Theme(models.TextChoices):
    """Frontend rang sxemasi kaliti. Tailwind class'lari frontendda shu kalit bo'yicha tanlanadi."""

    BLUE = 'blue', "Ko'k"
    CYAN = 'cyan', 'Moviy'
    PURPLE = 'purple', 'Binafsha'
    YELLOW = 'yellow', 'Sariq'
    RED = 'red', 'Qizil'
    EMERALD = 'emerald', 'Zumrad'
    ORANGE = 'orange', "To'q sariq"


class Icon(models.TextChoices):
    """lucide-react ikonkalari. Yangi ikonka qo'shilsa frontenddagi components/ui/DynamicIcon.tsx ham yangilanadi."""

    SMARTPHONE = 'smartphone', 'Smartphone (mobil)'
    TERMINAL = 'terminal', 'Terminal (dasturlash)'
    LAYERS = 'layers', 'Layers (qatlamlar)'
    CPU = 'cpu', 'Cpu (elektronika)'
    BOX = 'box', 'Box (3D)'
    BRIEFCASE = 'briefcase', 'Briefcase (loyiha)'
    ROCKET = 'rocket', 'Rocket (startap)'
    ZAP = 'zap', 'Zap (energiya)'
    USERS = 'users', 'Users (jamoa)'
    TROPHY = 'trophy', 'Trophy (g\'alaba)'
    PRINTER = 'printer', 'Printer'
    MONITOR = 'monitor', 'Monitor (kompyuter)'
    HAMMER = 'hammer', 'Hammer (asboblar)'


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField('yaratilgan', auto_now_add=True)
    updated_at = models.DateTimeField('yangilangan', auto_now=True)

    class Meta:
        abstract = True


class PublishableModel(TimeStampedModel):
    """Admin'da yashirish/ko'rsatish va tartiblash mumkin bo'lgan kontent."""

    is_published = models.BooleanField("saytda ko'rsatilsin", default=True)
    order = models.PositiveIntegerField('tartib', default=0)

    class Meta:
        abstract = True
        ordering = ('order', 'id')
