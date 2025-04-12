import matplotlib
from flask import Flask, request, jsonify, render_template_string, render_template, send_file
import subprocess
import matplotlib.pyplot as plt
matplotlib.use("Agg")



app = Flask(__name__)

def s_k_cc(phi, ts):
lista =[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
lista2 =[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
if ((phi in lista) and(ts in lista2))
:
	path_file = (f "Sk_eta_{phi}" + "00" + f "_Temp_{ts}" + "0.dat")
elif((phi in lista) and(ts not in lista2)):
	path_file = (f "Sk_eta_{phi}" + "00" + f "_Temp_{ts}" + ".dat")
		else
:
	path_file = f "Sk_eta_{phi}" + "0" + f "_Temp_{ts}" + ".dat"

		Sks = open(path_file, "r")
		sk_cc = open("Sk_cc.dat", "w")

		Sdk_cc =[]
		time =[]

		for columna
in Sks:
		t = columna.split()[0]
			cation_cation = columna.split()[1]

			sk_cc.write(t + "\t" + cation_cation + "\n")
			time.append(float (t))
			Sdk_cc.append(float (cation_cation))

			sk_cc.close()

			plt.plot(time, Sdk_cc)
			plt.title("Structure Factor cation-cation")
			plt.xlabel("k $\sigma $")
			plt.ylabel("S(k)")
			plt.savefig("./static/images/S(k)_cc.png")
			plt.close()

def s_k_ca(phi, ts):
		lista =[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
			lista2 =[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
			if ((phi in lista) and(ts in lista2))
	:
			path_file = (f "Sk_eta_{phi}" + "00" + f "_Temp_{ts}" + "0.dat")
	elif((phi in lista) and(ts not in lista2)):
			path_file = (f "Sk_eta_{phi}" + "00" + f "_Temp_{ts}" + ".dat")
				else
	:
			path_file = f "Sk_eta_{phi}" + "0" + f "_Temp_{ts}" + ".dat"

				Sks = open(path_file, "r")
				sk_ca = open("Sk_ca.dat", "w")

				Sdk_ca =[]
				time =[]

				for columna
		in Sks:
				t = columna.split()[0]
					cation_anion = columna.split()[2]


					sk_ca.write(t + "\t" + cation_anion + "\n")
					time.append(float (t))
					Sdk_ca.append(float (cation_anion))

					sk_ca.close()

					plt.plot(time, Sdk_ca)
					plt.title("Structure Factor cation-anion")
					plt.xlabel("k $\sigma $")
					plt.ylabel("S(k)")
					plt.savefig("./static/images/S(k)_ca.png")
					plt.close()

		def s_k_aa(phi, ts):
				lista =[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
					lista2 =[0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
					if ((phi in lista) and(ts in lista2))
			:
					path_file = (f "Sk_eta_{phi}" + "00" + f "_Temp_{ts}" + "0.dat")
			elif((phi in lista) and(ts not in lista2)):
					path_file = (f "Sk_eta_{phi}" + "00" + f "_Temp_{ts}" + ".dat")
						else
			:
					path_file = f "Sk_eta_{phi}" + "0" + f "_Temp_{ts}" + ".dat"

						Sks = open(path_file, "r")
						sk_aa = open("Sk_aa.dat", "w")

						Sdk_aa =[]
						time =[]

						for columna
				in Sks:
						t = columna.split()[0]
							anion_anion = columna.split()[3]

							sk_aa.write(t + "\t" + anion_anion + "\n")
							time.append(float (t))
							Sdk_aa.append(float (anion_anion))


							plt.plot(time, Sdk_aa)
							plt.title("Structure Factor anion-anion")
							plt.xlabel("k $\sigma $")
							plt.ylabel("S(k)")
							plt.savefig("./static/images/S(k)_aa.png")
							plt.close()

							sk_aa.close()


							@ app.route("/", methods =["GET", "POST"])
				def index():
						result = None
							ratio = None
							asym = None
							S_k_cc = None
							S_k_ca = None
							S_k_aa = None
							select_option = None
							if request
					.method == "POST":
#Obtener los números desde el formulario
	big = float	(request.form["big"])
			small = float (request.form["small"])
	phi = float (request.form["phi"])
	ts = float (request.form["ts"])
	select_option = request.form.get("Option")

	if select_option == "Structure":
#Llamar al programa Fortran pasando los números como parámetros
	try:
#Ejecutamos el programa Fortran con los parámetros desde Flask
	process = subprocess.Popen(
				   ["./structure_Apple_Silicon"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True
	)
#Enviar los números al programa Fortran
		input_data = f "{big}\n{small}\n{phi}\n{ts}"
		output,		error = process.communicate(input = input_data)

		if process.returncode == 0:
		result = output.splitlines()
			[-1]
#Obtener la última línea de la salida
			ratio = round(big / small, 2)
			asym = round(ratio, 1)
			S_k_cc = s_k_cc(phi, ts)
			S_k_ca = s_k_ca(phi, ts)
			S_k_aa = s_k_aa(phi, ts)
			else
			:
			result = f "Error running Fortran: {error}"
			except Exception as e:
			result = f "Error: {str(e)}"

			else
			:
			try:
#Ejecutamos el programa Fortran con los parámetros desde Flask
			process = subprocess.Popen(
						   ["./dynamics_Apple_Silicon"], stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True
			)
#Enviar los números al programa Fortran
			input_data = f "{big}\n{small}\n{phi}\n{ts}"
			output,		error = process.communicate(input = input_data)

			if process.returncode == 0:
			result = output.splitlines()
				[-1]
#Obtener la última línea de la salida
				ratio = round(big / small, 2)
				asym = round(ratio, 1)
				else
				:
				result = f "Error running Fortran: {error}"
				except Exception as e:
				result = f "Error: {str(e)}"

				return render_template("index.html", result = result, rat = asym, S_k_aa = S_k_aa, S_k_ca = S_k_ca, S_k_cc = S_k_cc, select_option = select_option)

				@ app.route("/download_file_Sk_cc")
				def download_file_Sk_cc():
				return send_file("./Sk_cc.dat", as_attachment = True)

				@ app.route("/download_file_Sk_ca")
				def download_file_Sk_ca():
				return send_file("./Sk_ca.dat", as_attachment = True)

				@ app.route("/download_file_Sk_aa")
				def download_file_Sk_aa():
				return send_file("./Sk_aa.dat", as_attachment = True)

#if __name__ == '__main__':
#app.run(debug = True)
