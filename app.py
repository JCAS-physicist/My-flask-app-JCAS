import matplotlib
import os
import shutil
import tempfile
import stat
import subprocess
from flask import Flask, request, jsonify, render_template, send_file
import matplotlib.pyplot as plt

matplotlib.use("Agg")

app = Flask(__name__)
TMP_DIR = "/tmp"


structure_exec_path = os.path.join(TMP_DIR, "structure_Apple_Silicon")
if not os.path.exists(structure_exec_path):
    shutil.copy("./structure_Apple_Silicon", structure_exec_path)
    os.chmod(structure_exec_path, 0o755)

process = subprocess.Popen(
    [structure_exec_path],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)


def ensure_datafile_in_tmp(filename):
    src_path = os.path.abspath(filename)
    dst_path = os.path.join(TMP_DIR, filename)
    if not os.path.exists(dst_path):
        shutil.copy(src_path, dst_path)
    return dst_path


def ensure_executable_in_tmp(filename):
    src_path = os.path.abspath(filename)
    dst_path = os.path.join(TMP_DIR, filename)
    if not os.path.exists(dst_path):
        shutil.copy(src_path, dst_path)
        os.chmod(dst_path, os.stat(dst_path).st_mode | stat.S_IEXEC)
    return dst_path

# Tus funciones s_k_cc, s_k_ca, s_k_aa permanecen igual,
# pero asegurándote que las rutas a los archivos de entrada/salida
# también estén en /tmp para evitar errores de permisos

def s_k_cc(phi, ts):
    import tempfile
    import os

    TMP_DIR = tempfile.gettempdir()

    lista = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    lista2 = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    if ((phi in lista) and (ts in lista2)):
        path_file = f"Sk_eta_{phi}00_Temp_{ts}0.dat"
    elif((phi in lista) and (ts not in lista2)):
        path_file = f"Sk_eta_{phi}00_Temp_{ts}.dat"
    else:
        path_file = f"Sk_eta_{phi}0_Temp_{ts}.dat"

    with open(path_file, "r") as Sks:
        sk_cc_path = os.path.join(TMP_DIR, "Sk_cc.dat")
        with open(sk_cc_path, "w") as sk_cc:
            Sdk_cc = []
            time = []

            for columna in Sks:
                t = columna.split()[0]
                cation_cation = columna.split()[1]

                sk_cc.write(t + "\t" + cation_cation + "\n")
                time.append(float(t))
                Sdk_cc.append(float(cation_cation))

    # Guardar imagen en /tmp
    plt.plot(time, Sdk_cc)
    plt.title("Structure Factor cation-cation")
    plt.xlabel("k $\sigma $")
    plt.ylabel("S(k)")
    plot_path = os.path.join(TMP_DIR, "S(k)_cc.png")
    plt.savefig(plot_path)
    plt.close()

    return sk_cc_path  # Devuelve la ruta completa

def s_k_cc(phi, ts):
    TMP_DIR = tempfile.gettempdir()

    lista = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    lista2 = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    if ((phi in lista) and (ts in lista2)):
        path_file = f"Sk_eta_{phi}00_Temp_{ts}0.dat"
    elif((phi in lista) and (ts not in lista2)):
        path_file = f"Sk_eta_{phi}00_Temp_{ts}.dat"
    else:
        path_file = f"Sk_eta_{phi}0_Temp_{ts}.dat"

    with open(path_file, "r") as Sks:
        sk_cc_path = os.path.join(TMP_DIR, "Sk_cc.dat")
        with open(sk_cc_path, "w") as sk_cc:
            Sdk_cc = []
            time = []

            for columna in Sks:
                t = columna.split()[0]
                cation_cation = columna.split()[1]

                sk_cc.write(t + "\t" + cation_cation + "\n")
                time.append(float(t))
                Sdk_cc.append(float(cation_cation))

    # Guardar imagen en /tmp
    plt.plot(time, Sdk_cc)
    plt.title("Structure Factor cation-cation")
    plt.xlabel("k $\sigma $")
    plt.ylabel("S(k)")
    plot_path = os.path.join(TMP_DIR, "S(k)_cc.png")
    plt.savefig(plot_path)
    plt.close()

    return sk_cc_path  # Devuelve la ruta completa

