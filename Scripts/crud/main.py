from typing import Text
from flask import render_template, request, redirect, url_for
from flask.helpers import total_seconds
from flask_login import login_user, logout_user
from datetime import date
import datetime
from sqlalchemy.sql.elements import BooleanClauseList, Null, and_
from sqlalchemy.sql.operators import ilike_op
from app import app, db
from app.models import User , Servicos, Clientes, ServicosAgendados, StatusAgendamento
from random import randint
from sqlalchemy.sql import functions
import os

if __name__== 'main':
    port = int(os.getenv('PORT'), '5000')
    app.run(host='0.0.0.0', port = port)


@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome")
        telefone = request.form.get("telefone")
        usuario= request.form.get("usuario")
        senha = request.form.get("senha")

        if nome and telefone and usuario and senha:
            user = User(nome,telefone,usuario,senha)
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('login'))

    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        pwd = request.form['senha']

        user = User.query.filter_by(usuario=usuario).first()

        if not user or not user.verify_password(pwd):
            return redirect(url_for('login'))        

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/", methods=['GET', 'POST'])
def home():
    ultimaAtualizacao=datetime.datetime.now().strftime('%d-%m-%Y as %H:%M:%S')
    queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento == date.today()).filter(ServicosAgendados.status == 1).first()
    
    '''Pega ano atual'''
    anoAtual = datetime.datetime.now().year
    anoAtual = str(anoAtual)


    '''Quantidade de serviços por mês'''
    janSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-01-01',anoAtual+'-01-31')).filter(ServicosAgendados.status!=2).count()
    fevSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-02-01',anoAtual+'-02-29')).filter(ServicosAgendados.status!=2).count()
    marSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-03-01',anoAtual+'-03-31')).filter(ServicosAgendados.status!=2).count()
    abrSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-04-01',anoAtual+'-04-30')).filter(ServicosAgendados.status!=2).count()
    maiSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-05-01',anoAtual+'-05-31')).filter(ServicosAgendados.status!=2).count()
    junSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-06-01',anoAtual+'-06-30')).filter(ServicosAgendados.status!=2).count()
    julSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-07-01',anoAtual+'-07-31')).filter(ServicosAgendados.status!=2).count()
    agoSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-08-01',anoAtual+'-08-31')).filter(ServicosAgendados.status!=2).count()
    setSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-09-01',anoAtual+'-09-30')).filter(ServicosAgendados.status!=2).count()
    outSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-10-01',anoAtual+'-10-31')).filter(ServicosAgendados.status!=2).count()
    novSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-11-01',anoAtual+'-11-30')).filter(ServicosAgendados.status!=2).count()
    dezSearch= db.session.query(ServicosAgendados).filter(ServicosAgendados.data_agendamento.between(anoAtual+'-12-01',anoAtual+'-12-31')).filter(ServicosAgendados.status!=2).count()
    

    '''Numero de vezes que um serviço foi concludio'''
    cabeloSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==1).filter(ServicosAgendados.status == 1).count()
    barbaSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==2).filter(ServicosAgendados.status == 1).count()
    tinturaSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==3).filter(ServicosAgendados.status == 1 ).count()
    luzesSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==15).filter(ServicosAgendados.status == 1).count()
    penteadoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==16).filter(ServicosAgendados.status == 1).count()
    sombrancelhaSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==17).filter(ServicosAgendados.status == 1).count()
    novoSearch =db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==18).filter(ServicosAgendados.status == 1).count()

    '''Numero de vezes que cada servico foi cancelado'''
    cabeloCanceladoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==1).filter(ServicosAgendados.status==2).count()
    barbaCanceladoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==2).filter(ServicosAgendados.status==2).count()
    tinturaCanceladoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==3).filter(ServicosAgendados.status==2).count()
    luzesCanceladoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==15).filter(ServicosAgendados.status==2).count()
    penteadoCanceladoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==16).filter(ServicosAgendados.status==2).count()
    sombrancelhaCanceladoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==17).filter(ServicosAgendados.status==2).count()
    novoCanceladoSearch = db.session.query(ServicosAgendados).filter(ServicosAgendados.fk_id_servico==18).filter(ServicosAgendados.status==2).count()

    total = queryTotal[2]
    if total == None:
        total = 0
    
    servicosagendados = ServicosAgendados.query.filter_by(data_agendamento=date.today())
    return render_template('home.html', servicosagendados=servicosagendados,ultimaAtualizacao=ultimaAtualizacao, total=total,
                                                                                                                            janSearch =janSearch,
                                                                                                                            fevSearch =fevSearch,
                                                                                                                            marSearch =marSearch,
                                                                                                                            abrSearch =abrSearch,
                                                                                                                            maiSearch =maiSearch,
                                                                                                                            junSearch =junSearch,
                                                                                                                            julSearch =julSearch,
                                                                                                                            agoSearch =agoSearch,
                                                                                                                            setSearch =setSearch,
                                                                                                                            outSearch =outSearch,
                                                                                                                            novSearch =novSearch,
                                                                                                                            dezSearch =dezSearch,

                                                                                                                            cabeloSearch =cabeloSearch,
                                                                                                                            barbaSearch = barbaSearch,
                                                                                                                            tinturaSearch =tinturaSearch,
                                                                                                                            luzesSearch =luzesSearch,
                                                                                                                            sombrancelhaSearch =sombrancelhaSearch,
                                                                                                                            penteadoSearch =penteadoSearch,
                                                                                                                            novoSearch =novoSearch,

                                                                                                                            cabeloCanceladoSearch =cabeloCanceladoSearch,
                                                                                                                            barbaCanceladoSearch =barbaCanceladoSearch,
                                                                                                                            tinturaCanceladoSearch =tinturaCanceladoSearch,
                                                                                                                            luzesCanceladoSearch =luzesCanceladoSearch,
                                                                                                                            sombrancelhaCanceladoSearch =sombrancelhaCanceladoSearch,
                                                                                                                            penteadoCanceladoSearch =penteadoCanceladoSearch,
                                                                                                                            novoCanceladoSearch =novoCanceladoSearch
                                                                                                                            )


