#!/bin/bash
# Pipeline completa FASE 3B (ordine obbligatorio)
cd /home/claude/work && python3 tools/patch_dossier.py && python3 tools/patch_map3b.py && python3 tools/inject_net.py && bash tools/build_restyle.sh
