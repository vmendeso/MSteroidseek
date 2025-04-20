import pandas as pd
import numpy as np
from SpectraFP import SpectraFP
from app.utils.fastsimilarity import getOnematch


def match_FP(user_input, degree_freedom , df_fpx, threshold,  metric):
       
        lista = user_input.split(',')
        mz_peak_list = [float(x) for x in lista]
        mzs =  np.array(mz_peak_list)
        fpmz = SpectraFP(range_spectra=[14.0, 846.0, 0.1])
        fp_dfx = []
        fp_dfx = fpmz.genFP(mzs, correction=degree_freedom, spurious_variables=False)
        fp_dfx = np.array([fp_dfx])

        
        df_completo = pd.concat([df,df_fpx], axis=1)



        basex = df_completo.iloc[:,2:].values.astype('uint32')        
        var = getOnematch(base_train = basex, base_test = fp_dfx, complete_base = df_completo, similarity_metric=metric, alpha=1, beta=1, threshold=threshold)
        var = dict(sorted(var.items(), key=lambda x: x[1], reverse=True))
        return(var)