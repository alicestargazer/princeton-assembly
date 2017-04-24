from __future__ import unicode_literals

from django.db import models

class Problem(models.Model):
    number = models.IntegerField() # 1, 2, 3
    steps = models.IntegerField()
    current_line = models.IntegerField(default=1)
    filename = models.CharField(max_length=50, blank=True)
    stdout = models.TextField(blank=True)
    ccode = models.TextField(blank=True)
    test = models.CharField(max_length=50, blank=True)
    # slug = models.SlugField(unique=True)
    #
    # @models.permalink
    # def get_absolute_url(self):
    #     return 'blog:post', (self.slug,)
    class Meta:
        ordering = ['id']
    def __str__(self):
        problem_name="Problem #{0}".format(str(self.number))
        return problem_name
    def prev_instruction(self):
        if self.current_line != 1:
            return self.instruction_set.get(num=self.current_line-1)
    def current_instruction(self):
        return self.instruction_set.get(num=self.current_line)
    def id_lowest_text(self):
        text = self.text_set.order_by("id")[0]
        return text.id
    def id_lowest_rodata(self):
        rod = self.rodata_set.order_by("id")[0]
        return rod.id
    def id_lowest_data(self):
        data = self.data_set.order_by("id")[0]
        return data.id
    def id_lowest_bss(self):
        bss = self.bss_set.order_by("id")[0]
        return bss.id
    def id_lowest_stack(self):
        stack = self.stack_set.order_by("id")[0]
        return stack.id
    def stdin_label(self):
        rdi = self.register_set.get(name="%rsi")
        b = self.bss_set.get(name=hex(int(rdi.content, 16))[2:])
        return b.label


