##modules
#%matplotlib widget
#%matplotlib inline
#
# %matplotlib qt
import mne
import numpy as np

# Establecer un backend interactivo, como 'Qt5Agg', 'GTK3Agg', etc.
# Esto depende de los backends disponibles en tu sistema.
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')  # Asegúrate de que este backend está instalado.
mne.viz.set_browser_backend('qt')  # o 'matplotlib'

import pandas as pd 
import os
import sys

import re
from mne.preprocessing import ICA, corrmap, create_ecg_epochs, create_eog_epochs

from os.path import join as pathjoin
from time import time

from pathlib import Path

from autoreject import AutoReject

# aplicar la acf EN epochs

from statsmodels.tsa.stattools import acf
import numpy as np

import pandas as pd
sys.path.append("..")  # esto sube un nivel desde Scripts_visual_block

from scipy.io import savemat

import pickle

try:
    # Si se ejecuta como SCRIPT .py: usar __file__
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
except NameError:
    # Si se ejecuta como NOTEBOOK Jupyter: usar path relativo
    sys.path.append("..")  # sube un nivel desde la carpeta actual del notebook



# --- Configuración dinámica de rutas ---
from get_paths_SELF import get_paths_SELF

# Parámetros editables
disco = "g"
layer_script = "event"
subj = "s01b"
subj=sys.argv[1] 
# Generar variables automáticamente

path_dict = get_paths_SELF(disco=disco, layer_script=layer_script, subj=subj)
globals().update(path_dict)

# Mostrar todos los paths generados
print("\n📁 Rutas generadas:")
for k, v in path_dict.items():
    print(f"{k:<20} → {v}")


# Montage and read of edf file
# From BESA, two files come:

# **.edf**: Meaning: European Data Format, a standard for storing biomedical signals.. Contains Raw EEG signals (amplitudes in µV), sampling information, channel names, event markers, and other acquisition metadata.
 
# **.elp**:  Electrode Position file, a format that can store electrode positions in 2D or 3D coordinates, depending on the system and configuration. lectrode names and coordinates (Cartesian or spherical) either measured or estimated. In many EEG studies, these positions are not actually measured with a 3D digitizer (e.g., Polhemus) but are instead based on standard templates. Although this file is available, it lacks the Z coordinate, so we cannot use it to reconstruct full 3D electrode positions. Instead, we applied a standard montage from MNE for the Brain Vision EasyCap-M1 cap, which reflects the typical electrode layout for our system.




# In our EEG setup, electrode positions were not measured individually using a 3D digitizer (e.g., Polhemus). Instead, we applied a standard montage corresponding to the Brain Vision EasyCap-M1 cap, which matches the typical 64-channel layout used in our recordings. This approach assumes that the electrodes are placed according to the 10–10 system, which is standard practice in EEG studies and sufficient for analyses in sensor space, such as ERP or spectral analysis. The reference electrode M1 was excluded from the dataset as it is not used in subsequent analyses.

edf_file = data_task_edf / f"{subj}_vis_c_BVica-export.edf"
elp_file = data_task_edf / f"{subj}_vis_c_BVica-export.elp"

# -------------------------
# 2. Leer EDF
# -------------------------

# Leer el EDF
raw = mne.io.read_raw_edf(edf_file, preload=True)



# Ahora aplicar el montaje estándar
montage = mne.channels.make_standard_montage("easycap-M1")
raw.rename_channels(lambda name: name.replace("EEG ", "").replace("-Ref", ""))

# Eliminar el canal M1
if "M1" in raw.ch_names:
    raw.drop_channels(["M1"])
raw.set_montage(montage, on_missing='ignore')

# Plotear



# plots
# raw.plot()
# raw.plot_sensors(kind="3d", show_names=True)
# raw.plot_sensors(kind="topomap", show_names=True)

# Filtrado
low_pass=50
high_pass=0.5

raw_high_low_pass = raw.filter(l_freq=low_pass, h_freq=high_pass, n_jobs=5, verbose=True)

# Creating Events

### correspondencia triggers
# # - 1 a 3 – cara self
# # - 4 a 6 – cara friend
# # - 7 a 9 – cara unknown


# # - *6 – imagen emocional negativa
# # - *5 – imagen emocional neutra
# # - *4 – imagen emocional positiva

