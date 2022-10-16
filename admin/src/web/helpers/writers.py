import csv 
from fpdf import FPDF
from flask import render_template
 

def write_csv_file(filename,data):
    """Args:
        filename (str): Name of the file to be written
        data (list): Data to be written
    """    
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["Nombre","Apellido","DNI","Email","Direccion","Estado","Telefono"])
        for associate in data:
            writer.writerow([associate.name,associate.surname,associate.DNI_number,associate.email,associate.address,associate.active,associate.phone_number])

def write_pdf_file(filename,data):
    """Args:
        filename (str): Name of the file to be written
        data (list): Data to be written
    """    
    pdf = FPDF()
    
    # Add a page
    pdf.add_page()
    
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 25,style="B")
    
    # create a cell
    pdf.cell(200, 30, txt = "Club Deportivo Villa Elisa",ln = 1, align = 'C')
    
    # add another cell
    pdf.set_font("Arial", size = 15)
    pdf.cell(200, 20, txt = "Reporte completo del listado de asociados",ln = 2, align = 'C')
    
    pdf.set_font("Arial", size = 10)
    for associate in data:
        pdf.multi_cell(200, 10, 
            txt = f"""Nombre: {associate.name} {associate.surname} DNI: {associate.DNI_number} 
            Email: {associate.email} Direccion: {associate.address} Estado: {"Activo" if associate.active else "Inactivo"}
            Telefono: {associate.phone_number}""",ln = 2, align = 'C')
        pdf.ln(5)

    pdf.output(filename)  

            