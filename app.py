import os
import matplotlib
from flask import Flask, request, jsonify, render_template, send_file
import subprocess
import matplotlib.pyplot as plt
matplotlib.use("Agg")

app = Flask(__name__)
TMP_DIR = "/tmp"
IMG_DIR = os.path.join(TMP_DIR, "images")

# Crear directorios temporales si no existen
os.makedirs(IMG_DIR, exist_ok=True)

def get_data_filename(phi, ts):
    lista = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    lista2 = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    if ((phi in lista) and (ts in lista2)):
        return f"Sk_eta_{phi}00_Temp_{ts}0.dat"
    elif((phi in lista) and (ts not in lista2)):
        return f"Sk_eta_{phi}00_Temp_{ts}.dat"
    else:
        return f"Sk_eta_{phi}0_Temp_{ts}.dat"

def s_k_generic(phi, ts, index, output_filename, image_filename, title):
    path_file = os.path.join(TMP_DIR, get_data_filename(phi, ts))
    output_path = os.path.join(TMP_DIR, output_filename)
    image_path = os.path.join(IMG_DIR, image_filename)

    with open(path_file, "r") as Sks, open(output_path, "w") as output_file:
        y_values = []
        x_values = []

        for row in Sks:
            parts = row.split()
            t = parts[0]
            val = parts[index]

            output_file.write(f"{t}\t{val}\n")
            x_values.append(float(t))
            y_values.append(float(val))

    plt.plot(x_values, y_values)
    plt.title(title)
    plt.xlabel("k $\sigma $")
    plt.ylabel("S(k)")
    plt.savefig(image_path)
    plt.close()

def s_k_cc(phi, ts):
    s_k_generic(phi, ts, 1, "Sk_cc.dat", "S(k)_cc.png", "Structure Factor cation-cation")

def s_k_ca(phi, ts):
    s_k_generic(phi, ts, 2, "Sk_ca.dat", "S(k)_ca.png", "Structure Factor cation-anion")

def s_k_aa(phi, ts):
    s_k_generic(phi, ts, 3, "Sk_aa.dat", "S(k)_aa.png", "Structure Factor anion-anion")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    ratio = None
    asym = None
    S_k_cc = None
    S_k_ca = None
    S_k_aa = None
    select_option = None
    if request.method == "POST":
        big = float(request.form["big"])
        small = float(request.form["small"])
        phi = float(request.form["phi"])
        ts = float(request.form["ts"])
        select_option = request.form.get("Option")

        exe = "./structure_Apple_Silicon" if select_option == "Structure" else "./dynamics_Apple_Silicon"
        exe_path = os.path.join(TMP_DIR, exe)

        try:
            process = subprocess.Popen(
                [exe_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            input_data = f"{big}\n{small}\n{phi}\n{ts}"
            output, error = process.communicate(input=input_data)

            if process.returncode == 0:
                result = output.splitlines()[-1]
                ratio = round(big / small, 2)
                asym = round(ratio, 1)

                if select_option == "Structure":
                    s_k_cc(phi, ts)
                    s_k_ca(phi, ts)
                    s_k_aa(phi, ts)
            else:
                result = f"Error running Fortran: {error}"
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, rat=asym, S_k_aa=S_k_aa, S_k_ca=S_k_ca, S_k_cc=S_k_cc, select_option=select_option)

@app.route("/download_file_Sk_cc")
def download_file_Sk_cc():
    return send_file(os.path.join(TMP_DIR, "Sk_cc.dat"), as_attachment=True)

@app.route("/download_file_Sk_ca")
def download_file_Sk_ca():
    return send_file(os.path.join(TMP_DIR, "Sk_ca.dat"), as_attachment=True)

@app.route("/download_file_Sk_aa")
def download_file_Sk_aa():
    return send_file(os.path.join(TMP_DIR, "Sk_aa.dat"), as_attachment=True)

# Para producción, asegúrate de tener imágenes en la carpeta /tmp/images accesibles en el HTML
