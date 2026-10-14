
from django.contrib import admin
from .models import Carrera, Profesor, Estudiante, Curso, Inscripcion
  
  
# Inline: permite gestionar inscripciones dentro de la ficha de Curso o Estudiante
class InscripcionInline(admin.TabularInline):
 model = Inscripcion
 extra = 1
 fields = ('estudiante', 'curso', 'nota_final', 'estado')
 autocomplete_fields = ('estudiante', 'curso')
  
  
@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
 list_display = ('codigo', 'nombre', 'duracion_semestres')
 search_fields = ('codigo', 'nombre')
  
  
@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
 list_display = ('rut', 'nombre', 'apellido', 'email', 'especialidad')
 search_fields = ('rut', 'nombre', 'apellido')
 list_filter = ('especialidad',)
  
  
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
 list_display = ('rut', 'nombre', 'apellido', 'email', 'carrera')
 search_fields = ('rut', 'nombre', 'apellido')
 list_filter = ('carrera',)
 inlines = [InscripcionInline]
  
  
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
 list_display = ('codigo', 'nombre', 'creditos', 'profesor')
 search_fields = ('codigo', 'nombre')
 list_filter = ('profesor',)
 inlines = [InscripcionInline]
  
  
@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
 list_display = ('estudiante', 'curso', 'nota_final', 'estado', 'fecha_inscripcion')
 list_filter = ('estado', 'curso')
 search_fields = ('estudiante__nombre', 'estudiante__apellido', 'curso__nombre')
 list_editable = ('nota_final', 'estado')
 autocomplete_fields = ('estudiante', 'curso')