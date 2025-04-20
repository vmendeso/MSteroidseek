from rdkit.Chem import rdDepictor
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
import base64

def __moltosvg(self, mol, molSize = (300,300), kekulize = True):
    mol = Chem.MolFromSmiles(mol)
    mc = Chem.Mol(mol.ToBinary())
    if kekulize:
        try:
            Chem.Kekulize(mc)
        except:
            mc = Chem.Mol(mol.ToBinary())
    if not mc.GetNumConformers():
        rdDepictor.Compute2DCoords(mc)
    drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0],molSize[1])
    drawer.DrawMolecule(mc)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    return svg.replace('svg:','')

# render svg    
def render_svg(self, smiles):
    svg = __moltosvg(self, mol=smiles)
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    #st.write(html, unsafe_allow_html=True)
    return(html)