from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.board import list_disciplines, add_discipline, get_discipline, delete_discipline, update_discipline,get_last_discipline
from src.web.forms.discipline import DisciplineForm
from src.web.helpers.auth import login_required
from src.core.board import get_cfg

discipline_blueprint = Blueprint("discipline", __name__, url_prefix="/discipline")


@discipline_blueprint.get("/")
@login_required
def index():
    pairs=[("name","Nombre"),("category","Categoría"),("instructors","Instructores"),
    ("dates","Días y horarios"),("true","Disponible"),("false","No Disponible"),("monthly_cost","Costo mensual")]

    if request.args.get("column") in ["true","false"]:
        return render_template("discipline/list.html",disciplines=list_disciplines("available",request.args.get("column")),pairs=pairs)

    if request.args.get("search"):
        return render_template("discipline/list.html",disciplines=list_disciplines(request.args["column"],request.args["search"]),pairs=pairs)
        
    return render_template("discipline/list.html",disciplines=list_disciplines(),pairs=pairs)

@discipline_blueprint.get("/add")
@login_required
def get_add():
    return render_template("discipline/add.html",form=DisciplineForm(currency=get_cfg().currency))

@discipline_blueprint.post("/add")
@login_required
def post_add():
    form = DisciplineForm(request.form)
    if form.validate():
        add_discipline(form.data,get_cfg().currency)
        flash(f"Se agregó {get_last_discipline()}", category="alert alert-info")
        return redirect(url_for("discipline.index"))
    else:
        return render_template("discipline/add.html", form=form)

@discipline_blueprint.get("/update/<id>")
@login_required
def get_update(id):
    return render_template("discipline/update.html",form=DisciplineForm(obj=get_discipline(id),currency=get_cfg().currency))

@discipline_blueprint.post("/update/<id>")
@login_required
def update(id):
    form = DisciplineForm(request.form)
    if form.validate():
        flash(f"Se actualizó {get_discipline(id)}", category="alert alert-info")
        update_discipline(id,form.data)
        return redirect(url_for("discipline.index"))
    else:
        return render_template("discipline/update.html", form=form)

@discipline_blueprint.post("/delete/<id>")
@login_required
def delete(id):
    flash(f"Se elimino {get_discipline(request.form['Delete'])}", category="alert alert-warning")
    delete_discipline(id)
    return redirect(url_for("discipline.index"))

