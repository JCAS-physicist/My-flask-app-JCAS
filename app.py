import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, send_file, make_response
import subprocess
import tempfile
import os
import shutil
import time

app = Flask(__name__)

TMP_DIR = tempfile.gettempdir()
STATIC_TMP_DIR = os.path.join("static", "tmp")
os.makedirs(STATIC_TMP_DIR, exist_ok=True)

def prepare_executable(binary_name):
    local_bin_path = os.path.join(os.getcwd(), binary_name)
    tmp_bin_path = os.path.join(TMP_DIR, binary_name)

    if not os.path.exists(tmp_bin_path):
        shutil.copy(local_bin_path, tmp_bin_path)
        os.chmod(tmp_bin_path, 0o755)
    return tmp_bin_path


def s_k_cc(phi, ts):
    # --- Formateo igual que antes ---
    if phi < 1:
        phi_str = f"{phi:.3f}"
    else:
        phi_str = f"{int(phi) * 10}"

    if ts < 1:
        ts_str = f"{ts:.3f}"
    elif ts < 10:
        ts_str = f"{ts:.3f}"
    else:
        ts_str = f"{int(ts)}"

    # --- Archivo Structure Factor ---
    path_file = f"Sk_eta_{phi_str}_Temp_{ts_str}.dat"

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

    print("Máximo de S(k) cc:", max(Sdk_cc))

    img_tmp_path_cc = os.path.join(TMP_DIR, "Sk_cc.png")
    plt.plot(time, Sdk_cc)
    plt.title("Structure Factor cation-cation")
    plt.xlabel("k $\sigma $")
    plt.ylabel("S(k)")
    plt.savefig(img_tmp_path_cc)
    plt.close()

    img_static_path_cc = os.path.join(STATIC_TMP_DIR, "Sk_cc.png")
    shutil.copyfile(img_tmp_path_cc, img_static_path_cc)


    # --- Archivo MSD ---
    msd_filename = f"Wt_eta_{phi_str}_Temp_{ts_str}.dat"
    print("Buscando archivo MSD:", msd_filename)

    if not os.path.exists(msd_filename):
        print(f"Archivo MSD no encontrado: {msd_filename}")
        msd_img_path = None
    else:
        msd_a = []
        msd_c = []
        time_data = []

        with open(msd_filename, "r") as MSD_com:
            for linea in MSD_com:
                if linea.strip() == "":
                    continue
                parts = linea.split()
                if len(parts) < 3:
                    continue
                t, cation, anion = parts[0], parts[1], parts[2]
                time_data.append(float(t))
                msd_c.append(float(cation))
                msd_a.append(float(anion))

        # Guardar archivo .dat en TMP_DIR (opcional)
        msd_dat_path = os.path.join(TMP_DIR, "msd_jcas.dat")
        with open(msd_dat_path, "w") as f:
            for t, c, a in zip(time_data, msd_c, msd_a):
                f.write(f"{t}\t{c}\t{a}\n")

        # Generar gráfica MSD
        img_tmp_path_msd = os.path.join(TMP_DIR, "msd_jcas.png")
        plt.figure()
        plt.plot(time_data, msd_a, label="Anion", marker="o")
        plt.plot(time_data, msd_c, label="Cation", marker="s")
        plt.xscale("log")
        plt.yscale("log")
        plt.title("MSD")
        plt.xlabel("Time")
        plt.ylabel("MSD")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(img_tmp_path_msd)
        plt.close()

        img_static_path_msd = os.path.join(STATIC_TMP_DIR, "msd_jcas.png")
        shutil.copyfile(img_tmp_path_msd, img_static_path_msd)
        msd_img_path = "tmp/msd_jcas.png"

    # --- Retornar ambas rutas ---
    return "tmp/Sk_cc.png", msd_img_path

def s_k_ca(phi, ts):
    if phi < 1:
        phi_str = f"{phi:.3f}"  
    else:
        phi_str = f"{int(phi) * 10}"  

    if ts < 1:
        ts_str = f"{ts:.3f}" 
    elif ts < 10:
        ts_str = f"{ts:.3f}"
    else:
        ts_str = f"{int(ts)}"  

    path_file = f"Sk_eta_{phi_str}_Temp_{ts_str}.dat"

    with open(path_file, "r") as Sks:
        sk_ca_path = os.path.join(TMP_DIR, "Sk_ca.dat")
        with open(sk_ca_path, "w") as sk_ca:
            Sdk_ca = []
            time = []

            for columna in Sks:
                t = columna.split()[0]
                cation_anion = columna.split()[2]
                sk_ca.write(t + "\t" + cation_anion + "\n")
                time.append(float(t))
                Sdk_ca.append(float(cation_anion))

    img_tmp_path = os.path.join(TMP_DIR, "Sk_ca.png")
    plt.plot(time, Sdk_ca)
    plt.title("Structure Factor cation-anion")
    plt.xlabel("k $\sigma $")
    plt.ylabel("S(k)")
    plt.savefig(img_tmp_path)
    plt.close()

    img_static_path = os.path.join(STATIC_TMP_DIR, "Sk_ca.png")
    shutil.copyfile(img_tmp_path, img_static_path)
    return "tmp/Sk_ca.png"

