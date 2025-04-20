from rdkit import Chem
from rdkit.Chem import Descriptors

def n4cycleFilter(var):
        mol = []
        smi = []
        steroids =[]
        steroids_index = []
        sim_ = []
        for smiles, sims_ in var.items():
        #for i in range(0 ,len(df['Smiles'])):
            mol.append(Chem.MolFromSmiles(smiles))
            sim_.append(sims_)
        for i,z in enumerate(mol):
            try:
                nali = Descriptors.NumAliphaticCarbocycles(z)
            except:
                pass
            if nali == 4:
                steroids_index.append(i)
                smi.append(Chem.MolToSmiles(z)) 
            
        return smi, sim_  