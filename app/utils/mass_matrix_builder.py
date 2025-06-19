import pandas as pd
import numpy as np
import pickle
import sklearn


# steroid mass matrix builder
def frag_matrix_builder(mass,intencity_rel,exact_mass):
    ## separando m/z
    mz_temp = [int(float(x)) for x in mass]
    
    ## separando int.rel
    rel_temp = [int(float(x)) for x in intencity_rel]
    # massa exata
    exact_mz = int(exact_mass)
    # buscando lista de m/z (artigo)
    mz4steroid_subtracao = [15,29,90,180,270,105,195,285,119,209,103,193,283,143,155,140,157,144]
    sinais_mz = [103,129,143,169,244,218,231]
    
    # aplicando subtracao da massa exata para gerar os possiveis fragmentos
    list_frags = []
    frags = []
    for m in range(0, len(mz4steroid_subtracao)):
        frags.append(exact_mz - mz4steroid_subtracao[m])
    list_frags += [frags]
    frags = []
    
    # colocando pesos nas intensidade relativa na possição correção
    weight_df = pd.DataFrame(np.zeros((1,len(mz4steroid_subtracao)), dtype = int))
    colunas = [str(x) for x in mz4steroid_subtracao]
    weight_df.columns = colunas
    #weight_df
    
    # encontrando os index dos fragmentos presentes na amostra
    for ind, elementos in enumerate(mz_temp):
        if elementos in list_frags[0]:
            index_frag = list_frags[0].index(elementos)
            if rel_temp[ind] < 25.0:
                weight_df.iloc[0, index_frag] = 1
            elif rel_temp[ind] > 25.0 and rel_temp[ind] < 50:
                weight_df.iloc[0, index_frag] = 2
            else:
                weight_df.iloc[0, index_frag] = 3
        else:
                pass
    
    # weight_df
    # encontrando sinais mz
    weight_df2 = pd.DataFrame(np.zeros((1,len(sinais_mz)), dtype = int))
    colunas = [str(x) for x in sinais_mz]
    weight_df2.columns = colunas
    for ind, elementos in enumerate(mz_temp):
        if elementos in sinais_mz:
            index_frag = sinais_mz.index(elementos)
            if rel_temp[ind] < 25.0:
                weight_df2.iloc[0, index_frag] = 1
            elif rel_temp[ind] > 25.0 and rel_temp[ind] < 50:
                weight_df2.iloc[0, index_frag] = 2
            else:
                weight_df2.iloc[0, index_frag] = 3
        else:
            pass
    
    # encontrando peso da massa exata
    index_exact = mz_temp.index(exact_mz)
    intencity = rel_temp[index_exact]
    if intencity < 25.0:
        exact_weight = 1
    elif intencity > 25.0  and intencity < 50.0:
        exact_weight = 2
    else:
        exact_weight = 3
    
    # concatenando fragmentos e sinais m/z
    weight_df = weight_df.values.tolist()
    weight_df2 = weight_df2.values.tolist()
    list_final =list([exact_weight,*weight_df[0],*weight_df2[0]])
    
    
    return list_final


def run_anabolic_model(descriptor_ms):
    xgb_path = "app/config/data/ml_models/model_GBC_testo.sav"
    with open("app/config/data/ml_models/model_RFC_testo.sav", "rb") as f:
        _xgb = pickle.load(f)
    #result_rt = self._rf.predict([descriptor_ms])
    result_xgb = _xgb.predict([descriptor_ms])
    return result_xgb