@app.route("/lista")
def lista():
    pessoas = User.query.all()
    return render_template("lista.html",pessoas=pessoas)


@app.route("/excluir/<int:id>")
def excluir(id):
    pessoa = User.query.filter_by(id=id).first()

    db.session.delete(pessoa)
    db.session.commit()

    pessoas = User.query.all()
    return render_template("lista.html",pessoas=pessoas)


@app.route("/clientes", methods=['GET', 'POST'])
def clientes():
    alerta= ""
    if request.method == "POST":
        nome = request.form.get("nome_cliente")
        cpf = request.form.get("cpf_cliente")
        telefone = request.form.get("telefone_cliente")

        verificacaoClientes = bool(Clientes.query.filter_by(cpf = cpf).first())
        if verificacaoClientes == False:
            if nome and cpf and telefone:
                valido = cpf_validate(cpf)
                if valido == True:
                    user = Clientes(nome,cpf,telefone)
                    db.session.add(user)
                    db.session.commit()
                else:
                    alerta = "CPF Inválido!!!"
        else:
            alerta = "CPF já existe em nosso banco de dados!!!" 
    clientes = Clientes.query.all()
    return render_template("clientes.html",clientes=clientes, alerta=alerta)

@app.route("/pesquisaCliente", methods=['GET', 'POST'])
def pesquisaCliente():
    clientes = ""
    if request.method == "POST":
        conteudoPesquisa = request.form.get("tipoClientePesquisa")
        tipoPesquida = request.form.get("comboboxCliente")
        if conteudoPesquisa:
            if tipoPesquida == "2":
                clientes= db.session.query(Clientes).filter(Clientes.nome.like("%"+conteudoPesquisa+"%")).all()
            elif tipoPesquida == "1":
                clientes= Clientes.query.filter_by(nome=conteudoPesquisa).all()
            elif tipoPesquida == "3":
                clientes= Clientes.query.filter_by(cpf=conteudoPesquisa).all()
            elif tipoPesquida == "4":
                clientes= db.session.query(Clientes).filter(Clientes.cpf.like("%"+conteudoPesquisa+"%")).all()
            else:
                clientes = Clientes.query.all()
        else:
            clientes = Clientes.query.all()
        
    return render_template("clientes.html",clientes=clientes)


@app.route("/excluircliente/<int:id>")
def excluircliente(id):
    clientes = Clientes.query.all()
    if id :
        cliente = Clientes.query.filter_by(id_cliente=id).first()

        db.session.delete(cliente)
        db.session.commit()

        return redirect(url_for("clientes"))

    return render_template("clientes.html",clientes=clientes)


