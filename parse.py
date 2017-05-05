print "from visualizer.models import Instruction, Register, Problem, Stack, Eflag, Rodata, Data, BSS, Text, Arg"
print "curr_pk=5"
print "p=Problem(number=curr_pk, steps=1)"
# print 'p=Problem.objects.get(pk=curr_pk)'
print "p.save()"
print "p.eflag_set.all().delete()"
print "eflags=Eflag(cf=0, zf=0, sf=0, of=0, problem_id=curr_pk)"
print "eflags.save()"
print "p.rodata_set.all().delete()"
print "p.data_set.all().delete()"
print "p.bss_set.all().delete()"
print "p.arg_set.all().delete()"
print "p.constant_set.all().delete()"

filename="power.s.txt"
with open(filename,"r") as f:
    content = f.read().splitlines()
f.close()

print "p.instruction_set.all().delete()"
pid = 5
labeled = 0
labl = ""
cnt = 0
for line in content:
    if line:
        instr = line.lstrip(' ').rstrip(' ')
        if "#" not in instr:
            if "string" not in instr:
                instr_arr = instr.split()
                if ":" in instr:
                    labeled = 1
                    labl = instr_arr[0][:-1]
                elif "section" in instr:
                    num = cnt+1
                    print "i = Instruction(problem_id="+str(pid)+", name=\""+instr_arr[0]+"\", src=\"\\"+instr_arr[1][:-1]+"\\"+"\"\", num="+str(num)+")"
                    print "i.save()"
                    cnt = cnt + 1
                elif len(instr_arr) == 2:
                    num = cnt+1
                    if labeled == 0:
                        print "i = Instruction(problem_id="+str(pid)+", name=\""+instr_arr[0]+"\", src=\""+instr_arr[1]+"\", num="+str(num)+")"
                    else:
                        print "i = Instruction(problem_id="+str(pid)+", name=\""+instr_arr[0]+"\", src=\""+instr_arr[1]+"\", label=\""+labl+"\", num="+str(num)+")"
                        labeled = 0
                    print "i.save()"
                    cnt = cnt + 1
                elif len(instr_arr) == 3:
                    num = cnt+1
                    if labeled == 0:
                        print "i = Instruction(problem_id="+str(pid)+", name=\""+instr_arr[0]+"\", src=\""+instr_arr[1][:-1]+"\", dest=\""+instr_arr[2]+"\", num="+str(num)+")"
                    else:
                        print "i = Instruction(problem_id="+str(pid)+", name=\""+instr_arr[0]+"\", src=\""+instr_arr[1][:-1]+"\", dest=\""+instr_arr[2]+"\", label=\""+labl+"\", num="+str(num)+")"
                        labeled = 0
                    print "i.save()"
                    cnt = cnt + 1
                elif len(instr_arr) == 1:
                    num = cnt+1
                    if labeled == 0:
                        print "i = Instruction(problem_id="+str(pid)+", name=\""+instr_arr[0]+"\", num="+str(num)+")"
                    else:
                        print "i = Instruction(problem_id="+str(pid)+", name=\""+instr_arr[0]+"\", label=\""+labl+"\", num="+str(num)+")"
                        labeled = 0
                    print "i.save()"
                    cnt = cnt + 1
            else:
                instr_arr = instr.split("\"")
                rodata = "\""+instr_arr[1]+"\""
                num = cnt+1
                if labeled == 0:
                    print "i = Instruction(problem_id="+str(pid)+", name=\".string\", src=\"\\"+rodata[:-1]+"\\"+"\"\", num="+str(num)+")"
                else:
                    print "i = Instruction(problem_id="+str(pid)+", name=\".string\", src=\"\\"+rodata[:-1]+"\\"+"\"\", label=\""+labl+"\", num="+str(num)+")"
                    labeled = 0
                print "i.save()"
                cnt = cnt + 1
print "p.steps="+str(cnt)
print "p.filename="+filename
print "p.save()"
