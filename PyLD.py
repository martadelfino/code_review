
import csv
import itertools

import pandas as pd

def get_dict_of_genotypes(file_path):
    with open(file_path) as vcf_file:
        # Skip metadata:
        vcf_lines = itertools.dropwhile(lambda row: row.startswith('##'), vcf_file)
        # According to the spec (https://samtools.github.io/hts-specs/VCFv4.2.pdf)
        # the next line should be the header:
        columns = vcf_lines.__next__().strip().lstrip('#').split('\t')
        # What remains of vcf_lines should now be the data:
        vcf_data = map(lambda row: row.strip().split('\t'), vcf_lines)
        # Pandas is happy to consume the iterable:
        vcf_df = pd.DataFrame(vcf_data, columns=columns)
        # Columns of interest start with 'HG', index by 'ID':
        gene_columns = list(filter(lambda col: col.startswith('HG'), columns))
        gene_df = vcf_df.set_index('ID')[gene_columns]
        # DataFrame.to_dict('index') returns a dict of dicts.
        # Need the values of the inner dicts as lists.
        return {k: list(v.values()) for k, v in gene_df.to_dict('index').items()}
    
def pipe_split(gtype):
    return gtype.split('|')

def determine_haplotype(genotype_list_1, genotype_list_2):
    '''Function compares alleles of each individual and determines their haplotype
    '''

    # "genotypes" contains pairs of tuples from each list.
    genotypes = zip(
        map(pipe_split, genotype_list_1),
        map(pipe_split, genotype_list_2)
    )
    '''
    zip(*iterable) and itertools are our friends: (GRG)
        eg = [(1 ,2), (3, 4)]
        list(zip(*eg))
        [(1, 3), (2, 4)]
    '''
    results = (''.join(gt)
        for gt in itertools.chain.from_iterable(
            itertools.starmap(zip, genotypes)
        )
    )    
    valid = ('00', '01', '10', '11')
    return [res if res in valid else 'N/A' for res in results]    

def count_haplotypes(compare_genotypes):
    '''Function counts how many of each haplotype exist
    The 00 is PA PB alleles (so reference, reference for each rsID)
    01 is PA Pb alleles
    10 is Pa PB alleles
    11 is Pa Pb alleles
    This is only possible because the vcf files I used had phased data.
    '''
    
    '''
     "itertools.groupby" makes this a "one-liner", if that's a *good*
     thing. *Might* be faster than "+=". Don't forget to sort. -GRG
    '''
    return {
        hap: len(list(group)) for hap, group in itertools.groupby(
            sorted(compare_genotypes))
    }
    
def count_PA_PB_PAB(haplotype_counts):
    '''
    Function obtains the PA, PB, PAB allele frequencies needed for r^2 and D' calculations
    In this case, I'm dividing the frequencies by the total individuals in the population
    For the toy population we used had 100 individuals, so 200 alleles
    '''
    count_dict = {'PA': 0, 'PB': 0, 'PAB': 0}
    
    '''
    "sum" is a built-in, if all the values in the dict are numeric,
    All Shall Be Well. No need to hard-code:
    '''
    total = sum(haplotype_counts.values()) 
    count_dict['PA'] = (haplotype_counts['00'] + haplotype_counts['01']) / total
    count_dict['PB'] = (haplotype_counts['00'] + haplotype_counts['10']) / total
    count_dict['PAB'] = (haplotype_counts['00']) / total

    return count_dict
    
def calculate_D(count_dict):
    '''
    Function that calculates D
    This is only dependent on what alleles were chosen for PA, PB, Pa, Pb. 
    '''
    PA = count_dict['PA'] 
    PB = count_dict['PB'] 
    PAB = count_dict['PAB'] 
    D = PAB - (PA * PB)
    return D    
    
def calculate_r_squared(D, count_dict):
    '''
    Function calculates the r^2, which is a measure of D. It measures the correlation.
    '''
    PA = count_dict['PA']
    PB = count_dict['PB']
    try:
        r_squared = (D ** 2) / (PA * (1 - PA) * PB * (1 - PB))
    except ZeroDivisionError:
        r_squared = 0.0
    
    return r_squared    
    
def calculate_D_prime(D, count_dict):
    '''
    Function for calculating D' measurement of Linkage Disequilibrium. 
    Function takes D, PA and PB calculated previously. 
    The equation for D' is D / Dmax. Dmax is calculated differently for D>0 and D<0.
    '''
    PA = count_dict['PA']
    PB = count_dict['PB']
    try: 
        if D > 0:
            Dmax = min(PA*(1-PB), (1-PA)*PB)
        else:
            Dmax = max(-abs(PA)*PB, -abs((1-PA)*(1-PB)))
        D_prime = D / Dmax
    except ZeroDivisionError:
        D_prime = 0.0 

    return D_prime

class LD(object):
    def __init__(self, file_path, list_of_rsIDs):
        self.file_path = file_path
        self.list_of_rsIDs = list_of_rsIDs

    def calculate_LD_measures(self): 
        population = get_dict_of_genotypes(self.file_path)

        '''Do away with one level of indentation with "combinations".
        Unless you *really* want to manipulate indices,
        some_list[i] for i in range(len(some_list)) is a bit cringe...
        -GRG
        '''
        
        get_genotype = population.get
        results = []
        for rsID_1, rsID_2 in itertools.combinations(self.list_of_rsIDs):
            # Genotypes
            genotype1 = get_genotype(population, rsID_1)
            genotype2 = get_genotype(population, rsID_2)
            # Haplotypes
            haplotypes = determine_haplotype(genotype1, genotype2)
            haplotypes_count = count_haplotypes(haplotypes)
            # Loci Frequencies
            loci_frequencies = count_PA_PB_PAB(haplotypes_count)
            # LD measures 
            D = calculate_D(loci_frequencies)
            r2 = calculate_r_squared(D, loci_frequencies)
            Dprime = calculate_D_prime(D, loci_frequencies)
            # Dictionary of result for one pair of rsIDs
            result = {'rsID_1': rsID_1, 'rsID_2': rsID_2,
                'haplotypes': haplotypes_count,
                'pA':  loci_frequencies['PA'], 
                'pB': loci_frequencies['PB'], 
                'pAB': loci_frequencies['PAB'],
                'D': D,
                'r^2': r2, 
                'Dprime': Dprime}
            # List of final results
            results.append(result)

        return results
    
    def save_results(self, output_file_path):
        results = self.calculate_LD_measures()
        with open(output_file_path, 'w', newline='', encoding="utf-8") as f:
            # DictWriters are a thing -GRG.
            writer = csv.DictWriter(
                f, fieldnames=results[0].keys(), delimiter='\t'
            )
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        

#test_list = ['rs1050979', 'rs34941730', 'rs116763857']
#test = LD('toy_data.vcf', test_list)
#print(test.calculate_LD_measures())
#test.save_results('test_output.tsv')

