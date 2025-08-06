from pathlib import Path
import mne


# PUT THIS IN THE MAIN SCRIPT
# sys.path.append("..")  # esto sube un nivel desde Scripts_visual_block


# # --- Configuración dinámica de rutas ---
# from get_paths_MOUS import get_paths_MOUS

# # Parámetros editables
# disco = "g"
# modality = "visual"
# layer_script = "block"
# subj = "sub-V1001"

# # Generar variables automáticamente
# path_dict = get_paths_MOUS(disco=disco, modality=modality, layer_script=layer_script, subj=subj)
# globals().update(path_dict)

# # Mostrar todos los paths generados
# print("\n📁 Rutas generadas:")
# for k, v in path_dict.items():
#     print(f"{k:<20} → {v}")


#INSTRUCTIONS:
# 1. Add the path
# 2. Add the mkdir
# 3. include the variable in the return

def get_paths_SELF(disco,layer_script,subj):
    # Carpeta general
    
    
    # Carpetas generales de datos
    # Carpeta general
    
    data_self = Path("F:\\WORKAREA\\Datos SELF\\")
    
    data_task_edf =  data_self / "Self_Exp2" / "Exp2_review" / "Visual_Corregidos" / "ICA" / "EDF"
    data_rest_edf = data_self /"data_rest_edf" 


    
    
    datadir = Path(f"{disco}:/PROYECTO_SELF/")

    # #carpetas generales de datos



    # Carpeta de preprocesado
    output_preproc = datadir / "output_preproc"
    channels_structure_path = datadir / "channels_structure"

    preproc_path = output_preproc / f"preproc_{layer_script}"
    preproc_path.mkdir(parents=True, exist_ok=True)

    # Subcarpetas preprocesado
    epochs_path = preproc_path / f"epochs_{layer_script}"
    ICA_path = preproc_path / f"ICA_{layer_script}"
    epochs_clean_path = preproc_path / f"epochs_clean_{layer_script}"
    epochs_matlab_path = preproc_path / f"epochs_matlab_{layer_script}"
    evoked_path = preproc_path / f"evoked_{layer_script}"
    #add mkdir paths
    for p in [epochs_path, ICA_path, epochs_clean_path,epochs_matlab_path, evoked_path]:
        p.mkdir(parents=True, exist_ok=True)
        print(f"✅ Carpeta creada: {p}")

    # Source folders
    output_source = datadir / "output_source"
    source_path = output_source / f"source_{layer_script}"
    raw_hsp_path = source_path / "raw_hsp"
    fwd_path = source_path / "fwd"
    inverse_path = source_path / "inverse"
    for p in [source_path, raw_hsp_path, fwd_path, inverse_path]:
        p.mkdir(parents=True, exist_ok=True)
        print(f"✅ Carpeta creada: {p}")


    # Analysis folders
    output_analysis = datadir / "output_analysis"
    analysis_path = output_analysis / f"analysis_{layer_script}"
    analysis_path.mkdir(parents=True, exist_ok=True)

    ACW_path = analysis_path / f"acw_{layer_script}"
    PLE_path = analysis_path / f"PLE_{layer_script}"
    ISC_path = analysis_path / f"ISC_{layer_script}"
    ISC_block_path = output_analysis / f"analysis_block" / f"ISC_block"
    
    for p in [ACW_path, PLE_path, ISC_path,ISC_block_path]:
        p.mkdir(parents=True, exist_ok=True)
        print(f"✅ Carpeta creada: {p}")




    return {
        "datadir": datadir,
        "data_self": data_self,
        "data_task_edf": data_task_edf,
        "data_rest_edf": data_rest_edf,
        "output_preproc": output_preproc,
        "preproc_path": preproc_path,
        "channels_structure_path": channels_structure_path,
        "epochs_path": epochs_path,
        "ICA_path": ICA_path,
        "epochs_clean_path": epochs_clean_path,
        "epochs_matlab_path": epochs_matlab_path,
    
        "evoked_path": evoked_path,

        "source_path": source_path,
        "raw_hsp_path": raw_hsp_path,
        "fwd_path": fwd_path,
        "inverse_path": inverse_path,

        "output_analysis": output_analysis,
        "analysis_path": analysis_path,
        "ACW_path": ACW_path,
        "PLE_path": PLE_path,
        "ISC_path": ISC_path,
        "ISC_block_path": ISC_block_path,
    }