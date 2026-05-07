import json
from datetime import datetime
import subprocess

# Cargar datos
with open("datos_ranking.json", encoding="utf-8") as f:
    data = json.load(f)

fecha_hoy = datetime.now().strftime("%d de %B de %Y")

# ================== GENERAR HTML ==================
html = f'''<h2 style="color: #134e5e; font-family: Arial, Helvetica, sans-serif; text-align: center; margin-bottom: 8px;">
  Ranking Top 8 Modelos Open Weights / iA Local
</h2>
<p style="text-align: center; color: #555; font-family: Arial, Helvetica, sans-serif;">
  <strong>Actualizado:</strong> {fecha_hoy}
</p>

<table border="1" cellpadding="12" cellspacing="0" style="border-collapse: collapse; width: 100%; max-width: 1250px; margin: 20px auto; font-family: Arial, Helvetica, sans-serif; border: 1px solid #ddd; background-color: #f9f7f2;">
  <thead>
    <tr style="background-color: #1e6b7e; color: white;">
      <th style="width: 6%; text-align: center;">Posición</th>
      <th style="width: 24%;">Modelo</th>
      <th style="width: 37%;">Descripción / Fortalezas principales</th>
      <th style="width: 8%; text-align: center;">Score</th>
      <th style="width: 11%; text-align: center;">VRAM (Q4/Q5)</th>
      <th style="width: 14%; text-align: center;">Plataformas</th>
    </tr>
  </thead>
  <tbody>
'''

for m in data["modelos"]:
    bg = '#ffffff' if m['posicion'] % 2 == 1 else '#f8f5f0'
    html += f'''
    <tr style="background-color: {bg};">
      <td align="center"><strong>{m['posicion']}</strong></td>
      <td><strong>{m['modelo']}</strong><br><small>{m.get('compania', '')}</small></td>
      <td>{m['descripcion']}</td>
      <td align="center"><strong>{m['score']}</strong></td>
      <td align="center">{m['vram']}</td>
      <td align="center">Ollama · LM Studio · Jan</td>
    </tr>
'''

html += '''
  </tbody>
</table>

<p style="text-align: center; color: #555; font-size: 0.9em; margin-top: 15px;">
  <strong>Nota:</strong> Todos los modelos son <strong>Open Weights</strong> con licencias permisivas (Apache 2.0 / MIT).<sup>*</sup><br>
  Los scores son compuestos basados en leaderboards públicos. 
  <a href="https://onyx.app/self-hosted-llm-leaderboard" target="_blank" style="color: #134e5e;">Ver leaderboards →</a>
</p>

<p style="text-align: center; font-size: 0.85em; color: #777;">
  * Open Weights = Se liberan los pesos entrenados del modelo (permite uso local y fine-tuning), pero no el código completo de entrenamiento ni los datos originales.
</p>
'''

with open("ranking_ia_local.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ Ranking generado - {fecha_hoy}")

# Push automático a GitHub
try:
    subprocess.run(["git", "add", "ranking_ia_local.html"], check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", f"Actualización ranking iA Local - {fecha_hoy}"], check=True, capture_output=True)
    subprocess.run(["git", "push"], check=True, capture_output=True)
    print("🚀 Push automático a GitHub completado")
except Exception:
    print("⚠️ Push no realizado (primera vez o sin cambios)")
    