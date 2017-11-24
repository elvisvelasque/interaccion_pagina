import selenium 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver
import  sqlite3
from PIL import Image	
import time


#################################################################################################################################################################
################################ CODIGO PRINCIPAL ###############################################################################################################
#################################################################################################################################################################


#SQLITE CONACION
conn = sqlite3.connect('SIAF.db')
c = conn.cursor()

# Create table solo si no estan creadas previamente

c.execute('''CREATE TABLE EXPEDIENTE_ADMIN
			 (Entidad INTEGER,  año text, expediente int, nom_entidad text, tipo_operacio text, nom_operacion text, tipo_mod_compra text, nom_mod_compra text, tipo_prc_selecc text, nom_prc_selecc)''')

c.execute('''CREATE TABLE DATOS_EXPEDIENTE
			 (Entidad INTEGER,  año text, expediente int, num_registro int, ciclo char, fase char, sec int, corr int, doc INTEGER, numero text, fecha date, ff int, moneda text,  monto real, estado char, fecha_proceso datetime,  id_trx INTEGER )''')

#INGRESAR A LA PAGINA
driver= webdriver.Chrome()
driver.get('http://apps2.mef.gob.pe/consulta-vfp-webapp/consultaExpediente.jspx')

for k in range(6):


	e=str(k)+".jpg"
	if k>0:
		driver.back()
		driver.refresh()

	#TOMAR CAPTURA DEL CAPCTCHA Y MOSTRARLO
	driver.save_screenshot('screenshot.png')
	screenshot=Image.open('screenshot.png')
	captcha= screenshot.crop((149,518,349,576))
	captcha.save("img/"+e)
	A= Image.open("img/"+e)
	A.show()

	#LLENAR EL FORMULARIO DE ENTRADA
	cont= input("¿Cual es el contenido del captcha? ")
	captcha_entrada= driver.find_element_by_id("j_captcha")
	captcha_entrada.send_keys(str(cont))

	unidad_ejec= driver.find_element_by_id("secEjec")
	unidad_ejec.send_keys("300001")

	expediente= driver.find_element_by_id("expediente")
	exp=k+100
	expediente.send_keys(str(exp))

	buscar=driver.find_element_by_xpath("//*[@id='command']/input").click()
	time.sleep(3)

    #leer data DEL REGISTRO EXPEDIENTE ADMIN
	año= driver.find_element_by_id("anoEje")
	dato_año= año.get_attribute("value")

	entidadid = driver.find_element_by_id("secEjec")
	id_entidad= entidadid.get_attribute("value")

	entidadnom = driver.find_element_by_id("secEjecNombre")
	nom_entidad= entidadnom.get_attribute("value")

	expedid = driver.find_element_by_id("expediente")
	id_expediente= expedid.get_attribute("value")

	t_ope= driver.find_element_by_id("tipoOperacion")
	tipo_ope= t_ope.get_attribute("value")

	nom_ope= driver.find_element_by_id("tipoOperacionNombre")
	nombre_ope= nom_ope.get_attribute("value")

	t_modcom= driver.find_element_by_id("modalidadCompra")
	tipo_modo_compra= t_modcom.get_attribute("value")

	nom_modcom= driver.find_element_by_id("modalidadCompraNombre")
	nombre_modcom= nom_modcom.get_attribute("value")

	t_prc_sel= driver.find_element_by_id("tipoProceso")
	tipo_prc_sel= t_prc_sel.get_attribute("value")

	nom_prc_sel= driver.find_element_by_id("tipoProcesoNombre")
	nombre_prc_sel= nom_prc_sel.get_attribute("value")

	#leer DATOS DEL EXPEDIENTE

	tablaexpedientes = driver.find_elements_by_tag_name("td")
	datostabla=[]
	for i in range(len(tablaexpedientes)//14):
		regexpediente = ()
		regexpediente += (dato_año,)
		regexpediente += (id_entidad,)
		regexpediente += (id_expediente,)
		regexpediente += (i+1,)
		regexpediente += (tablaexpedientes[i*14+0].text,)
		regexpediente += (tablaexpedientes[i*14+1].text,)
		regexpediente += (tablaexpedientes[i*14+2].text,)
		regexpediente += (tablaexpedientes[i*14+3].text,)
		regexpediente += (tablaexpedientes[i*14+4].text,)
		regexpediente += (tablaexpedientes[i*14+5].text,)
		regexpediente += (tablaexpedientes[i*14+6].text,)
		regexpediente += (tablaexpedientes[i*14+7].text,)
		regexpediente += (tablaexpedientes[i*14+8].text,)
		regexpediente += (tablaexpedientes[i*14+9].text,)
		regexpediente += (tablaexpedientes[i*14+10].text,)
		regexpediente += (tablaexpedientes[i*14+11].text,)
		regexpediente += (tablaexpedientes[i*14+12].text,)
		datostabla.append(regexpediente)	
		

	#guardar data 
	EXP_arreglo =  [( id_entidad, dato_año, id_expediente , nom_entidad, tipo_ope, nombre_ope,tipo_modo_compra , nombre_modcom , tipo_prc_sel, nombre_prc_sel)]

	c.executemany('INSERT INTO EXPEDIENTE_ADMIN VALUES (?,?,?,?,?,?,?,?,?,?)', EXP_arreglo)
	c.executemany('INSERT INTO DATOS_EXPEDIENTE VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', datostabla)



#Revision de tablas
c.execute('SELECT * FROM EXPEDIENTE_ADMIN')
print("Tabla EXPEDIENTE_ADMIN")
print( c.fetchall())

c.execute('SELECT * FROM DATOS_EXPEDIENTE')
print(" Tabla DATOS_EXPEDIENTE ")
print( c.fetchall())
