# AUTOGENERATED! DO NOT EDIT! File to edit: extract_genetic_data.ipynb (unless otherwise specified).

__all__ = ['G_O_dict_maker_single', 'say_hello']

# Cell

def G_O_dict_maker_single(self, filename):
        """
        creates GWAS and outside genetic info data structures for a single file
        """
        file = open(filename, "r")

        found_GWAS = set()
        found_outside = set()
        GWAS_map = {}
        outside_map = {}

        line_num = 1

        for i,line in tqdm(enumerate(file)):
            rsid = self.column_getter(line, self.rsid_col)
            if rsid in self.GWAS_set or rsid in self.outside_set:
                pos_1 = self.column_getter(line, self.snp_col)
                if "/" in pos_1:
                    pos_2 = pos_1[2]
                    pos_1 = pos_1[0]
                else:
                    pos_2 = self.column_getter(line, self.snp_col + 1)
                if len(pos_1) > 1 or len(pos_2) > 1:
                    continue

                poss_geno = possible_genotypes(pos_1, pos_2)
                head, alleles = self.column_cutter(line, self.col_cut)
                allele_list = alleles.split(self.delim)
                if self.is_triples:
                    if len(allele_list) % 3 != 0:
                        raise ValueError(
                            "Missing data. Incomplete genotype triple found in line " + str(line_num) + ".")
                    else:
                        allele_list = self.triplicate_converter(
                            allele_list, pos_1, pos_2)

                allele_list = list(map(self.clean_item_cached, allele_list))
                # remove list here
                total = len(list(allele_list))

                if rsid in self.GWAS_set:
                    found_GWAS.add(rsid)
                    new_map = defaultdict(list)
                    new_map["alleles"] = poss_geno
                    new_map["total"] = total
                    for i in range(len(list(allele_list))):
                        curr_allele = allele_list[i]
                        if curr_allele != self.NA:
                            new_map[curr_allele].append(i)
                        else:
                            new_map["NA_indices"].append(i)
                    GWAS_map[rsid] = new_map
                else:
                    found_outside.add(rsid)
                    outside_map[rsid] = allele_list, poss_geno
            line_num += 1
        file.close()

        logging.info(str(len(found_GWAS)) + " out of " + str(len(self.GWAS_set)
                                                             ) + " GWAS rsIDs found in " + filename + ".")
        not_found_GWAS = self.GWAS_set.difference(found_GWAS)
        if len(not_found_GWAS) > 0:
            logging.info("WARNING: The following GWAS rsIDs are found in the pairing file, but not " +
                         filename + ".\n" + str(not_found_GWAS))
            if not_found_GWAS == self.GWAS_set:
                return None, None

        logging.info(str(len(found_outside)) + " out of " + str(len(self.outside_set)
                                                                ) + " outside rsIDs found in " + filename + ".")
        not_found_outside = self.outside_set.difference(found_outside)
        if len(not_found_outside):
            logging.info("WARNING: The following outside rsIDs are found in the pairing file, but not " +
                         filename + ".\n" + str(not_found_outside))
            if not_found_outside == self.outside_set:
                return None, None

        df_data = [*zip(not_found_GWAS, ["not_found"] * len(not_found_GWAS), ["GWAS"]* len(not_found_GWAS)),
            *zip(not_found_outside, ["not_found"] * len(not_found_outside), ["outside"]* len(not_found_outside)),]

        self.filter_df = pd.DataFrame(df_data, columns=["rsID", "reason_for_filtering", "SNP_type"])

        return GWAS_map, outside_map

# Cell
def say_hello(to):
    "Say hello to somebody"
    return f'Hello {to}!'