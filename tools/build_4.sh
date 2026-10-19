#!/bin/bash
# Pipeline completa FASE 4 (ordine obbligatorio). Parte da index.html gia' ottenuto con build_3c + X-Men.
cd /home/claude/work && python3 tools/patch_dossier.py && python3 tools/patch_map3b.py && python3 tools/patch_cron3c.py \
 && python3 tools/patch_dossier4.py hook && python3 tools/inject_net.py && bash tools/build_restyle.sh && python3 tools/patch_dossier4.py inject && python3 tools/patch_fase1.py
