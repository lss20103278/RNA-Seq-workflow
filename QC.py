#!/usr/bin/python

import os; import re; import subprocess;

raw_data_dirname = raw_input("raw_data_dirname: ")
raw_data = subprocess.Popen('ls -F '+raw_data_dirname+" |grep /$ |cut -d '/' -f 1", shell=True, stdout=subprocess.PIPE)
stdoutput = raw_data.communicate()[0]
name = stdoutput.split('\n')[:-1]
n = len(name)
#p = re.compile(r'(.*?)_R1.fastq')
#name = p.findall(stdoutput)
#n = len(name)

file = open('QC.bash','w')
#os.chdir('RL0001')
dir_path = os.getcwd()
if not os.path.exists(dir_path+'/QC'):
    os.system('mkdir QC')
if not os.path.exists(dir_path+'/error'):
    os.system('mkdir error')
if not os.path.exists(dir_path+'/output'):
    os.system('mkdir output')
if not os.path.exists(dir_path+'/results'):
    os.system('mkdir results')

file.write("#!/bin/bash\n####################################################################\n#\n#A (quite) simple submit script for a one or tow processor job\n#\n####################################################################\n#\n# SGE options\n#\n#Change to the current working directory upon starting of the job\n#$ -cwd\n#\n# Specify the kind of shell script you use, for example, bash\n#$ -S /bin/bash\n#\n# # join the error and standard output streams\n# #$ -j y\n#\n#\n# don't flood myself with e-mail\n#$ -m e\n#\n# this is my e-mail address\n#$ -M 1573077420@qq.com\n#\n#where the format error go\n")
file.write("#$ -e "+dir_path+"/error\n")
file.write("#where the format output go\n")
file.write("#$ -o "+dir_path+"/output\n")
file.write("# notify me about pending SIG_STOP and SIG_KILL\n#$ -notify\n#\n# Specify the array start ,end , step\n")
file.write("#$ -t 1-"+str(n)+":1\n") 
file.write("# end of SGE stuff\n#########################################################\n# now execute my job:\n")
file.write("ARRAY=(head ")
for i in range(len(name)):
    file.write(name[i]+" ")
file.write(")\n")
file.write("#  echo ${ARRAY[$SGE_TASK_ID]}\n")

file.write("source ~/.bashrc\n")
file.write("DIR="+dir_path+"\n")
file.write("RE=$DIR/results\n")
file.write("DATA=$DIR/"+raw_data_dirname+"\nTMPD=$DIR/QC\nCODE=/home/sslv/Script/RNA_seq_script/countsum.pl\n")

file.write("mkdir -p $TMPD/${ARRAY[$SGE_TASK_ID]}\nzcat $DATA/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.gz > $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq\nzcat $DATA/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq.gz > $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq\n/share/apps/prog/FastQC/fastqc -o $TMPD/${ARRAY[$SGE_TASK_ID]} -t 28 $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq\n/share/apps/prog/FastQC/fastqc -o $TMPD/${ARRAY[$SGE_TASK_ID]} -t 28 $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq\n/share/apps/prog/SolexaQA_v.2.2/DynamicTrim.pl $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq -h 17 -d $TMPD/${ARRAY[$SGE_TASK_ID]}\n/share/apps/prog/SolexaQA_v.2.2/DynamicTrim.pl $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq -h 17 -d $TMPD/${ARRAY[$SGE_TASK_ID]}\n/share/apps/prog/SolexaQA_v.2.2/LengthSort.pl $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.trimmed $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq.trimmed -l 25 -d $TMPD/${ARRAY[$SGE_TASK_ID]}\n")

file.write("cutadapt -a AGATCGGAAGAG -f fastq $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.trimmed.paired1 -o $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.cut\ncutadapt -a AGATCGGAAGAG -f fastq $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.trimmed.paired2 -o $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq.cut\n/share/apps/prog/SolexaQA_v.2.2/LengthSort.pl $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.cut $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq.cut -l 25 -d $TMPD/${ARRAY[$SGE_TASK_ID]}\n")

file.write('''OUT1="${ARRAY[$SGE_TASK_ID]}_R1.fastq\t`perl $CODE $DATA/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq`\t`perl $CODE $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.trimmed.paired1`\t`perl $CODE $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.cut`\t`perl $CODE $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.cut.paired1`"\nOUT2="${ARRAY[$SGE_TASK_ID]}_R2.fastq\t`perl $CODE $DATA/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq`\t`perl $CODE $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.trimmed.paired2`\t`perl $CODE $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R2.fastq.cut`\t`perl $CODE $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.cut.paired2`"\n''')
file.write('''echo "$OUT1\n''')
file.write('''$OUT2" >> $RE/outcome.tmp\n''')

file.write("mv $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.cut.paired1 $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_clean_pair1.fastq\nmv $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_R1.fastq.cut.paired2 $TMPD/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_clean_pair2.fastq\n")



file.write("# end of job script")


