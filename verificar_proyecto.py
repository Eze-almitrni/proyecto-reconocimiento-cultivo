"""
verificar_proyecto.py  -  Diagnóstico del proyecto (ejecutar ANTES de abrir los notebooks)
    python verificar_proyecto.py
Revisa: librerías instaladas, archivos en datos/, esquema de cada CSV y consistencia entre ellos.
"""
import importlib, sys
from pathlib import Path

import pandas as pd

OK, MAL, AVISO = "✅", "❌", "⚠️ "
problemas = []


def chequeo(cond, ok, mal, grave=True):
    print(f"  {OK if cond else (MAL if grave else AVISO)} {ok if cond else mal}")
    if not cond and grave:
        problemas.append(mal)
    return cond


print(f"Python {sys.version.split()[0]} | carpeta: {Path.cwd()}\n")
print("1) Librerías")
for lib, minimo in [("pandas", "2.0"), ("numpy", "1.24"), ("sklearn", "1.3"), ("scipy", "1.10"), ("matplotlib", "3.7"), ("seaborn", "0.12")]:
    try:
        v = importlib.import_module(lib).__version__
        chequeo(True, f"{lib} {v}", "")
    except ImportError:
        chequeo(False, "", f"Falta {lib}  →  pip install -r requirements.txt")

D = Path("datos")
print("\n2) Archivos en datos/")
chequeo(D.exists(), "carpeta datos/ encontrada", "No existe datos/: abrí la carpeta COMPLETA del proyecto (File > Open Folder)")


def leer(nombre):
    p = D / nombre
    return pd.read_csv(p, encoding="utf-8-sig") if p.exists() else None


A_COLS = ["Nitrógeno (N)", "Fósforo (P)", "Potasio (K)", "Temperatura (°C)", "Humedad (%)", "pH del suelo", "Precipitación (mm)", "Cultivo"]
tr, te, cr = leer("train.csv"), leer("test.csv"), leer("Crop_recommendation_castellano.csv")
for nom, df in [("train.csv", tr), ("test.csv", te), ("Crop_recommendation_castellano.csv", cr)]:
    if chequeo(df is not None, f"{nom}: {0 if df is None else len(df):,} filas", f"Falta datos/{nom}"):
        chequeo(list(df.columns) == A_COLS, "   columnas correctas", f"{nom}: columnas inesperadas {list(df.columns)}")
        chequeo(df.isna().sum().sum() == 0, "   sin nulos", f"{nom}: tiene nulos")
if tr is not None and te is not None:
    chequeo(len(tr) + len(te) == 2200 and tr.Cultivo.nunique() == 22, "train+test = 2.200 parcelas, 22 cultivos", "train/test no suman 2.200 filas o no tienen 22 cultivos")

B_COLS = ["Estado", "Distrito", "Anio", "Temporada", "Cultivo", "Area_ha", "Produccion_ton", "clave_repetida", "Rendimiento",
          "produccion_imputada", "produccion_nula_reportada", "unidad_comparable"]
for nom in ["crop_production_limpio_express.csv", "crop_production_limpio_castellano.csv"]:
    df = leer(nom)
    if chequeo(df is not None, f"{nom}: {0 if df is None else len(df):,} filas", f"Falta datos/{nom}", grave=(nom.endswith("express.csv"))):
        chequeo(list(df.columns) == B_COLS, "   columnas correctas", f"{nom}: columnas inesperadas")
        chequeo(len(df) == 244844, "   244.844 filas (esperado, sin duplicados de arroz)", f"{nom}: {len(df)} filas (se esperaban 244.844)", grave=False)

en = leer("cultivos_enriquecido_castellano.csv")
if chequeo(en is not None, f"cultivos_enriquecido_castellano.csv: {0 if en is None else len(en)} cultivos", "Falta datos/cultivos_enriquecido_castellano.csv"):
    chequeo({"cultivo", "rendimiento_mediano_t_ha"} <= set(en.columns), "   columnas correctas", "cultivos_enriquecido: faltan columnas")

dic = leer("diccionario_traduccion.csv")
chequeo(dic is not None, f"diccionario_traduccion.csv: {0 if dic is None else len(dic)} entradas", "Falta datos/diccionario_traduccion.csv", grave=False)

print("\n3) Archivo crudo (solo para Etapa2b_Taller)")
crudo = next((D / n for n in ("crop_production_india.csv", "crop_production.csv") if (D / n).exists()), None)
if crudo is None:
    print(f"  {AVISO}Falta datos/crop_production_india.csv (246.091 filas, columnas State_Name, District_Name, Crop_Year, Season, Crop, Area, Production).")
    print("     Es el archivo SUCIO original de la Etapa 1. Sin él NO se puede ejecutar el taller (Etapa2b); los otros 2 notebooks funcionan igual.")
else:
    n = len(pd.read_csv(crudo))
    chequeo(n == 246091, f"{crudo.name}: {n:,} filas", f"{crudo.name}: {n:,} filas (se esperaban 246.091)", grave=False)

print("\n" + ("🎉 TODO LISTO para ejecutar los notebooks." if not problemas else f"Hay {len(problemas)} problema(s) a resolver:\n  - " + "\n  - ".join(problemas)))
