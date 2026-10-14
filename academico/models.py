

# Create your models here.
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Carrera(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    duracion_semestres = models.PositiveSmallIntegerField(default=8)

    class Meta:
        verbose_name = "Carrera"
        verbose_name_plural = "Carreras"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Profesor(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    especialidad = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Estudiante(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    fecha_nacimiento = models.DateField()
    carrera = models.ForeignKey(
        Carrera,
        on_delete=models.PROTECT,
        related_name="estudiantes",
    )

    class Meta:
        verbose_name = "Estudiante"
        verbose_name_plural = "Estudiantes"
        ordering = ["apellido", "nombre"]

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Curso(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    creditos = models.PositiveSmallIntegerField(default=5)
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cursos",
    )
    # Relación muchos a muchos usando la tabla intermedia Inscripcion
    estudiantes = models.ManyToManyField(
        Estudiante,
        through="Inscripcion",
        related_name="cursos",
    )

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ["codigo"]

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Inscripcion(models.Model):
    ESTADOS = [
        ("CURSANDO", "Cursando"),
        ("APROBADO", "Aprobado"),
        ("REPROBADO", "Reprobado"),
        ("RETIRADO", "Retirado"),
    ]

    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    # Campos propios de la relación
    fecha_inscripcion = models.DateField(auto_now_add=True)
    nota_final = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(1.0), MaxValueValidator(7.0)],
    )
    estado = models.CharField(
        max_length=10, choices=ESTADOS, default="CURSANDO"
    )

    class Meta:
        verbose_name = "Inscripción"
        verbose_name_plural = "Inscripciones"
        # Un estudiante no puede inscribirse dos veces en el mismo curso
        constraints = [
            models.UniqueConstraint(
                fields=["estudiante", "curso"],
                name="unique_estudiante_curso",
            )
        ]

    def __str__(self):
        return f"{self.estudiante} en {self.curso}"