# how to deal with different data types of each register???? <----------
class Register(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # rax, rdx
    content = models.CharField(max_length=50, blank=True, null=True) # all 8 bytes

    def __str__(self):
        return self.name

    def get_other_names(self):
        other_names = []
        if self.name.endswith("x") or self.name.endswith("i") or self.name.endswith("p"):
            if self.name.endswith("x"):
                byte_version = "%{0}".format(self.name[2:]).replace("x", "l")
            else:
                word = "%{0}".format(self.name[2:])
                byte_version = "{0}l".format(word)
            long_version = self.name.replace("r","e")
            word_version = "%{0}".format(self.name[2:])
        else:
            long_version = "{0}d".format(self.name)
            word_version = "{0}w".format(self.name)
            byte_version = "{0}b".format(self.name)
        other_names.append(long_version)
        other_names.append(word_version)
        other_names.append(byte_version)
        return other_names

    def getType(self):
        if "sp" in self.name: return "Stack Pointer"
        elif "a" in self.name: return "Return Value"
        elif "b" in self.name or "12" in self.name or "13" in self.name or "14" in self.name or "15" in self.name: return "Callee Saved"
        elif "di" in self.name: return "1st argument"
        elif "si" in self.name: return "2nd argument"
        elif "d" in self.name: return "3rd argument"
        elif "c" in self.name: return "4th argument"
        elif "8" in self.name: return "5th argument"
        elif "9" in self.name: return "6th argument"
        else: return "Caller Saved"

    def eightByte(self):
        if "X" in self.content:
            return "XXXXXXXX"
        else:
            hexed = self.content[0:8]
            return hexed

    def fourByte(self):
        if "X" in self.content[8:]:
            return "XXXX"
        else:
            hexed = self.content[8:12]
            return hexed

    def twoByte(self):
        if "X" in self.content[12:]:
            return "XX"
        else:
            hexed = self.content[12:14]
            return hexed

    def oneByte(self):
        if "X" in self.content[14:]:
            return "XX"
        else:
            hexed = self.content[14:16]
            return hexed

    def eightVal(self):
        if self.content.startswith("X"):
            return "X"
        else:
            x = int(self.content,16)
            if x > 0x7FFFFFFF:
                x -= 0x100000000
            return x

    def fourVal(self):
        four = self.content[8:]
        if four.startswith("X"):
            return "X"
        else:
            x = int(four,16)
            if x > 0x7FFFFFFF:
                x -= 0x100000000
            return x

    def twoVal(self):
        two = self.content[12:]
        if two.startswith("X"):
            return "X"
        else:
            x = int(two,16)
            if x > 0x7FFFFFFF:
                x -= 0x100000000
            return x

    def oneVal(self):
        one = self.content[14:]
        if one.startswith("X"):
            return "X"
        else:
            x = int(one,16)
            if x > 0x7FFFFFFF:
                x -= 0x100000000
            return x

    def is_stack_pointer(self):
        return "sp" in self.name

    def is_return(self):
        return "rax" in self.name or "eax" in self.name

    def longName(self):
        if self.name.endswith("x") or self.name.endswith("i") or self.name.endswith("p"):
            long_version = self.name.replace("r","e")
        else:
            long_version = "{0}d".format(self.name)
        return long_version

    def wordName(self):
        if self.name.endswith("x") or self.name.endswith("i") or self.name.endswith("p"):
            word_version = "%{0}".format(self.name[2:])
        else:
            word_version = "{0}w".format(self.name)
        return word_version

    def byteName(self):
        if self.name.endswith("x"):
            byte_version = "%{0}".format(self.name[2:]).replace("x", "l")
        elif self.name.endswith("i") or self.name.endswith("p"):
            word = "%{0}".format(self.name[2:])
            byte_version = "{0}l".format(word)
        else:
            byte_version = "{0}b".format(self.name)
        return byte_version

    class Meta:
        ordering = ['id']

class Instruction(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    num = models.IntegerField(default=1)
    src = models.CharField(max_length=50, blank=True)
    dest = models.CharField(max_length=50, blank=True)
    label = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_description(self):
        if self.name == ".section":
            return "Make the "+self.src+" section the current section"
        elif self.name == ".string":
            return "Allocate memory containing "+self.src+" where the string is '\\0' terminated, in the current section."
        elif self.name == ".globl":
            return "Mark label \""+self.src+"\" so it is accessible by code generated from other source code files."
        elif self.name == ".type":
            return "Mark label "+self.src.split(',')[0]+" so the linker knows that it denotes the beginning of a function."
        elif self.name == ".skip":
            return "Skip "+self.src+" byte(s) of memory in the current section."
        elif self.name == ".equ":
            return "Define "+self.src+" as a symbolic alias for "+self.dest+"."
        elif "mov" in self.name:
            return "Copy "+self.src+" to "+self.dest
        elif "add" in self.name:
            return "Add "+self.src+" to "+self.dest+""
        elif "sal" in self.name:
            return "Shift "+self.dest+" to the left "+self.src+" bits, filling with zeros. If "+self.src+" is a register, then it must be the CL register."
        elif self.name == "imulq" and self.dest == "":
            return "Signed Multiply: Multiply the contents of register RAX by "+self.src+", and store the product in registers RDX:RAX."
        elif "inc" in self.name:
            return "Increment "+self.src+"."
        elif "cmp" in self.name:
            return "Compute "+self.dest+" - "+self.src+" and set flags in the EFLAGS register based upon the result."
        elif self.name == "jmp":
            return "Jump to label \""+self.src+"\""
        elif "j" in self.name:
            return "Jump to label \""+self.src+"\" iff the flags in the EFLAGS register indicate a(n) "+self.name[1:]+" relationship between the most recently compared numbers."
        elif self.name == "call":
            if self.src == "printf":
                return "Call function \""+self.src+"\", formats and prints its arguments, after the first, under control of the format; returns number of characters successfully printed. "
            elif self.src == "scanf":
                return "Call function \""+self.src+"\", reads input from the stdin according to a format; returns number of inputs successfully read from stdin. "
            elif self.src == "abs":
                return "Call function \""+self.src+"\", computes the absolute value of its integer argument. "
            elif self.src == "getchar":
                return "Call function \""+self.src+"\", returns the character read from stdin as an unsigned char cast to an int or EOF on end of file or error."
            elif self.src == "putchar":
                return "Call function \""+self.src+"\", returns argument character written as an unsigned char cast to an int or EOF on error, writes character to stdout."
            else:
                return "Call function \""+self.src+"\""
        elif self.name == "ret":
            return "Return from the current function. "
        else:
            return self.name

    class Meta:
        ordering = ['num']

class Stack(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True) # 0x0, 0x8, etc.
    val = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['id']

class Eflag(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    cf = models.IntegerField(default=0)
    zf = models.IntegerField(default=0)
    sf = models.IntegerField(default=0)
    of = models.IntegerField(default=0)

class Rodata(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True) #address
    val = models.CharField(max_length=50, blank=True)
    label = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['id']

class Data(models.Model): #.globl, .byte, .word, etc.
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    val = models.CharField(max_length=50, blank=True)
    name = models.CharField(max_length=50, blank=True) #address
    label = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['id']

class BSS(models.Model): #.skip
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True) #address
    val = models.CharField(max_length=50, blank=True) #value at address
    label = models.CharField(max_length=50, blank=True) #label pointing to memory

    class Meta:
        ordering = ['id']

class Text(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    val = models.CharField(max_length=50, default="*code text here*")

class Arg(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True) #someLabel
    text = models.CharField(max_length=200, blank=True) #explanation
    val = models.CharField(max_length=50, blank=True) # user input value
    addr = models.CharField(max_length=50, blank=True) # user input value

    class Meta:
        ordering = ['id']

class Constant(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    label = models.CharField(max_length=50, blank=True) # SOMELABEL
    val = models.CharField(max_length=50, blank=True) #value at somelabel

    class Meta:
        ordering = ['id']
