from unidecode import unidecode

class NamePair(object):
    def __init__(self, pair_id, variant1, variant2, n_paar, n_pvoorkomen1, n_pvoorkomen2, n_genlias1, n_genlias2, n_namen, normalise_variants = False):
        self.pair_id = pair_id
        self.variant1 = unidecode(variant1) if normalise_variants else variant1
        self.altered_variant1 = variant1 != self.variant1 if normalise_variants else None
        self.variant2 = unidecode(variant2) if normalise_variants else variant2
        self.altered_variant2 = variant2 != self.variant2 if normalise_variants else None
        self.n_paar = int(n_paar)
        self.n_pvoorkomen1 = int(n_pvoorkomen1)
        self.n_pvoorkomen2 = int(n_pvoorkomen2)
        self.n_genlias1 = int(n_genlias1)
        self.n_genlias2 = int(n_genlias2)
        self.n_namen = int(n_namen)


class FirstNamePair(NamePair):
    def __init__(self, vpv_id, sexe, variant1, variant2, n_paar, n_pvoorkomen1, n_pvoorkomen2, n_genlias1, n_genlias2, n_namen, grondnaam1, grondnaam2, *args, normalise_variants = False):
        super().__init__(vpv_id, variant1, variant2, n_paar, n_pvoorkomen1, n_pvoorkomen2, n_genlias1, n_genlias2, n_namen)
        self.sexe = sexe
        self.grondnaam1 = grondnaam1
        self.grondnaam2 = grondnaam2


class LastNamePair(NamePair):
    def __init__(self, vpf_id, variant1, variant2, n_paar, n_pvoorkomen1, n_pvoorkomen2, n_genlias1, n_genlias2, n_namen, *args, normalise_variants = False):
        super().__init__(vpf_id, variant1, variant2, n_paar, n_pvoorkomen1, n_pvoorkomen2, n_genlias1, n_genlias2, n_namen)