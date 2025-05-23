import pandas as pd
import numpy as np
from SpectraFP import SpectraFP, SearchEngine
from app.utils.fastsimilarity import getOnematch

#def match_FP(user_input, degree_freedom, threshold,  metric):
#        se = SearchEngine()
#        csv_peaks = str(pd.read_csv(user_input))
#        lista = csv_peaks.split(',')
#        get_structures = se.search(signs_list=lista,
#                                   threshold=threshold,
#                                   difBetween13C=7,
#                                   correction=degree_freedom,
#                                   similarity=metric)
#        return get_structures
def match_FP(user_input, degree_freedom, df_fpx, df_db, threshold,  metric):
        lista = user_input.split(',')
        print(df_db)
        mz_peak_list = [float(x) for x in lista]
        mzs =  np.array(mz_peak_list)
        print(f"lista de mz aqui **************{mzs}")
        fpmz = SpectraFP(range_spectra=[14.0, 846.0, 0.1])
        fp_dfx = []
        fp_dfx = fpmz.genFP(mzs, correction=degree_freedom, spurious_variables=False)
        print(f"lista de fps aqui **************{fp_dfx}")
        fp_dfx = np.array([fp_dfx])
        print(f"lista de fps aqui **************{fp_dfx}")      
        df_completo = pd.concat([df_db,df_fpx], axis=1)        
        basex = df_completo.iloc[:,3:].values.astype('uint32') 
        print(f"lista de fps aqui **************{basex}")         
        var = getOnematch(base_train = basex, base_test = fp_dfx, complete_base = df_completo, similarity_metric=metric, alpha=1, beta=1, threshold=threshold)
        print(var)
        var = dict(sorted(var.items(), key=lambda x: x[1], reverse=True))
        return(var)