# # Ej. S 76: imagen negativa precedida por una cara desconocida

# # Vamos a cortar los estímulos desde cada imagen emocional 14,54,95...

# # Vamos a agrupar los estímulos en:(para self)

# # - 14,24,34: self_pos
# # - 15,25,35: self_neg
# # - 16, 26, 36: self_neu



self_faces = range(1, 4)      # 1, 2, 3
friend_faces = range(4, 7)    # 4, 5, 6
unknown_faces = range(7, 10)  # 7, 8, 9


# Extraer eventos desde las anotaciones
events, event_id = mne.events_from_annotations(raw)


# Mostrar los IDs de eventos detectados
print("Diccionario de eventos:", event_id)

# Graficar distribución de eventos en el tiempo
# Rangos
self_faces = range(1, 4)      # 1, 2, 3
friend_faces = range(4, 7)    # 4, 5, 6
unknown_faces = range(7, 10)  # 7, 8, 9


for i in self_faces:
    print(f"self_faces: {i}")
    
for i in friend_faces:
    print(f"friend_faces: {i}")
    
for i in unknown_faces:
    print(f"unknown_faces: {i}")
    
    
# Tipos de imagen
POS = 4
NEU = 5
NEG = 6

# Generar listas
self_pos = [f"{face}{POS}" for face in self_faces]
self_neu = [f"{face}{NEU}" for face in self_faces]
self_neg = [f"{face}{NEG}" for face in self_faces]

friend_pos = [f"{face}{POS}" for face in friend_faces]
friend_neu = [f"{face}{NEU}" for face in friend_faces]
friend_neg = [f"{face}{NEG}" for face in friend_faces]

unk_pos = [f"{face}{POS}" for face in unknown_faces]
unk_neu = [f"{face}{NEU}" for face in unknown_faces]
unk_neg = [f"{face}{NEG}" for face in unknown_faces]

dict_conditions = {
    'self_pos': self_pos,
    'self_neu': self_neu,
    'self_neg': self_neg,
    'friend_pos': friend_pos,
    'friend_neu': friend_neu,
    'friend_neg': friend_neg,
    'unk_pos': unk_pos,
    'unk_neu': unk_neu,
    'unk_neg': unk_neg
}

# Ejemplo de uso
print(f"Dict Conditions:")  # ['14', '24', '34']
print(dict_conditions)  # ['14', '24', '34']


for clave, valor in dict_conditions.items():
    print(clave)


pickle_file = epochs_clean_path / f"dict_conditions.pkl"

# Guardar dict_annotations
with open(pickle_file, "wb") as f:
    pickle.dump(dict_conditions, f)
annotations=raw.annotations

original_annotations=raw.annotations.copy()
# Inicializar listas para nuevas anotaciones
onsets, durations, descriptions = [], [], []

trigger_str_list=[]
# Recorrer SOLO anotaciones válidas
for num in range(len(annotations)):
    annotation=annotations.description[num]
    trigger_str = re.sub(r'^Trigger-', '', str(annotation))  # '11'
    # print(f"{trigger_str} and type= {type(trigger_str)}")
    label=[]
    if trigger_str in self_pos:
        label = 'self_pos'
    elif trigger_str in self_neu:
        label = 'self_neu'
    elif trigger_str in self_neg:
        label = 'self_neg'
    elif trigger_str in friend_pos:
        label = 'friend_pos'
    elif trigger_str in friend_neu:
        label = 'friend_neu'
    elif trigger_str in friend_neg:
        label = 'friend_neg'
    elif trigger_str in unk_pos:
        label = 'unk_pos'
    elif trigger_str in unk_neu:
        label = 'unk_neu'
    elif trigger_str in unk_neg:
        label = 'unk_neg'

    trigger_str_list.append(trigger_str)

    if label:
        onsets.append(annotations[num]['onset'])
        durations.append(annotations[num]['duration'])
        descriptions.append(label)


# Crear nuevas anotaciones
new_annotations = mne.Annotations(
    onset=onsets,
    duration=durations,
    description=descriptions,
    orig_time=raw.annotations.orig_time
)


print(f"Se crearon {len(new_annotations)} anotaciones nuevas.")


# Asignar al raw
raw.set_annotations(raw.annotations + new_annotations)




## Chek que coinciden las anottations

