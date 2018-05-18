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
# # join the error and standard output streams
# #$ -j y
#
#
# send e-mail when job ends
#$ -m e
#
# this is my e-mail address
#$ -M lyushanshan@qq.com
#
#where the format error go
#$ -e /home/sslv/Projects/error
#where the format output go
#$ -o /home/sslv/Projects/output
# notify me about pending SIG_STOP and SIG_KILL
#$ -notify
#
# Specify the array start ,end , step
#$ -t 1-6:1
# end of SGE stuff
#########################################################
# now execute my job:
ARRAY=(head wt_1 wt_2 wt_3 mt-1 mt-2 mt-3)
#  echo ${ARRAY[$SGE_TASK_ID]}
source ~/.bashrc
DIR=/home/sslv/Projects/CHK0008
TMPD=$DIR/hisat2_htseq_out
REF=/home/sslv/species/Ath/Arabidopsis_thaliana.TAIR10.22_tran
GTF=/home/sslv/species/Ath/Arabidopsis_thaliana.TAIR10.22_no_gene_name.gtf
mkdir -p $TMPD/${ARRAY[$SGE_TASK_ID]}MAP
/share/apps/prog/hisat2.0.4/hisat2 -p 28 -x $REF -1 $DIR/QC/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_clean_pair1.fastq -2 $DIR/QC/${ARRAY[$SGE_TASK_ID]}/${ARRAY[$SGE_TASK_ID]}_clean_pair2.fastq -S $TMPD/${ARRAY[$SGE_TASK_ID]}MAP/${ARRAY[$SGE_TASK_ID]}.sam
/share/apps/prog/samtools-1.3.1/bin/samtools sort -n -@ 8 -O SAM -o $TMPD/${ARRAY[$SGE_TASK_ID]}MAP/${ARRAY[$SGE_TASK_ID]}_sorted.sam $TMPD/${ARRAY[$SGE_TASK_ID]}MAP/${ARRAY[$SGE_TASK_ID]}.sam
/home/sslv/.local/bin/htseq-count -f sam -r name -s no -q $TMPD/${ARRAY[$SGE_TASK_ID]}MAP/${ARRAY[$SGE_TASK_ID]}_sorted.sam $GTF > $TMPD/${ARRAY[$SGE_TASK_ID]}MAP/${ARRAY[$SGE_TASK_ID]}_htseq_out.txt
sed -n "1,33602p" $TMPD/${ARRAY[$SGE_TASK_ID]}MAP/${ARRAY[$SGE_TASK_ID]}_htseq_out.txt > $TMPD/${ARRAY[$SGE_TASK_ID]}MAP/${ARRAY[$SGE_TASK_ID]}_htseq_out.R
