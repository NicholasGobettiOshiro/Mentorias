from django.db import models

# Create your models here.

class Disciplina(models.Model):
    disciplina = models.CharField(max_length = 50)
    def __str__(self):
        return self.disciplina

class Criar_mentoria(models.Model):
    def __str__(self):
        return str(self.id)
    class Meta:
        verbose_name = 'Criar mentoria'
        verbose_name_plural = 'Criar mentorias'

STATUS_DA_MENTORIA = (
    ('D', 'Disponível'),
    ('A', 'Agendada'),
)

class Mentoria(models.Model):
    data_e_horario = models.DateTimeField()
    disciplina = models.ManyToManyField(Disciplina)
    mentor = models.ForeignKey('auth.User', limit_choices_to = {'groups': 2}, editable = False, on_delete = models.PROTECT)
    mentor_email = models.CharField(max_length = 200, editable = False)
    mentorando = models.CharField(max_length = 200, editable = False, blank = True)
    status = models.CharField(max_length = 1, choices = STATUS_DA_MENTORIA, default = 'D', editable = False)
    criar_mentoria = models.ForeignKey(Criar_mentoria, editable = False, blank = True, null = True, on_delete = models.DO_NOTHING)