import re
from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import loader
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from .models import Problem, Instruction, Register, Stack, Eflag, Rodata, Data, BSS, Text, Arg, Constant
from .forms import AbsvalForm, PowerForm, UppercaseForm, RectForm

# User input views/forms
class HelloView(generic.DetailView):
    template_name = 'visualizer/user.html'
    model = Problem

    def get_context_data(self, **kwargs):
        context = super(HelloView, self).get_context_data(**kwargs)
        return context

class AbsvalView(generic.FormView):
    template_name = 'visualizer/user.html'
    form_class = AbsvalForm

    def get_context_data(self, **kwargs):
        context = super(AbsvalView, self).get_context_data(**kwargs)
        context['problem'] = Problem.objects.get(pk=int(self.kwargs['pk']))
        return context

    def form_valid(self, form):
        return super(AbsvalView, self).form_valid(form)

def absvalform(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'POST':
        form = AbsvalForm(request.POST)
        if form.is_valid():
            iInput_val = form.cleaned_data['iInput']
            a = Arg.objects.get(name="iInput", problem_id=problem_id)
            a.addr = '4000'
            a.val=iInput_val
            a.save()
            return HttpResponseRedirect(reverse('visualizer:visualizer', args=(problem_id, )))
    else:
        form = AbsvalForm()
    return render(request, 'visualizer/user.html', {'form':form});

class UppercaseView(generic.FormView):
    template_name = 'visualizer/user.html'
    form_class = UppercaseForm

    def get_context_data(self, **kwargs):
        context = super(UppercaseView, self).get_context_data(**kwargs)
        context['problem'] = Problem.objects.get(pk=int(self.kwargs['pk']))
        return context

    def form_valid(self, form):
        return super(UppercaseView, self).form_valid(form)

def uppercaseform(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'POST':
        form = UppercaseForm(request.POST)
        if form.is_valid(): # and input is a character **
            cInput_val = form.cleaned_data['cInput']
            a = Arg.objects.get(name="cInput", problem_id=problem_id)
            a.val=cInput_val
            a.save()
            return HttpResponseRedirect(reverse('visualizer:visualizer', args=(problem_id, )))
    else:
        form = UppercaseForm()
    return render(request, 'visualizer/user.html', {'form':form});

class RectView(generic.FormView):
    template_name = 'visualizer/user.html'
    form_class = RectForm

    def get_context_data(self, **kwargs):
        context = super(RectView, self).get_context_data(**kwargs)
        context['problem'] = Problem.objects.get(pk=int(self.kwargs['pk']))
        return context

    def form_valid(self, form):
        return super(RectView, self).form_valid(form)

def rectform(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'POST':
        form = RectForm(request.POST)
        if form.is_valid():
            iLength_val = form.cleaned_data['iLength']
            a = Arg.objects.get(name="iLength", problem_id=problem_id)
            a.val=iLength_val
            a.save()
            iWidth_val = form.cleaned_data['iWidth']
            a = Arg.objects.get(name="iWidth", problem_id=problem_id)
            a.val=iWidth_val
            a.save()
            return HttpResponseRedirect(reverse('visualizer:visualizer', args=(problem_id, )))
    else:
        form = RectForm()
    return render(request, 'visualizer/user.html', {'form':form});

class PowerView(generic.FormView):
    template_name = 'visualizer/user.html'
    form_class = PowerForm

    def get_context_data(self, **kwargs):
        context = super(PowerView, self).get_context_data(**kwargs)
        context['problem'] = Problem.objects.get(pk=int(self.kwargs['pk']))
        return context

    def form_valid(self, form):
        return super(PowerView, self).form_valid(form)

def powerform(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    if request.method == 'POST':
        form = PowerForm(request.POST)
        if form.is_valid():
            lBase_val = form.cleaned_data['lBase']
            a = Arg.objects.get(name="lBase", problem_id=problem_id)
            a.val=lBase_val
            a.save()
            lExp_val = form.cleaned_data['lExp']
            a = Arg.objects.get(name="lExp", problem_id=problem_id)
            a.val=lExp_val
            a.save()
            return HttpResponseRedirect(reverse('visualizer:visualizer', args=(problem_id, )))
    else:
        form = PowerForm()
    return render(request, 'visualizer/user.html', {'form':form});

# Page views
class IndexView(generic.ListView):
    template_name = 'visualizer/index.html'
    context_object_name = 'list_of_problems'

    def get_queryset(self):
        """Return the list of problems available."""
        return Problem.objects.all()

class VisualizerView(generic.DetailView):
    template_name = 'visualizer/visualizer.html'
    model = Problem
    # slug_field = 'filename'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(VisualizerView, self).get_context_data(**kwargs)
        # context['curr_instr'] = Stack.objects.all()
        # problem.register_set.values_list('reg_name', flat=True).distinct()
        return context

# Instruction Operands
def sal(suffix, reg, value):
    if suffix == "q":
        new_val = int(reg.content, 16) << int(value)
        reg.content = '%016x' % new_val
    elif suffix == "l":
        new_val = int(reg.content[8:], 16) << int(value)
        reg.content = "00000000" + '%08x' % new_val
    elif suffix == "w":
        new_val = int(reg.content[12:], 16) << int(value)
        reg.content = reg.content[0:12] + '%04x' % new_val
    elif suffix == "b":
        new_val = int(reg.content[14:], 16) << int(value)
        reg.content = reg.content[0:14] + '%02x' % new_val
    reg.save()

def sub(suffix, reg, value, p_id): #q, %rsp, $24 # hasn't been tested on l, w, b
    if suffix == 'q':
        byte = 8
        incr = value/8
        addr = reg.content
    elif suffix == "l":
        byte = 4
        incr = value/4
        addr = reg.fourByte
    elif suffix == "w":
        byte = 2
        incr = value/2
        addr = reg.twoByte
    elif suffix == "l":
        byte = 1
        incr = value/1
        addr = reg.oneByte
    for x in range(incr):
        # if does not already exist in the stack
        new_addr = int(addr) + byte
        s = Stack(name=hex(new_addr), problem_id=p_id)
        s.save()
        addr = new_addr
    if suffix == "q": reg.content = str(addr)
    elif suffix == "l": reg.fourByte = str(addr)
    elif suffix == "w": reg.twoByte = str(addr)
    elif suffix == "b": reg.oneByte = str(addr)

def cmp(suffix, reg, value, p_id):
    eflags = Eflag.objects.get(problem_id=p_id)
    if suffix == "q": dest = int(reg.content)
    elif suffix == "l": dest = int(reg.fourByte)
    elif suffix == "w": dest = int(reg.twoByte)
    elif suffix == "b": dest = int(reg.oneByte)
    if dest - value == 0:
        eflags.zf = True
        eflags.sf = False
    elif dest - value > 0:
        eflags.zf = False
        eflags.sf = False
    elif dest - value < 0:
        eflags.zf = False
        eflags.sf = True
    eflags.save()

def movsb(reg, value, problem): # sign extended mov
    if int(value) < 0:
        reg.content = hex((int(value) + (1 << 64)) % (1 << 64))[2:-1].upper()
    else:
        reg.content = '%016x' % int(value)
    reg.save()

def add(suffix, reg, value):
    if suffix == "q":
        new_val = int(reg.content, 16) + int(value)
        reg.content = '%016x' % new_val
    elif suffix == "l":
        new_val = int(reg.content[8:], 16) + int(value)
        reg.content = "00000000" + '%08x' % new_val
    elif suffix == "w":
        new_val = int(reg.content[12:], 16) + int(value)
        reg.content = reg.content[0:12] + '%04x' % new_val
    elif suffix == "b":
        new_val = int(reg.content[14:], 16) + int(value)
        reg.content = reg.content[0:14] + '%02x' % new_val
    reg.save()

def mov(suffix, reg, value, problem): #string(value)
    if suffix == "q":
        reg.content = '%016x' % int(value)
    elif suffix == "l":
        if int(value) < 0:
            reg.content = "00000000" + hex((int(value) + (1 << 32)) % (1 << 32))[2:].upper()
        else:
            reg.content = "00000000" + '%08x' % int(value)
    elif suffix == "w":
        reg.content = reg.content[0:12] + '%04x' % int(value)
    elif suffix == "b":
        reg.content = reg.content[0:14] + '%02x' % int(value)
    reg.save()

# Helper functions
def get_regname(partial):
    if 'e' in partial:
        regname = "%r"+partial[2:]
    elif partial.endswith('d') or partial.endswith('w') or partial.endswith('b'):
        regname = partial[:-1]
    elif partial.endswith('l') and len(partial) == 4:
        regname = "%r"+instr.dest[1:3]
    elif partial.endswith('l') and len(partial) == 3:
        regname = "%r"+partial[1]+"x"
    elif "r" not in partial:
        regname = "%r"+partial[1:]
    else:
        regname = partial
    return regname

def getVal(src, problem): # returns a string of an int or string of a hex
    if src.startswith("$"): # $0 or $someLabel -> returns "0" or "addr of someLabel as int"
        imm = src[1:]
        if imm.isdigit(): return imm
        else:
            if problem.constant_set.all().filter(label=imm).exists():
                constant = problem.constant_set.get(label=imm)
                return constant.val
            elif problem.rodata_set.all().filter(label=imm).exists():
                rod = problem.rodata_set.get(label=imm)
                return str(int(rod.name, 16))
            elif problem.data_set.all().filter(label=imm).exists():
                data = problem.data_set.get(label=imm)
                return str(int(data.name, 16))
            elif problem.bss_set.all().filter(label=imm).exists():
                bss = problem.bss_set.get(label=imm)
                return str(int(bss.name, 16))
            else: # $'\n'
                return str(ord('\n'))
    elif src.startswith("%"): # %eax
        if 'e' in src:
            regname = "%r"+src[2:]
            sec = 4
        elif src.endswith('d'):
            regname = src[:-1]
            sec = 4
        elif src.endswith('w'):
            regname = src[:-1]
            sec = 2
        elif src.endswith('b'):
            regname = src[:-1]
            sec = 1
        elif src.endswith('l') and len(src) == 4:
            regname = "%r"+src[1:3]
            sec = 1
        elif src.endswith('l') and len(src) == 3:
            regname = "%r"+src[1]+"x"
            sec = 1
        elif "r" not in src:
            regname = "%r"+src[1:]
            sec = 2
        else:
            regname = src
            sec = 8
        reg = problem.register_set.get(name=regname)
        if sec == 8:
            return reg.content
        elif sec == 4:
            return reg.content[8:]
        elif sec == 2:
            return reg.content[12:]
        else:
            return reg.content[14:]
    else: # iInput, i(%rax)
        if "(" not in src: # mov cChar %edi
            if problem.bss_set.all().filter(label=src).exists():
                bss = problem.bss_set.get(label=src)
                return bss.val
            elif problem.data_set.all().filter(label=src).exists():
                data = problem.data_set.get(label=src)
                return data.val
        else: # FIX # mov 4(%eax) %edi
            content = getMem(src, problem)

def getMem(name, problem): # returns correct address
    if name.count(',') == 2: #scaled indexed addressing
        arr = [name.split('(')[0]] + name.split('(')[1].split(')')[0].split(',')
        if arr[0] == "": base = 0
        else: base = int(arr[0])
        if arr[1] == "": regIndex = 0
        else: regIndex = getVal(problem.register_set.get(name=arr[1]))
        regScale = getVal(problem.register_set.get(name=arr[2]))
        scale = int(arr[3])
        mem = base + regIndex + (regScale * scale)
    elif name.count(',') == 1: #indexed addressing
        arr = [name.split('(')[0]] + name.split('(')[1].split(')')[0].split(',')
        if arr[0] == "": base = 0
        else: base = int(arr[0])
        regIndex = getVal(problem.register_set.get(name=arr[1]))
        regScale = getVal(problem.register_set.get(name=arr[2]))
        mem = base + regIndex + regScale
    else:
        arr = [name.split('(')[0]] + [name.split('(')[1].split(')')[0]]
        if arr[0] == "": base = 0
        else: base = int(arr[0])
        regIndex = getVal(problem.register_set.get(name=arr[1]))
        mem = base + regIndex
    return mem

def setMem(value, dest, problem):
    if "(" not in dest: # movl %eax iAbsVal
        if problem.bss_set.all().filter(label=dest).exists():
            bss = problem.bss_set.get(label=dest)
            bss.val=value
            bss.save()
        elif problem.data_set.all().filter(label=dest).exists():
            data = problem.data_set.get(label=dest)
            data.val=value
            data.save()
    else:
        content = getMem(dest, problem)
        if "mov" in name:
            val = getVal(src)
            for addr in problem.stack_set.all():
                if int(addr.name, 16) == content:
                    addr.val = val
                    addr.save()

def animate(request, problem_id, instruction_id):
    problem = get_object_or_404(Problem, pk=problem_id)
    curr_num = int(request.POST['instruction'].split('#')[1])
    curr_instruction = problem.instruction_set.get(num=curr_num)
    eflags = problem.eflag_set.get(problem_id=problem_id)
    name = curr_instruction.name # mov
    suffix = name[-1:] # q
    src = curr_instruction.src # $0
    dest = curr_instruction.dest # %eax
    if curr_instruction.label: someLabel = curr_instruction.label # someLabel
    if name == "call":
        if src == "printf":
            rdi_addr = getVal("%rdi", problem)
            if int(rdi_addr, 16) >= int('0x2000', 16) and int(rdi_addr, 16) < int('0x3000', 16):
                string = problem.rodata_set.get(name=hex(int(rdi_addr, 16))[2:])
            if problem.register_set.all().filter(name="%rsi").exists():
                rsi = getVal("%rsi", problem)
            if problem.register_set.all().filter(name="%rdx").exists():
                rdx = getVal("%rdx", problem)
            if problem.register_set.all().filter(name="%rcx").exists():
                rcx = getVal("%rcx", problem)
            total_cnt = string.val.count("%d") + string.val.count("%ld")
            if total_cnt == 0:
                output = string.val[1:-1]
            elif total_cnt == 1:
                output = string.val[1:-1] % int(rsi, 16)
            elif total_cnt == 2:
                output = string.val[1:-1] % (int(rsi, 16), int(rdx, 16))
            elif total_cnt == 3:
                output = string.val[1:-1] % (int(rsi, 16), int(rdx, 16), int(rcx, 16))
            rax = problem.register_set.get(name="%rax")
            problem.stdout = problem.stdout + output
            mov("l", rax, str(len(output)-2), problem)
        elif src == "scanf": #fix
            rdi_addr = getVal("%rdi", problem) # 202a
            rsi_addr = getVal("%rsi", problem) # 3000
            output_var= problem.arg_set.get(addr=hex(int(rsi_addr, 16))[2:])
            b = problem.bss_set.get(name=hex(int(rsi_addr, 16))[2:])
            b.val = output_var.val
            b.save()
            rax = problem.register_set.get(name="%rax")
            problem.stdout = problem.stdout + str(output_var.val) + "\n"
            mov("l", rax, "1", problem)
        elif src == "abs":
            edi_val = getVal("%edi", problem)
            x = int(edi_val, 16)
            if x > 0x7FFFFFFF:
                x -= 0x100000000
            abs_val = str(abs(x))
            rax = problem.register_set.get(name="%rax")
            mov("l", rax, abs_val, problem)
        elif src == "getchar":
            char = problem.arg_set.get(name="cInput")
            stdin = char.val
            problem.stdout = problem.stdout + str(char.val) + "\n"
            rax = problem.register_set.get(name="%rax")
            mov("l", rax, str(ord(stdin)), problem)
        elif src == "putchar": # int putchar(int char)
            edi = getVal("%edi", problem) # int char
            char_val = chr(int(edi, 16)) # output character
            problem.test = char_val
            problem.stdout = problem.stdout + char_val
            rax = problem.register_set.get(name="%rax")
            rdi = problem.register_set.get(name="%rdi")
            rax.content = rdi.content
            rax.save()
        next_line = curr_instruction.num + 1
    elif name == ".skip":
        if not problem.bss_set.all().filter(label=someLabel).exists() or  problem.bss_set.order_by("-name")[0].label == someLabel:
            mem = problem.bss_set.order_by("-name")[0]
            new_addr = int(mem.name, 16)+int(src)
            mem.label = someLabel
            mem.save()
            b = BSS(name=hex(new_addr)[2:], problem_id=problem_id, val=' ')
            b.save()
        next_line = curr_instruction.num + 1
    elif name == ".byte":
        if not problem.data_set.all().filter(label=someLabel).exists() or  problem.bss_set.order_by("-name")[0].label == someLabel:
            mem = problem.data_set.order_by("-name")[0]
            new_addr = int(mem.name, 16)+1
            mem.label = someLabel
            mem.val = int(src)
            mem.save()
            d = Data(name=hex(new_addr)[2:], problem_id=problem_id, val=' ')
            d.save()
        next_line = curr_instruction.num + 1
    elif name == ".quad":
        if not problem.data_set.all().filter(label=someLabel).exists() or  problem.bss_set.order_by("-name")[0].label == someLabel:
            mem = problem.data_set.order_by("-name")[0]
            new_addr = int(mem.name, 16)+8
            mem.label = someLabel
            mem.val = int(src)
            mem.save()
            d = Data(name=hex(new_addr)[2:], problem_id=problem_id, val=' ')
            d.save()
        next_line = curr_instruction.num + 1
    elif name == ".long":
        if not problem.data_set.all().filter(label=someLabel).exists() or  problem.bss_set.order_by("-name")[0].label == someLabel:
            mem = problem.data_set.order_by("-name")[0]
            new_addr = int(mem.name, 16)+4
            mem.label = someLabel
            mem.val = int(src)
            mem.save()
            d = Data(name=hex(new_addr)[2:], problem_id=problem_id, val=' ')
            d.save()
        next_line = curr_instruction.num + 1
    elif name == ".word":
        if not problem.data_set.all().filter(label=someLabel).exists() or  problem.bss_set.order_by("-name")[0].label == someLabel:
            mem = problem.data_set.order_by("-name")[0]
            new_addr = int(mem.name, 16)+2
            mem.label = someLabel
            mem.val = int(src)
            mem.save()
            d = Data(name=hex(new_addr)[2:], problem_id=problem_id, val=' ')
            d.save()
        next_line = curr_instruction.num + 1
    elif name == ".section":
        next_line = curr_instruction.num + 1
    elif name == ".string":
        rod = problem.rodata_set.order_by("-name")[0]
        new_addr = int(rod.name, 16)+len(src)
        rod.val=src
        rod.label=someLabel
        rod.save()
        r = Rodata(val=' ', problem_id=problem_id, name=hex(new_addr)[2:])
        r.save()
        next_line = curr_instruction.num + 1
    elif name == ".equ":
        c = Constant(problem_id=problem_id, label=src, val=dest)
        c.save()
        next_line = curr_instruction.num + 1
    elif "ret" in name:
        next_line = curr_instruction.num + 1
    elif "cmp" in name:
        srcVal = getVal(src, problem)
        eflags = Eflag.objects.get(problem_id=problem_id)
        destVal = getVal(dest, problem)
        if int(destVal, 16) - int(srcVal) == 0: # dest = src
            eflags.zf = 1
            eflags.sf = 0
            eflags.cf = 0
        elif int(destVal, 16) - int(srcVal) > 0: # dest > src
            eflags.zf = 0
            eflags.sf = 0
            eflags.cf = 1
        elif int(destVal, 16) - int(srcVal) < 0: # dest < src
            eflags.zf = 0
            eflags.sf = 1
            eflags.cf = 0
        eflags.save()
        next_line = curr_instruction.num + 1
    elif name.startswith("j"): # all jumps
        if name == "jg":
            if not (eflags.sf or eflags.of) and not eflags.zf:
                for instr in problem.instruction_set.all():
                    if instr.label == src:
                        next_line = instr.num
            else:
                next_line = curr_instruction.num + 1
        elif name == "jge":
            if not (eflags.sf or eflags.of):
                for instr in problem.instruction_set.all():
                    if instr.label == src:
                        next_line = instr.num
            else:
                next_line = curr_instruction.num + 1
        elif name == "jmp":
            for instr in problem.instruction_set.all():
                if instr.label == src:
                    next_line = instr.num
        else:
            next_line = curr_instruction.num + 1
        eflags.save()
    elif name == "imulq" and dest == "":
        srcVal = getVal(src, problem)
        raxVal = getVal("%rax", problem)
        new_val = int(raxVal, 16) * int(srcVal)
        octword = '%032x' % int(new_val)
        rdx = problem.register_set.get(name="%rdx")
        rdx.content = octword[0:16]
        rdx.save()
        rax = problem.register_set.get(name="%rax")
        rax.content = octword[16:32]
        rax.save()
        next_line = curr_instruction.num + 1
    elif "inc" in name:
        srcVal = getVal(src, problem)
        new_val = str(int(srcVal) + 1)
        setMem(new_val, src, problem)
        next_line = curr_instruction.num + 1
    elif src.startswith("$") and dest.startswith("%"): # immediate to register
        imm = getVal(src, problem)
        regname = get_regname(dest) # get r name
        reg = problem.register_set.get(name=regname)
        if "mov" in name:
            mov(suffix, reg, imm, problem)
        elif "add" in name and "sp" in dest: #deallocate stack <--- REFINE
            problem.stack_set.exclude(name="1000").delete()
        elif "add" in name:
            add(suffix, reg, imm)
        elif "sal" in name:
            sal(suffix, reg, imm)
        elif "sub" in name: #allocate stack
            sub(suffix, reg, imm, problem_id)
        elif "cmp" in name:
            cmp(suffix, reg, imm, problem_id)
        next_line = curr_instruction.num + 1
    elif src.startswith("$"): # immediate to memory
        imm = getVal(src, problem)
        if src[1:].isdigit(): # immediate is integer
            srcVal = src[1:]
        elif not src[1:].isdigit():
            if problem.constant_set.all().filter(label=src[1:]).exists():
                constant = problem.constant_set.get(label=src[1:])
                srcVal = constant.val
        if "mov" in name:
            if problem.bss_set.all().filter(label=dest).exists():
                bss = problem.bss_set.get(label=dest)
                bss.val = imm
                bss.save()
        elif "add" in name:
            if not src[1:].isdigit(): # immediate is integer
                if problem.bss_set.all().filter(label=dest).exists():
                    bss = problem.bss_set.get(label=dest)
                    new_val = int(bss.val)+int(imm)
                    bss.val=str(new_val)
                    bss.save()
        # mem = mem[content]
        next_line = curr_instruction.num + 1
    elif src.startswith("%") and dest.startswith("%"): # register to register
        regSrc = problem.register_set.get(name=src)
        reg = problem.register_set.get(name=dest)
        if "mov" in name:
            mov(suffix, reg, getVal(regSrc), problem)
        if "add" in name: #dest = dest + src
            add(suffix, reg, getVal(regSrc))
        next_line = curr_instruction.num + 1
    elif src.startswith("%"): # register to memory
        srcVal = int(getVal(src, problem), 16)
        setMem(srcVal, dest, problem)
        next_line = curr_instruction.num + 1
    elif dest.startswith("%"): # memory to register
        srcVal = getVal(src, problem) #"-5"
        regname = get_regname(dest)
        reg = problem.register_set.get(name=regname)
        if "movsb" in name:
            movsb(reg, srcVal, problem)
        elif "mov" in name:
            mov(suffix, reg, srcVal, problem)
        elif "add" in name:
            add(suffix, reg, srcVal)
        reg.save()
        next_line = curr_instruction.num + 1
    else:
        next_line = curr_instruction.num + 1
    problem.current_line = next_line
    problem.save()
    return HttpResponseRedirect(reverse('visualizer:visualizer', args=(problem.id, )))

def reset(request, problem_id):
    curr_pk = int(request.POST['reset'].split('#')[1])
    problem = get_object_or_404(Problem, pk=curr_pk)
    problem.current_line = 1
    problem.register_set.all().delete()
    for instr in problem.instruction_set.all(): # create register if not existing beforehand
        if instr.dest.startswith("%"):
            regname = get_regname(instr.dest)
            if not problem.register_set.all().filter(name=regname).exists():
                r = Register(name=regname, problem_id=curr_pk)
                r.save()
        if instr.src.startswith("%"):
            regname = get_regname(instr.src)
            if not problem.register_set.all().filter(name=regname).exists():
                r = Register(name=regname, problem_id=curr_pk)
                r.save()
    for reg in problem.register_set.all():
        if "sp" in reg.name: #set stack pointer to 0x400
            reg.content = str(int('1000', 16))
            reg.save()
        else:
            reg.content = "XXXXXXXXXXXXXXXX"
            reg.save()
    for instr in problem.instruction_set.all():
        if "sal" in instr.name and instr.src.startswith("$") and "rdi" in instr.dest:
            rdi = problem.register_set.get(name="%rdi")
            suffix = instr.name[-1:]
            if suffix == "q":
                rdi.content = str(0)
                rdi.save()
    problem.rodata_set.all().delete()
    r = Rodata(name="2000", problem_id=problem_id, val=' ')
    r.save()
    problem.data_set.all().delete()
    d = Data(name="3000", problem_id=problem_id, val=' ')
    d.save()
    problem.bss_set.all().delete()
    b = BSS(name="4000", problem_id=problem_id, val=' ')
    b.save()
    problem.text_set.all().delete()
    text=Text(problem_id=problem_id)
    text.save()
    problem.constant_set.all().delete()
    problem.stdout = ""
    problem.stack_set.all().delete()
    s = Stack(name="6000", problem_id=problem_id, val=' ')
    s.save()
    # problem.stack_set.get(name="1000").val = None
    eflags = problem.eflag_set.get(problem_id=problem_id)
    eflags.cf = False
    eflags.zf = False
    eflags.sf = False
    eflags.of = False
    eflags.save()
    problem.save()
    if curr_pk == 1:
        return HttpResponseRedirect(reverse('visualizer:hello', args=(problem.id, )))
    elif curr_pk == 2:
        return HttpResponseRedirect(reverse('visualizer:absval', args=(problem.id, )))
    elif curr_pk == 3:
        return HttpResponseRedirect(reverse('visualizer:uppercase', args=(problem.id, )))
    elif curr_pk == 4:
        return HttpResponseRedirect(reverse('visualizer:rect', args=(problem.id, )))
    elif curr_pk == 5:
        return HttpResponseRedirect(reverse('visualizer:power', args=(problem.id, )))
