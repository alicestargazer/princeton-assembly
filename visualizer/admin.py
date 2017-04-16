from django.contrib import admin

# Register your models here.
from .models import Problem, Instruction, Register, Stack, Eflag, Rodata, Data, BSS, Text, Arg, Constant

class InstructionInLine(admin.TabularInline):
    model = Instruction
    fields = ['num', 'label', 'name', 'src', 'dest']
    extra = 0
class RegisterInLine(admin.TabularInline):
    model = Register
    fields = ['name', 'content']
    classes = ['collapse']
    extra = 0
class StackInLine(admin.TabularInline):
    model = Stack
    fields = ['name', 'val']
    extra = 0
class EflagInLine(admin.TabularInline):
    model = Eflag
    fields = ['cf', 'zf', 'sf', 'of']
    extra = 0
class RodataInLine(admin.TabularInline):
    model = Rodata
    fields = ['val', 'name', 'label']
    extra = 0
class DataInLine(admin.TabularInline):
    model = Data
    fields = ['val', 'name', 'label']
    extra = 0
class BSSInLine(admin.TabularInline):
    model = BSS
    fields = ['val', 'name', 'label']
    extra = 0
class TextInLine(admin.TabularInline):
    model = Text
    fields = ['val']
    extra = 0
class ArgInLine(admin.TabularInline):
    model = Arg
    fields = ['name', 'addr', 'val', 'text']
    extra = 0
class ConstantInLine(admin.TabularInline):
    model = Constant
    fields = ['label', 'val']
    extra = 0
class ProblemAdmin(admin.ModelAdmin):
    fields = ['number', 'steps', 'current_line', 'filename', 'ccode', 'stdout']
    list_display = ('number', 'steps', 'current_line', 'filename', 'ccode', 'stdout',)
    inlines = [InstructionInLine, RegisterInLine, StackInLine, EflagInLine, RodataInLine, DataInLine, BSSInLine, TextInLine, ArgInLine, ConstantInLine]
class InstructionAdmin(admin.ModelAdmin):
    fields = ['num', 'label', 'name', 'src', 'dest']
    list_display = ('num', 'label', 'name', 'src', 'dest',)
class RegisterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': ['name', 'problem']}),
        ('Register Contents', {'fields': ['content']}),
    ]
    list_display = ('name', 'content')
class StackAdmin(admin.ModelAdmin):
    fields = ['name', 'val']
    list_display = ('name', 'val',)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Instruction, InstructionAdmin)
admin.site.register(Register, RegisterAdmin)
admin.site.register(Stack, StackAdmin)
