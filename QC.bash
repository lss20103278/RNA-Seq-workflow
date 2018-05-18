#!/bin/bash
####################################################################
#
#A (quite) simple submit script for a one or tow processor job
#
####################################################################
#
# SGE options
#
#Change to the current working directory upon starting of the job
#$ -cwd
#
# Specify the kind of shell script you use, for example, bash
#$ -S /bin/bash
#
# join the error and standard output streams
#$ -j y
#
#
# don't flood myself with e-mail
#$ -m e
#
# this is my e-mail address
##$ -M lyushanshan@qq.com
#
#where the format error go
#$ -e /psc/home/sslv
#where the format output go
#$ -o /psc/home/sslv
# notify me about pending SIG_STOP and SIG_KILL
#$ -notify
#
# Specify the array start ,end , step
#$ -t 1-6:1 
# end of SGE stuff
#########################################################
# now execute my job:
ARRAY=(head wt_1 wt_2 wt_3 mt_1 mt_2 mt_3)
#  echo ${ARRAY[$SGE_TASK_ID]}

DIR=/psc/home/sslv/KIM0001
RE=$DIR/results
DATA=$DIR/data
TMPD=$DIR/tmp_data
CODE=/psc/home/sslv/KIM0001/RNA_seq_script/countsum.pl

/psc/program/install/SolexaQA_v.2.2/DynamicTrim.pl $DATA/${ARRAY[$SGE_TASK_ID]}1.fastq -h 20 -d $TMP
/psc/program/install/SolexaQA_v.2.2/DynamicTrim.pl $DATA/${ARRAY[$SGE_TASK_ID]}2.fastq -h 20 -d $TMP
/psc/program/install/SolexaQA_v.2.2/LengthSort.pl $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.trimmed $TMP/${ARRAY[$SGE_TASK_ID]}2.fastq.trimmed -l 25 -d $TMP

/psc/home/sslv/cutadapt-1.4.1/bin/cutadapt -a AGATCGGAAGAG -f fastq $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.trimmed.paired1 -o $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.cut
/psc/home/sslv/cutadapt-1.4.1/bin/cutadapt -a AGATCGGAAGAG -f fastq $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.trimmed.paired2 -o $TMP/${ARRAY[$SGE_TASK_ID]}2.fastq.cut
/psc/program/install/SolexaQA_v.2.2/LengthSort.pl $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.cut $TMP/${ARRAY[$SGE_TASK_ID]}2.fastq.cut -l 25 -d $TMP

OUT1="${ARRAY[$SGE_TASK_ID]}1.fastq	`perl $CODE $DATA/${ARRAY[$SGE_TASK_ID]}1.fastq`	`perl $CODE $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.trimmed.paired1`	`perl $CODE $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.cut.paired1`"
OUT2="${ARRAY[$SGE_TASK_ID]}2.fastq	`perl $CODE $DATA/${ARRAY[$SGE_TASK_ID]}2.fastq`	`perl $CODE $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.trimmed.paired2`	`perl $CODE $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.cut.paired2`"
echo "$OUT1
$OUT2" >> $RE/outcome.tmp

mv $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.cut.paired1 $TMPD/${ARRAY[$SGE_TASK_ID]}clean_pair1.fastq
mv $TMP/${ARRAY[$SGE_TASK_ID]}1.fastq.cut.paired2 $TMPD/${ARRAY[$SGE_TASK_ID]}clean_pair2.fastq



# end of job script


