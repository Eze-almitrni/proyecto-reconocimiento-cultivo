# 🌾 Etapa 2 – Aprendizaje Supervisado y No Supervisado (Sistema de recomendación de cultivos)

## Estructura de la carpeta
```
Proyecto_Etapa2/
├── Etapa2_Aprendizaje_Supervisado_y_No_Supervisado.ipynb   ← notebook PRINCIPAL (completo)
├── Etapa2_Version_Resumida_RF_y_KMeans.ipynb               ← versión corta: Random Forest + K-Means
├── Etapa2b_Taller_Limpieza_Datos_Sucios.ipynb              ← taller de limpieza (necesita el archivo CRUDO, ver abajo)
├── verificar_proyecto.py                                   ← diagnóstico: ejecutalo primero
├── requirements.txt
├── datos/                                                  ← TODOS los CSV
│   ├── train.csv, test.csv                                 (Dataset A, 1.760 + 440 parcelas, ya en castellano)
│   ├── Crop_recommendation_castellano.csv                  (Dataset A completo, 2.200 parcelas)
│   ├── crop_production_limpio_express.csv                  (Dataset B limpio, inglés, 244.844 filas)
│   ├── crop_production_limpio_castellano.csv               (Dataset B limpio, castellano)
│   ├── cultivos_enriquecido_castellano.csv                 (rendimiento mediano real por cultivo)
│   ├── diccionario_traduccion.csv                          (inglés → castellano)
│   └── crop_production_india.csv                           ⚠️ FALTA: ver "Único archivo pendiente"
├── salida/                                                 ← lo que generan los notebooks
└── docs/info_avances.txt                                   ← tus notas de avance
```

## Cómo ejecutarlo en VS Code (paso a paso)
1. Descomprimí el zip y abrí la carpeta **completa**: `File → Open Folder → Proyecto_Etapa2` (no abras solo un `.ipynb`).
2. Terminal de VS Code (`Ctrl+ñ`):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate          # Windows   |   source .venv/bin/activate   # Mac/Linux
   pip install -r requirements.txt
   python verificar_proyecto.py    # debe terminar en 🎉 TODO LISTO
   ```
3. Abrí un notebook → arriba a la derecha **Select Kernel → Python Environments → .venv** → **Run All**.
4. Orden sugerido: Principal (o la Resumida) → Taller. El principal **no depende** del taller.

Tiempos aproximados (PC normal): Resumida 1–2 min · Principal 4–6 min.

## Qué corregí para que funcione (importante)
| Problema encontrado | Efecto si no se corregía | Solución |
|---|---|---|
| `train.csv` y `test.csv` ya vienen **traducidos**, pero el notebook los traducía con `.map(CULT_A)` | La columna `Cultivo` quedaba **100 % vacía (NaN)** y todo el modelado fallaba | Ahora usa `.replace(...)`: acepta archivos en inglés **o** ya en castellano |
| Los notebooks pedían `crop_production_LIMPIO.csv`, `cultivos_enriquecido.csv`, `Crop_recommendation.csv` (nombres que no tenés) | `FileNotFoundError` | Función `ruta()` que busca en `datos/` y acepta los nombres alternativos que sí tenés |
| `cultivos_enriquecido_castellano.csv` tiene **otro esquema** que el esperado (`cultivo_etapa1`, `rendimiento_mediano`) | Error en la recomendación Top‑3 | La celda detecta ambos esquemas |
| Los CSV limpios no traen la columna `yield_outlier` | `AttributeError: rendimiento_atipico` | Se recalcula con la regla de la Etapa 1‑B (IQR×3 por cultivo). **Reproduce exactamente** tus 231.248 filas confiables y los conteos por cultivo |
| Código pensado para Colab (`files.upload()`) | Carga rota en VS Code | Reemplazado por búsqueda de archivos con mensajes de error claros |
| Los notebooks escribían CSV sueltos en la carpeta | Desorden / sobrescribir datos | Todo lo generado va a `salida/` |

## Verificación realizada
- Principal y Resumida ejecutados **de punta a punta sin errores** (17 y 7 gráficos).
- Todo el **Dataset A** (clasificación con 6 algoritmos, PCA, K‑Means, jerárquico, mezcla gaussiana) da **exactamente los mismos resultados** que tus corridas guardadas (99,5 % de acierto, etc.).
- Dataset B (regresión y regiones agrícolas): ver la tabla de coincidencia en el mensaje de entrega.
- Taller: rutas, carga y guardado probados; ver "Único archivo pendiente".

## ⚠️ Único archivo pendiente: `crop_production_india.csv`
El Taller de limpieza trabaja con el archivo **crudo y sucio** (246.091 filas; columnas `State_Name, District_Name, Crop_Year, Season, Crop, Area, Production`), es decir, el original de la Etapa 1 **antes** de limpiarlo. No se puede reconstruir a partir de los archivos limpios, y no estaba entre los que subiste. Copialo a `datos/` con ese nombre (se acepta también `crop_production.csv`) y ejecutá `python verificar_proyecto.py`: te confirma si tiene las 246.091 filas esperadas. **Los otros dos notebooks funcionan sin él.** El taller además baja el dataset Titanic de internet (si no hay conexión, esa parte se omite sola).

## Solución de problemas
| Mensaje | Qué hacer |
|---|---|
| `FileNotFoundError: No encuentro '...'` | Abriste el notebook fuera de la carpeta del proyecto. Usá *Open Folder* y corré `verificar_proyecto.py` |
| `ModuleNotFoundError` | Kernel equivocado: elegí `.venv` y `pip install -r requirements.txt` |
| `OneHotEncoder ... sparse_output` | scikit‑learn viejo: `pip install -U scikit-learn` (se necesita ≥ 1.3) |
| Excel muestra todo en una columna | Los CSV usan `,` y UTF‑8; importalos con *Datos → Desde texto/CSV*, no con doble clic |

## Límites a decir de entrada (ya están en tus notebooks)
El Dataset A es “demasiado perfecto” (exactamente 100 casos por cultivo): el ~99 % no se trasladaría a un campo real. El orden por rendimiento (t/ha) no es orden por conveniencia: falta el precio.
