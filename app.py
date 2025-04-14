import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from flask import Flask, request, render_template, send_file
import subprocess
import tempfile
import os
import shutil

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
    path_file = build_path(phi, ts)

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

    img_tmp_path = os.path.join(TMP_DIR, "S(k)_cc.png")
    plt.plot(time, Sdk_cc)
    plt.title("Structure Factor cation-cation")
    plt.xlabel("k $\\sigma $")
    plt.ylabel("S(k)")
    plt.savefig(img_tmp_path)
    plt.close()

    img_static_path = os.path.join(STATIC_TMP_DIR, "S(k)_cc.png")
    shutil.copyfile(img_tmp_path, img_static_path)
    return "tmp/S(k)_cc.png"

def s_k_ca(phi, ts):
    path_file = build_path(phi, ts)

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

    img_tmp_path = os.path.join(TMP_DIR, "S(k)_ca.png")
    plt.plot(time, Sdk_ca)
    plt.title("Structure Factor cation-anion")
    plt.xlabel("k $\\sigma $")
    plt.ylabel("S(k)")
    plt.savefig(img_tmp_path)
    plt.close()

    img_static_path = os.path.join(STATIC_TMP_DIR, "S(k)_ca.png")
    shutil.copyfile(img_tmp_path, img_static_path)
    return "tmp/S(k)_ca.png"

def s_k_aa(phi, ts):
    path_file = build_path(phi, ts)

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

    img_tmp_path = os.path.join(TMP_DIR, "S(k)_aa.png")
    plt.plot(time, Sdk_aa)
    plt.title("Structure Factor anion-anion")
    plt.xlabel("k $\\sigma $")
    plt.ylabel("S(k)")
    plt.savefig(img_tmp_path)
    plt.close()

    img_static_path = os.path.join(STATIC_TMP_DIR, "S(k)_aa.png")
    shutil.copyfile(img_tmp_path, img_static_path)
    return "tmp/S(k)_aa.png"

def build_path(phi, ts):
    lista = [0.1 * i for i in range(1, 10)]
    lista2 = [0.01 * i for i in range(1, 10)]
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
    S_k_cc_path = None
    S_k_ca_path = None
    S_k_aa_path = None
    select_option = None

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
                    S_k_cc_path = s_k_cc(phi, ts)
                    S_k_ca_path = s_k_ca(phi, ts)
                    S_k_aa_path = s_k_aa(phi, ts)
            else:
                result = f"Error running Fortran: {error}"
        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template("index.html", result=result, rat=asym,
                           S_k_aa=S_k_aa_path, S_k_ca=S_k_ca_path,
                           S_k_cc=S_k_cc_path, select_option=select_option)

@app.route("/download_file_Sk_cc")
def download_file_Sk_cc():
    return send_file(os.path.join(TMP_DIR, "Sk_cc.dat"), as_attachment=True)

@app.route("/download_file_Sk_ca")
def download_file_Sk_ca():
    return send_file(os.path.join(TMP_DIR, "Sk_ca.dat"), as_attachment=True)

@app.route("/download_file_Sk_aa")
def download_file_Sk_aa():
    return send_file(os.path.join(TMP_DIR, "Sk_aa.dat"), as_attachment=True)

# if __name__ == "__main__":
#     app.run(debug=True)
