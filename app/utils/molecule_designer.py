from rdkit.Chem import rdDepictor
from rdkit import Chem
from rdkit.Chem.Draw import rdMolDraw2D
import base64

def __moltosvg(smiles, molSize=(300, 300), kekulize=True):
    # Verificação de SMILES vazio ou inválido
    smiles = smiles.strip()
    if not smiles:
        print("[ERRO] SMILES vazio detectado.")
        return None

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"[ERRO] SMILES inválido: {smiles}")
        return None


    mc = Chem.Mol(mol.ToBinary())
    if kekulize:
        try:
            Chem.Kekulize(mc)
        except:
            mc = Chem.Mol(mol.ToBinary())
    if not mc.GetNumConformers():
        rdDepictor.Compute2DCoords(mc)

    drawer = rdMolDraw2D.MolDraw2DSVG(molSize[0], molSize[1])
    drawer.DrawMolecule(mc)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    return svg.replace('svg:', '')

# Renderiza o SVG como uma tag HTML <img>
def render_svg(smiles):
    svg = __moltosvg(smiles=smiles)
    if svg is None:
        return '<p style="color:red;">Erro ao renderizar a molécula (SMILES inválido).</p>'
    
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    return html
