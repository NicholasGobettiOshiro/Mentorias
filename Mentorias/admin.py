from django.contrib import admin
from .models import *
from django.core.mail import send_mail

# Register your models here.

admin.site.site_title = 'Mentorias'

admin.site.disable_action('delete_selected')

admin.site.register(Disciplina)

class MentoriaAdmin(admin.ModelAdmin):
    list_display = ['data_e_horario', 'disciplinas', 'mentor', 'mentorando', 'status']
    search_fields = ['id', 'data_e_horario', 'disciplina__disciplina', 'mentor__first_name', 'mentor__last_name', 'mentorando', 'status']
    list_filter = ['data_e_horario', 'disciplina', 'mentor', 'status']
    actions = ['cancelar']
    date_hierarchy = 'data_e_horario'

    def disciplinas(self, obj):
        return ",\n".join([d.disciplina for d in obj.disciplina.all()])

    def save_model(self, request, obj, form, change):
        obj.mentor = request.user
        obj.mentor_email = request.user.email
        obj.save()

    # def agendar(self, request, queryset):
    #     mensagem = 'Detalhes da mentoria:\nMentor: ' + str(queryset.get(mentor)) + '\nMentorando: ' + request.user + '\nQuando: ' + str(data_e_horario)
    #     if send_mail('Mentoria agendada: ' + str(data_e_horario), mensagem, 'nicholasgobetti0@hotmail.com', [request.user.email, mentor_email]) == 1:
    #         rows_updated = queryset.update(status = 'A')
    #         queryset.update(mentorando = str(request.user))
    #         if rows_updated == 1:
    #             message_bit = '1 mentoria foi agendada.'
    #         else:
    #             message_bit = '%s mentorias foram agendadas.' % rows_updated
    #     else:
    #             message_bit = 'Ocorreu um erro durante o envio de e-mail. Se seu endereço de e-mail está correto, mande uma mensagem para +55 13 99666-3591 ou nicholasgobetti0@hotmail.com'
    #     self.message_user(request, message_bit)
    #     agendar.short_description = 'Agendar mentoria(s).'

    def cancelar(self, request, queryset):
        rows_updated = queryset.update(status = 'D')
        if rows_updated == 1:
            message_bit = '1 mentoria foi cancelada.'
        else:
            message_bit = '%s mentorias foram canceladas' % rows_updated
        self.message_user(request, message_bit)
        cancelar.short_description = 'Cancelar mentoria(s).'

admin.site.register(Mentoria, MentoriaAdmin)

class MentoriaInline(admin.TabularInline):
    model = Mentoria
    extra = 3

class Criar_mentoriaAdmin(admin.ModelAdmin):
    inlines = [MentoriaInline]
    def save_formset(self, request, form, formset, change):
        for form in formset.forms:
            form.instance.mentor = request.user
        formset.save()

admin.site.register(Criar_mentoria, Criar_mentoriaAdmin)