for categoria, triggers in dict_conditions.items():
    # 1. Onsets de triggers originales de esa categoría
    onsets_original = [
        ann['onset']
        for ann in original_annotations
        if re.sub(r'^Trigger-', '', str(ann['description'])) in triggers
    ]
    
    # 2. Onsets de anotaciones categorizadas
    onsets_cat = [
        ann['onset']
        for ann in raw.annotations
        if str(ann['description']) == categoria
    ]
    
    # 3. Comparar
    if np.allclose(sorted(onsets_original), sorted(onsets_cat)):
        print(f"✅ {categoria} coincide con los triggers originales {triggers}")
    else:
        print(f"❌ {categoria} NO coincide con los triggers originales {triggers}")
        diff1 = set(onsets_original) - set(onsets_cat)
        diff2 = set(onsets_cat) - set(onsets_original)
        if diff1:
            print(f"   - En originales pero no en {categoria}: {diff1}")
        if diff2:
            print(f"   - En {categoria} pero no en originales: {diff2}")
for categoria, triggers in dict_conditions.items():
    # 1. Contar ocurrencias de cada trigger en originales
    trigger_counts_original = {
        trig: sum(
            re.sub(r'^Trigger-', '', str(ann['description'])) == trig
            for ann in original_annotations
        )
        for trig in triggers
    }
    
    # 2. Contar ocurrencias de la categoría en anotaciones nuevas
    cat_count = sum(
        str(ann['description']) == categoria
        for ann in raw.annotations
    )
    
    # 3. Mostrar resultados
    print(f"\n🔍 {categoria}")
    print(f"   Originales: {trigger_counts_original} (total={sum(trigger_counts_original.values())})")
    print(f"   Total {categoria}: {cat_count}")
    
    # 4. Comprobar coincidencia total
    if sum(trigger_counts_original.values()) == cat_count:
        print(f"✅ Coincide en total")
    else:
        print(f"❌ NO coincide en total")
# Epoching
# 1. Convertir anotaciones a eventos

dict_epochs={}
events, event_id = mne.events_from_annotations(raw)

for clave, valor in dict_conditions.items():

    # 3. Crear epochs solo para self_pos
    dict_epochs[clave] = mne.Epochs(
        raw,
        events,
        event_id={f"{clave}": event_id[f"{clave}"]},  # Solo esta categoría
        tmin=-0.5,   
        tmax=9,   
        baseline=(-0.5, 0),  # Baseline desde el inicio del epoch hasta 0 s
        preload=True,
        reject_by_annotation=None
    )


for clave, epochs in dict_epochs.items():


    ar = AutoReject(random_state=73, n_jobs=15, verbose= True,)
    ar.fit(epochs)  # fit on a few epochs to save time

    print("After AutoReject fitting:")
    epochs_ar, reject_log = ar.transform(epochs, return_log=True)  # Aplicación de la transformación

    print(f"bads {epochs_ar.info['bads']}")

    epochs_ar.save(epochs_clean_path/f"{subj}_epochs_{clave}_{layer_script}-epo.fif", split_size='1.8GB', overwrite=True)


    fig = reject_log.plot("vertical", show_names=50, aspect="equal", show=False)
    reject_log.save(epochs_clean_path/f"{subj}_reject_log_1_{clave}_{layer_script}.npz", overwrite=True)
    fig_path = epochs_clean_path / f"{subj}_reject_log_{clave}_{layer_script}.png"
    fig.savefig(fig_path)
    fig.clf()
    plt.close(fig)
    
    
    
        # Crear estructura FieldTrip
    ft_data = {}
    ft_data['trial'] = [trial for trial in epochs_ar.get_data().transpose(0, 2, 1)]
    times = epochs_ar.times.tolist()
    ft_data['time'] = [times for _ in range(len(epochs_ar))]
    ft_data['label'] = epochs_ar.ch_names
    ft_data['fsample'] = float(epochs_ar.info['sfreq'])

    # Crear nombre de archivo
    filename = epochs_matlab_path / f"{subj}_epochs_{clave}_{layer_script}.mat"

    # Guardar como struct en .mat
    savemat(filename, {'data': ft_data})
    print(f"✅ Exportado {filename} en formato FieldTrip.")
    
    del epochs_ar, reject_log, fig, ft_data  # Liberar memoria
    
    
    
    



        