import csv
import pandas as pd


def get_dict_of_genotypes(file_path):
    column_names: list[str] = []

    column_names = []

    with open(file_path, 'r') as f:
        for line in f:
            # Strip whitespace from the line
            line = line.strip()
            if line.startswith("##"):
                # Skip header lines that start with "##"
                continue
            # Store column names if the line starts with '#'
            elif line.startswith("#"):
                column_names = line.split("\t")
            else:
                break

    # Read the VCF file again and create a df excluding header lines
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                # Split the line by tabs and append the data to the list
                data.append(line.split("\t"))

    # Create a DataFrame using column names and data
    df = pd.DataFrame(data, columns=column_names)

    filtered_df: pd.DataFrame = df[['ID'] + [col for col in df.columns if col.startswith('HG')]]

    result_dict = {}

    for index, row in filtered_df.iterrows():
            # Extract the ID from the current row
        id_value = row['ID']
        # Extract the values from the remaining columns
        values = row.drop('ID').tolist()
        # Add the ID and values to the dictionary
        result_dict[id_value] = values
        
    return result_dict



def get_genotype(population_dictionary, rsID):
    genotype_list = population_dictionary[rsID]
    return genotype_list
    

def determine_haplotype(genotype_list_1, genotype_list_2):
    '''Function compares alleles of each individual and determines their haplotype
    '''
    result = []
    for i in range(len(genotype_list_1)):
        genotype1 = genotype_list_1[i].split("|")
        genotype2 = genotype_list_2[i].split("|")
        gt1 = int(genotype1[0])
        gt2 = int(genotype2[0])
        gt3 = int(genotype1[1])
        gt4 = int(genotype2[1])
        if gt1 == 0 and gt2 == 0:
            result.append("00")
        elif gt1 == 0 and gt2 == 1:
            result.append("01")
        elif gt1 == 1 and gt2 == 0:
            result.append("10")
        elif gt1 == 1 and gt2 == 1:
            result.append("11")
        else:
            result.append("N/A")
        if gt3 == 0 and gt4 == 0:
            result.append("00")
        elif gt3 == 0 and gt4 == 1:
            result.append("01")
        elif gt3 == 1 and gt4 == 0:
            result.append("10")
        elif gt3 == 1 and gt4 == 1:
            result.append("11")
        else:
            result.append("N/A")
    return result
    

def count_haplotypes(compare_genotypes) -> dict[str, int]:
    '''Function counts how many of each haplotype exist
    The 00 is PA PB alleles (so reference, reference for each rsID)
    01 is PA Pb alleles
    10 is Pa PB alleles
    11 is Pa Pb alleles
    This is only possible because the vcf files I used had phased data.
    '''
    count_dict: dict[str, int] = {'00': 0, '01': 0, '10': 0, '11': 0}
    for genotype in compare_genotypes:
        count_dict[genotype] += 1
    return count_dict
    

def count_PA_PB_PAB(haplotype_counts) -> dict[str, int]:
    '''
    Function obtains the PA, PB, PAB allele frequencies needed for r^2 and D' calculations
    In this case, I'm dividing the frequencies by the total individuals in the population
    For the toy population we used had 100 individuals, so 200 alleles
    '''
    count_dict = {'PA': 0, 'PB': 0, 'PAB': 0}
    total = 200 # this will need to become a count of how many HG individuals there are 
    count_dict['PA'] = (haplotype_counts['00']+haplotype_counts['01'])/total
    count_dict['PB'] = (haplotype_counts['00']+haplotype_counts['10'])/total
    count_dict['PAB'] = (haplotype_counts['00'])/total

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



class LD:
    def __init__(self, file_path, list_of_rsIDs) -> None:
        self.file_path = file_path
        self.list_of_rsIDs = list_of_rsIDs
        self.results: list[dict] = []

    def calculate_LD_measures(self): 
        population = get_dict_of_genotypes(self.file_path)

        for i in range(len(self.list_of_rsIDs)):
            for j in range(i+1, len(self.list_of_rsIDs)):
                rsID_1 = self.list_of_rsIDs[i]
                rsID_2 = self.list_of_rsIDs[j]
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
                self.results.append(result)

        return self.results
    
    def save_results(self, output_file_path) -> None:
        results = self.calculate_LD_measures()
        with open(output_file_path, 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(results[0].keys())
            for row in results:
                writer.writerow(row.values())
        

#test_list = ['rs1050979', 'rs34941730', 'rs116763857']
#test = LD('/Users/martadelfino/PyLD/toy_data.vcf', test_list)
#print(test.calculate_LD_measures())


#test.save_results('/Users/martadelfino/PyLD/test_output.csv')