def s_k_aa(phi, ts):
    if phi < 1:
        phi_str = f"{phi:.3f}"  
    else:
        phi_str = f"{int(phi) * 10}"  

    if ts < 1:
        ts_str = f"{ts:.3f}"
    elif ts < 10:
        ts_str = f"{ts:.3f}"
    else:
        ts_str = f"{int(ts)}"  

    path_file = f"Sk_eta_{phi_str}_Temp_{ts_str}.dat"

    with open(path_file, "r") as Sks:
        sk_aa_path = os.path.join(TMP_DIR, "Sk_aa.dat")
        with open(sk_aa_path, "w") as sk_aa:
            Sdk_aa = []
            time = []

            for columna in Sks:
                t = columna.split()[0]
                anion_anion = columna.split()[3]
                sk_aa.write(t + "\t" + anion_anion + "\n")
                time.append(float(t))
                Sdk_aa.append(float(anion_anion))

    img_tmp_path = os.path.join(TMP_DIR, "Sk_aa.png")
    plt.plot(time, Sdk_aa)
    plt.title("Structure Factor anion-anion")
    plt.xlabel("k $\sigma $")
    plt.ylabel("S(k)")
    plt.savefig(img_tmp_path)
    plt.close()

    img_static_path = os.path.join(STATIC_TMP_DIR, "Sk_aa.png")
    shutil.copyfile(img_tmp_path, img_static_path)
    return "tmp/Sk_aa.png"

def build_path(phi, ts):
    lista = [0.1 * i for i in range(1, 10)]
    lista2 = [0.01 * i for i in range(1, 10)]
    if ((phi in lista) and (ts in lista2)):
        return f"Sk_eta_{phi}00_Temp_{ts}0.dat"
    elif ((phi in lista) and (ts not in lista2)):
        return f"Sk_eta_{phi}00_Temp_{ts}.dat"
    else:
        return f"Sk_eta_{phi}0_Temp_{ts}.dat"

def build_msd_path(phi, ts):
    # Formatear phi
    if phi < 1:
        phi_str = f"{phi:.3f}"
    else:
        phi_str = f"{int(phi) * 10}"

    # Formatear ts
    if ts < 1:
        ts_str = f"{ts:.3f}"
    elif ts < 10:
        ts_str = f"{ts:.3f}"
    else:
        ts_str = f"{int(ts)}"

    # Construir el nombre del archivo
    filename = f"Wt_eta_{phi_str}_Temp_{ts_str}.dat"
    return filename

@app.route("/", methods=["GET", "POST"])
def index():
    phi = None
    ts = None
    result = None
    ratio = None
    asym = None
    S_k_cc_path = None
    S_k_ca_path = None
    S_k_aa_path = None
    msd_path = None
    select_option = None

    timestamp = str(time.time())
    
    if request.method == "POST":
        big = float(request.form["big"])
        small = float(request.form["small"])
        phi = float(request.form["phi"])
        ts = float(request.form["ts"])
        select_option = request.form.get("Option")

        bin_name = "structure" if select_option == "Structure" else "dynamics"
        bin_path = prepare_executable(bin_name)

        try:
            input_data = f"{big}\n{small}\n{phi}\n{ts}\n"
            process = subprocess.Popen(["/usr/bin/env", bin_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output, error = process.communicate(input=input_data)

            if process.returncode == 0:
                result = output.splitlines()[-1]
                ratio = round(big / small, 2)
                asym = round(ratio, 1)

                if select_option == "Structure":
                    S_k_cc_path, msd_path = s_k_cc(phi, ts)
                    S_k_ca_path = s_k_ca(phi, ts)
                    S_k_aa_path = s_k_aa(phi, ts)

                elif select_option == "dynamics":
                    S_k_cc_path, msd_path = s_k_cc(phi, ts)

            else:
                result = f"Error running Fortran: {error}"
        except Exception as e:
            result = f"Error: {str(e)}"

    html = render_template("index.html", result=result, rat=asym,
                               S_k_aa=S_k_aa_path, S_k_ca=S_k_ca_path,
                               S_k_cc=S_k_cc_path, msd=msd_path, select_option=select_option, timestamp=timestamp, phi=phi, ts=ts)
    response = make_response(html)
    response.cache_control.no_cache = True  # Asegura que no se cacheen
    return response

@app.route("/download_file_Sk_cc")
def download_file_Sk_cc():
    return send_file(os.path.join(TMP_DIR, "Sk_cc.dat"), as_attachment=True)

@app.route("/download_file_Sk_ca")
def download_file_Sk_ca():
    return send_file(os.path.join(TMP_DIR, "Sk_ca.dat"), as_attachment=True)

@app.route("/download_file_Sk_aa")
def download_file_Sk_aa():
    return send_file(os.path.join(TMP_DIR, "Sk_aa.dat"), as_attachment=True)

@app.route("/download_file_msd")
def download_file_msd():
    return send_file(os.path.join(TMP_DIR, "msd_jcas.dat"), as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True)
