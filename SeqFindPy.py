import argparse,re,sys

parser=argparse.ArgumentParser(description="To get the location and anotation of a sequence. First-writtern@20190716 by ZhenLi.")
parser.add_argument("-f","--fasta",required=True,type=str,help="The genome sequence,fasta format.")
parser.add_argument("-p","--expression",required=True,type=str,help="The pattern of the sequence.")
args=parser.parse_args()

def SeqLocation(genomefile):
    oplist=[]
    genome_dict={}
    with open(genomefile,'r') as F:
        for line in F:
            if line.startswith(">"):
                key=line.strip(">\n")
                genome_dict[key]=""
            else:
                genome_dict[key]+=line.rstrip()
    for key in genome_dict:
        sequence=genome_dict[key]
        reverse_seq=list(sequence)
        reverse_seq.reverse()
        reverse_seq="".join(reverse_seq)

        P_Location=re.finditer(args.expression,sequence,re.I)
        P_pattern_loc=[(i.start(),i.end()) for i in P_Location]
        for L in P_pattern_loc:
            oplist.append("\t".join([key,str(L[0]),str(L[1]),sequence[L[0]:L[1]],'.','+'])+"\n")

        N_Location=re.finditer(args.expression,reverse_seq,re.I)
        N_pattern_loc=[(i.start(),i.end()) for i in N_Location]
        for L in N_pattern_loc:
            oplist.append("\t".join([key,str(L[0]),str(L[1]),reverse_seq[L[0]:L[1]],'.','-'])+"\n")
    return oplist

if __name__=="__main__":
    oplist=SeqLocation(genomefile=args.fasta)
    for i in oplist:
        sys.stdout.write(i)