def s_k_ca(phi, ts):
    TMP_DIR = tempfile.gettempdir()

    lista = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    lista2 = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    if ((phi in lista) and (ts in lista2)):
        path_file = f"Sk_eta_{phi}00_Temp_{ts}0.dat"
    elif((phi in lista) and (ts not in lista2)):
        path_file = f"Sk_eta_{phi}00_Temp_{ts}.dat"
    else:
        path_file = f"Sk_eta_{phi}0_Temp_{ts}.dat"

    with open(path_file, "r") as Sks:
        sk_ca_path = os.path.join(TMP_DIR, "Sk_ca.dat")
        with open(sk_ca_path, "w") as sk_ca:
            Sdk_ca = []
            time = []

            for columna in Sks:
                t = columna.split()[0]
                cation_anion = columna.split()[1]

                sk_ca.write(t + "\t" + cation_anion + "\n")
                time.append(float(t))
                Sdk_ca.append(float(cation_anion))

    # Guardar imagen en /tmp
    plt.plot(time, Sdk_ca)
    plt.title("Structure Factor cation-cation")
    plt.xlabel("k $\sigma $")
    plt.ylabel("S(k)")
    plot_path = os.path.join(TMP_DIR, "S(k)_ca.png")
    plt.savefig(plot_path)
    plt.close()

    return sk_ca_path  # Devuelve la ruta completa

def build_data_filename(phi, ts):
    lista = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    lista2 = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
    if ((phi in lista) and (ts in lista2)):
        return f"Sk_eta_{phi}00_Temp_{ts}0.dat"
    elif ((phi in lista) and (ts not in lista2)):
        return f"Sk_eta_{phi}00_Temp_{ts}.dat"
    else:
        return f"Sk_eta_{phi}0_Temp_{ts}.dat"



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

        TMP_DIR = tempfile.gettempdir()  # /tmp

        if select_option == "Structure":
            try:
                # Ruta original del ejecutable
                original_path = "./structure_Apple_Silicon"
                # Ruta en el directorio temporal
                structure_exec_path = os.path.join(TMP_DIR, "structure_Apple_Silicon")

                # Copiar el ejecutable si no está en /tmp y darle permisos
                if not os.path.exists(structure_exec_path):
                    shutil.copy(original_path, structure_exec_path)
                    os.chmod(structure_exec_path, 0o755)

                # Ejecutar el programa
                process = subprocess.Popen(
                    [structure_exec_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                input_data = f"{big}\n{small}\n{phi}\n{ts}"
                output, error = process.communicate(input=input_data)

                if process.returncode == 0:
                    result = output.splitlines()[-1]
                    ratio = round(big / small, 2)
                    asym = round(ratio, 1)
                    S_k_cc = s_k_cc(phi, ts)
                    S_k_ca = s_k_ca(phi, ts)
                    S_k_aa = s_k_aa(phi, ts)
                else:
                    result = f"Error running Fortran: {error}"

            except Exception as e:
                result = f"Error: {str(e)}"

        else:
            try:
                # Ruta del ejecutable dynamics
                dynamics_exec_path = os.path.join(TMP_DIR, "dynamics_Apple_Silicon")
                if not os.path.exists(dynamics_exec_path):
                    shutil.copy("./dynamics_Apple_Silicon", dynamics_exec_path)
                    os.chmod(dynamics_exec_path, 0o755)

                process = subprocess.Popen(
                    [dynamics_exec_path],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )

                input_data = f"{big}\n{small}\n{phi}\n{ts}"
                output, error = process.communicate(input=input_data)

                if process.returncode == 0:
                    result = output.splitlines()[-1]
                    ratio = round(big / small, 2)
                    asym = round(ratio, 1)
                else:
                    result = f"Error running Fortran: {error}"

            except Exception as e:
                result = f"Error: {str(e)}"

    return render_template("index.html", result=result, rat=asym, S_k_aa=S_k_aa, S_k_ca=S_k_ca, S_k_cc=S_k_cc, select_option=select_option)


@app.route("/download_file_Sk_cc")
def download_file_Sk_cc():
    path = os.path.join(tempfile.gettempdir(), "Sk_cc.dat")
    return send_file(path, as_attachment=True)

@app.route("/download_file_Sk_ca")
def download_file_Sk_ca():
    path = os.path.join(tempfile.gettempdir(), "Sk_ca.dat")
    return send_file(path, as_attachment=True)

@app.route("/download_file_Sk_aa")
def download_file_Sk_aa():
    path = os.path.join(tempfile.gettempdir(), "Sk_aa.dat")
    return send_file(path, as_attachment=True)