@app.route("/servicos", methods=['GET', 'POST'])
def servicos():
    if request.method == "POST":
        nome = request.form.get("servico")
        preco = request.form.get("preco")

        if nome and preco:
            user = Servicos(nome,preco)
            db.session.add(user)
            db.session.commit()
            
    servicos = Servicos.query.all()
    return render_template("servicos.html",servicos=servicos)


@app.route("/excluirservico/<int:id>")
def excluirservico(id):
    servicos = Servicos.query.all()
    if id :
        servico = Servicos.query.filter_by(id_servicos=id).first()

        db.session.delete(servico)
        db.session.commit()
        
        return redirect(url_for("servicos"))

    return render_template("servicos.html",servicos=servicos)


@app.route("/financeiro", methods=['GET', 'POST'])
def financeiro():
    total=0
    pesquisasDatas=""
    if request.method == 'POST':
        data = request.form.get("dataPesquisa")
        data2 = request.form.get("dataPesquisa2")
        tipoPesquida = request.form.get("comboboxTipoPesquisaFinanceiro")
        if data and tipoPesquida == "1":
            pesquisasDatas= db.session.query(ServicosAgendados, Servicos).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento == data).filter(ServicosAgendados.status == 1).all()
            queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento == data).filter(ServicosAgendados.status == 1).first()
            total = queryTotal[2]
            return render_template('financeiro.html', pesquisasDatas=pesquisasDatas, total=total)
        elif tipoPesquida == "2":
            if data and data2 :
                pesquisasDatas= db.session.query(ServicosAgendados, Servicos).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento.between(data,data2)).filter(ServicosAgendados.status == 1).all()
                queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.data_agendamento.between(data,data2)).filter(ServicosAgendados.status == 1).first()
                total = queryTotal[2]
                return render_template('financeiro.html', pesquisasDatas=pesquisasDatas, total=total)
        else:
            pesquisasDatas= db.session.query(ServicosAgendados, Servicos).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.status == 1).all()
            queryTotal= db.session.query(ServicosAgendados, Servicos, functions.sum(Servicos.preco)).join(Servicos, ServicosAgendados.fk_id_servico == Servicos.id_servicos).filter(ServicosAgendados.status == 1).first()
            total = queryTotal[2]
            return render_template('financeiro.html', pesquisasDatas=pesquisasDatas, total=total)

    return render_template('financeiro.html',pesquisasDatas=pesquisasDatas, total=total)


@app.route("/agendamento", methods=['GET', 'POST'])
def agendamento():
    alerta = ""
    if request.method == "POST":
        alerta = ""
        fk_id_servico = request.form.get("servicoagendado")
        desc = Servicos.query.filter_by(id_servicos=fk_id_servico).first()
        desc_servico = "NOME: "+desc.nome +", PREÇO: R$ "+str(desc.preco)+",00"
        fk_id_cliente = request.form.get("nome-cliente")
        cliente_selecionado = Clientes.query.filter_by(id_cliente=fk_id_cliente).first()
        nm_cliente = cliente_selecionado.nome
        data_agendamento = request.form.get("data")
        horario_agendado = request.form.get("horario")

        verificacaoServicosAgendados = bool(ServicosAgendados.query.filter_by(horario_agendado = horario_agendado, data_agendamento = data_agendamento).first())
        verificacaoHorario = datetime.datetime.now().strftime('%H:%M:%S')
        dataAtual = datetime.datetime.now().strftime('%Y-%m-%d')

        if verificacaoServicosAgendados == False:
            if verificacaoHorario < horario_agendado and dataAtual == data_agendamento:
                if fk_id_servico and desc_servico and fk_id_cliente and nm_cliente and horario_agendado and data_agendamento:
                    status = 0
                    desc_status = ""
                    alerta = ""
                    user = ServicosAgendados(fk_id_servico, desc_servico, fk_id_cliente, nm_cliente, horario_agendado, data_agendamento,status,desc_status)
                    db.session.add(user)
                    db.session.commit()
            elif verificacaoHorario < horario_agendado and dataAtual != data_agendamento:
                status = 0
                desc_status = ""
                alerta = ""
                user = ServicosAgendados(fk_id_servico, desc_servico, fk_id_cliente, nm_cliente, horario_agendado, data_agendamento,status,desc_status)
                db.session.add(user)
                db.session.commit()
            else:
                alerta = "Desculpe esse horario já passou"
        else: 
            alerta = f'''Já existe um cliente agendado para esse horário {horario_agendado}, por favor agende em um horário diferente!!!'''

    clientes = Clientes.query.all()
    servicos = Servicos.query.all()
    return render_template('agendamento.html', servicos=servicos, clientes=clientes, alerta = alerta)


@app.route("/agenda", methods=['GET', 'POST'])
def agenda():
    servicosagendados = ServicosAgendados.query.filter_by(data_agendamento=date.today())
    servicosconcluidos = ServicosAgendados.query.filter_by(status=1,data_agendamento=date.today())
    servicoscancelados = ServicosAgendados.query.filter_by(status=2,data_agendamento=date.today())
    if request.method == "POST":
        data = request.form.get("dataPesquisa")
        
        if data:
            servicosagendados = ServicosAgendados.query.filter_by(data_agendamento=data)
            servicosconcluidos = ServicosAgendados.query.filter_by(status=1,data_agendamento=data)
            servicoscancelados = ServicosAgendados.query.filter_by(status=2,data_agendamento=data)
        else:
            servicosagendados = ServicosAgendados.query.all()
            servicosconcluidos = ServicosAgendados.query.filter_by(status=1)
            servicoscancelados = ServicosAgendados.query.filter_by(status=2)
    return render_template('agenda.html', servicosagendados = servicosagendados, servicosconcluidos=servicosconcluidos, servicoscancelados=servicoscancelados)


@app.route("/excluirservicoagendado/<int:id>")
def excluirservicoagendado(id):
    servicosagendados = ServicosAgendados.query.all()
    if id:
        servico_agendado = ServicosAgendados.query.filter_by(id_servico_agendado=id).first()

        db.session.delete(servico_agendado)
        db.session.commit()

        return redirect(url_for("agenda"))

    
    return render_template('agenda.html', servicosagendados = servicosagendados)


@app.route("/atualizarServicos/<int:id>", methods=['GET', 'POST'])
def atualizarServicos(id):
    servico = Servicos.query.filter_by(id_servicos=id).first()
    
    if request.method == "POST":
        nome = request.form.get("servico")
        preco = request.form.get("preco")
       
        if nome and preco:
            servico.nome = nome
            servico.preco = preco

            db.session.commit()

            return redirect(url_for("servicos"))
    
    return render_template("atualizarServicos.html", servico=servico)


@app.route("/statusAgendamento/<int:id>", methods=['GET', 'POST'])
def statusAgendamento(id):
    servicosagendados = ServicosAgendados.query.filter_by(id_servico_agendado=id).first()

    if request.method == "POST":
        status = request.form.get("status")
       
        if status :
            servicosagendados.status = status
            desc_status = StatusAgendamento.query.filter_by(id_status=status).first()
            servicosagendados.desc_status = desc_status.desc_status
            db.session.commit()

            return redirect(url_for("agenda"))

    return render_template('statusAgendamento.html', servicosagendados = servicosagendados)

@app.route("/atualizarCliente/<int:id>", methods=['GET', 'POST'])
def atualizarCliente(id):
    cliente = cliente = Clientes.query.filter_by(id_cliente=id).first()
    erro = ""
    if request.method == "POST":
        nome = request.form.get("nome_cliente")
        cpf = request.form.get("cpf_cliente")
        telefone = request.form.get("telefone_cliente")
        

        if nome and cpf and telefone:
            valido = cpf_validate(cpf)
            if valido == True:
                cliente.nome = nome
                cliente.cpf = cpf
                cliente.telefone = telefone

                db.session.commit()

                return redirect(url_for("clientes"))
            else:
                erro = "CPF Inválido"

    
    return render_template("atualizarCliente.html", cliente = cliente, erro=erro)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')

def cpf_validate(numbers):

    cpf = [int(char) for char in numbers if char.isdigit()]


    if len(cpf) != 11:
        return False

    if cpf == cpf[::-1]:
        return False

    for i in range(9, 11):
        value = sum((cpf[num] * ((i+1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True

    

app.run(debug=True)