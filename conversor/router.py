from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from conversor import app, database

from conversor.forms import SuplementoForm, PlanningItemForm, ResumoForm, LoginForm, RegisterForm, ResumoForm, SalvarResumoForm, PessoaForm
from conversor.models import Suplemento, PlanejamentoItem, User, ResumoSalvo, Pessoa

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, logout_user

import json
from datetime import date

import os

import secrets

from conversor.schema import RESUMO_SCHEMA

from conversor.utils import (
agrupar_por_categoria,
    
    calcular_totais_planejamento, 
)



from flask import redirect, url_for

@app.route('/')
def home():
    return redirect(url_for('zonas'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.senha_hash, form.senha.data):
            login_user(user, remember=True)
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('listar_suplementos'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.senha.data)
        novo_usuario = User(
            nome=form.nome.data,
            sobrenome=form.sobrenome.data,
            email=form.email.data,
            senha_hash=hashed_password
        )
        database.session.add(novo_usuario)
        database.session.commit()
        flash('Cadastro realizado! Faça login.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('login'))
 


@app.route('/zonas')
def zonas():
    return render_template('zonas.html')


@app.route('/sobre')
def sobre():
    image_directory = os.path.join(app.root_path, 'static/image')
    images = [os.path.join('image', image) for image in os.listdir(image_directory) if image.endswith('.jpg')]
    return render_template('sobre.html', images=images)


# Cadastro de suplemento
@app.route('/suplementos/novo', methods=['GET', 'POST'])
@login_required
def novo_suplemento():
    form = SuplementoForm()
    
    if form.validate_on_submit():
        suplemento = Suplemento(
            nome=form.nome.data,
            tipo=form.tipo.data,
            marca=form.marca.data,
            carbo=form.carbo.data,
            proteina=form.proteina.data,
            sodio=form.sodio.data,
            magnesio=form.magnesio.data,
            potassio=form.potassio.data,
            calcio=form.calcio.data,
            cloro=form.cloro.data,
            fosforo=form.fosforo.data,
            zinco=form.zinco.data,
            cafeina=form.cafeina.data,
            taurina=form.taurina.data,
            beta_alanina=form.beta_alanina.data,
            citrulina=form.citrulina.data,
            creatina=form.creatina.data,
            coq10=form.coq10.data,
            carnitina=form.carnitina.data,
            leucina=form.leucina.data,
            isoleucina=form.isoleucina.data,
            valina=form.valina.data,
            arginina=form.arginina.data,
            niacina=form.niacina.data,
            gramas_por_porcao=form.gramas_por_porcao.data,
            descricao_porcao=form.descricao_porcao.data,
            vit_b1=form.vit_b1.data,
            vit_b2=form.vit_b2.data,
            vit_b3=form.vit_b3.data,
            vit_b5=form.vit_b5.data,
            vit_b6=form.vit_b6.data,
            vit_b7=form.vit_b7.data,
            vit_b9=form.vit_b9.data,
            vit_b12=form.vit_b12.data,
            vit_c=form.vit_c.data,
            vit_e=form.vit_e.data,
            vit_ferro=form.vit_ferro.data,
            gordura_saturada=form.gordura_saturada.data,
            fibras_alimentares=form.fibras_alimentares.data,
            vit_d=form.vit_d.data,
            acido_pantotenico=form.acido_pantotenico.data,
            acido_folico=form.acido_folico.data,
            tirosina=form.tirosina.data,
            colina=form.colina.data,
            ingredientes=form.ingredientes.data,
            comentario=form.comentario.data,
            user_id=current_user.id  # 👈 liga ao usuário
        )
        database.session.add(suplemento)
        database.session.commit()
        flash('Suplemento cadastrado com sucesso!', 'success')
        return redirect(url_for('listar_suplementos'))
    
    elif form.is_submitted():
        pass
        
    return render_template('cadastro_suplemento.html', form=form)


# Lista de suplementos
@app.route('/suplementos')
@login_required
def listar_suplementos():
    filtro = request.args.get('filtro', '')
    ordenar = request.args.get('ordenar', '')
    direcao = request.args.get('direcao', 'desc')

    query = Suplemento.query #Suplemento.query.filter_by(user_id=current_user.id)  # 👈 só do usuário logado

    if filtro:
        query = query.filter(
            Suplemento.nome.ilike(f'%{filtro}%') | Suplemento.tipo.ilike(f'%{filtro}%')
        )

    if ordenar == 'carbo':
        query = query.order_by(Suplemento.carbo.asc() if direcao == 'asc' else Suplemento.carbo.desc())
    elif ordenar == 'sodio':
        query = query.order_by(Suplemento.sodio.asc() if direcao == 'asc' else Suplemento.sodio.desc())

    suplementos = query.all()
    return render_template(
        'listar_suplementos.html',
        suplementos=suplementos,
        filtro=filtro,
        ordenar=ordenar,
        direcao=direcao
    )


# Duplicar suplemento
@app.route('/duplicar_suplemento/<int:id>', methods=['GET'])
@login_required
def duplicar_suplemento(id):
    suplemento_original = Suplemento.query.filter_by(id=id).first_or_404()

    suplemento_duplicado = Suplemento(
        nome=f"{suplemento_original.nome} (Cópia)",
        tipo=suplemento_original.tipo,
        marca=suplemento_original.marca,
        gramas_por_porcao=suplemento_original.gramas_por_porcao,
        descricao_porcao=suplemento_original.descricao_porcao,
        carbo=suplemento_original.carbo,
        sodio=suplemento_original.sodio,
        magnesio=suplemento_original.magnesio,
        potassio=suplemento_original.potassio,
        calcio=suplemento_original.calcio,
        cloro=suplemento_original.cloro,
        fosforo=suplemento_original.fosforo,
        zinco=suplemento_original.zinco,
        cafeina=suplemento_original.cafeina,
        taurina=suplemento_original.taurina,
        beta_alanina=suplemento_original.beta_alanina,
        citrulina=suplemento_original.citrulina,
        creatina=suplemento_original.creatina,
        coq10=suplemento_original.coq10,
        carnitina=suplemento_original.carnitina,
        leucina=suplemento_original.leucina,
        isoleucina=suplemento_original.isoleucina,
        valina=suplemento_original.valina,
        arginina=suplemento_original.arginina,
        niacina=suplemento_original.niacina,
        vit_b1=suplemento_original.vit_b1,
        vit_b2=suplemento_original.vit_b2,
        vit_b3=suplemento_original.vit_b3,
        vit_b6=suplemento_original.vit_b6,
        vit_b7=suplemento_original.vit_b7,
        vit_b9=suplemento_original.vit_b9,
        vit_b12=suplemento_original.vit_b12,
        vit_c=suplemento_original.vit_c,
        vit_e=suplemento_original.vit_e,
        ingredientes=suplemento_original.ingredientes,
        comentario=suplemento_original.comentario,
        user_id=current_user.id
    )

    database.session.add(suplemento_duplicado)
    database.session.commit()
    flash('Suplemento duplicado com sucesso!', 'success')
    return redirect(url_for('listar_suplementos'))


# Excluir suplemento
@app.route('/suplementos/excluir/<int:id>', methods=['GET'])
@login_required
def excluir_suplemento(id):
    suplemento = Suplemento.query.filter_by(id=id).first_or_404()
    database.session.delete(suplemento)
    database.session.commit()
    flash('Suplemento excluído com sucesso!', 'success')
    return redirect(url_for('listar_suplementos'))


# Editar suplemento
@app.route('/suplementos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_suplemento(id):
    suplemento = Suplemento.query.filter_by(id=id).first_or_404()
    form = SuplementoForm(obj=suplemento)

    if form.validate_on_submit():
        form.populate_obj(suplemento)
        database.session.commit()
        flash('Suplemento editado com sucesso!', 'success')
        return redirect(url_for('listar_suplementos'))

    return render_template('editar_suplemento.html', form=form, suplemento=suplemento)

# Planejamento
@app.route('/planejamento', methods=['GET', 'POST'])
@login_required
def planejamento():
    form = PlanningItemForm()
    form.suplemento_id.choices = [
        (s.id, s.nome) for s in Suplemento.query.order_by(Suplemento.nome.asc()).all()
    ]

    if form.validate_on_submit():
        item_existente = PlanejamentoItem.query.filter_by(
            suplemento_id=form.suplemento_id.data, user_id=current_user.id
        ).first()

        if item_existente:
            item_existente.quantidade += float(form.quantidade.data)
        else:
            novo_item = PlanejamentoItem(
                suplemento_id=form.suplemento_id.data,
                quantidade=form.quantidade.data,
                user_id=current_user.id
            )
            database.session.add(novo_item)

        database.session.commit()
        flash('Item adicionado/atualizado com sucesso!', 'success')
        return redirect(url_for('planejamento'))

    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    itens_validos = []

    for item in itens:
        if item.suplemento is None:
            database.session.delete(item)
        else:
            itens_validos.append(item)

    database.session.commit()
    totais = calcular_totais_planejamento(itens_validos)

    return render_template('planejamento.html', form=form, itens=itens_validos, totais=totais)



# Atualizar quantidade no planejamento
@app.route('/planejamento/atualizar/<int:item_id>', methods=['POST'])
@login_required
def atualizar_quantidade(item_id):
    item = PlanejamentoItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()

    try:
        # Aceita ponto ou vírgula como separador decimal
        quantidade_str = request.form.get('quantidade', '').replace(',', '.')
        nova_quantidade = float(quantidade_str)

        if nova_quantidade >= 0.01:
            item.quantidade = nova_quantidade
            database.session.commit()
            flash('Quantidade atualizada com sucesso!', 'success')
        else:
            flash('Quantidade inválida.', 'danger')

    except (ValueError, TypeError):
        flash('Quantidade inválida.', 'danger')

    return redirect(url_for('planejamento'))

# Remover item do planejamento
@app.route('/planejamento/remover/<int:item_id>', methods=['POST'])
@login_required
def remover_item(item_id):
    item = PlanejamentoItem.query.filter_by(id=item_id, user_id=current_user.id).first_or_404()
    database.session.delete(item)
    database.session.commit()
    flash('Item removido do planejamento.', 'success')
    return redirect(url_for('planejamento'))

# Remover todos os itens do planejamento
@app.route('/planejamento/remover_todos', methods=['POST'])
@login_required
def remover_todos_itens():
    PlanejamentoItem.query.filter_by(user_id=current_user.id).delete()
    database.session.commit()
    flash('Todos os itens foram removidos do planejamento.', 'success')
    return redirect(url_for('planejamento'))


# Resumo
@app.route('/resumo', methods=['GET', 'POST'])
@login_required
def resumo_view():
    form = ResumoForm()
    
    form_salvar = SalvarResumoForm()
    form_salvar.pessoa_id.choices = [(0, 'Eu mesmo')] + [
        (p.id, p.nome) for p in Pessoa.query.filter_by(user_id=current_user.id).order_by(Pessoa.nome.asc()).all()]

    if request.method == 'POST' and 'limpar' in request.form:
        return redirect(url_for('resumo_view'))

    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    itens_utilizados = [f"{item.quantidade}x {item.suplemento.nome}" for item in itens if item.suplemento]
    itens_utilizados_str = ", ".join(itens_utilizados)


    totais = calcular_totais_planejamento(itens)

    totais_por_hora = {}
    tempo_total = 0
    resumo_dados = {}

    if form.validate_on_submit():
        tempo_natacao = (form.tempo_natacao_horas.data or 0) + (form.tempo_natacao_minutos.data or 0) / 60
        tempo_bike = (form.tempo_bike_horas.data or 0) + (form.tempo_bike_minutos.data or 0) / 60
        tempo_corrida = (form.tempo_corrida_horas.data or 0) + (form.tempo_corrida_minutos.data or 0) / 60

        tempo_total = tempo_natacao + tempo_bike + tempo_corrida

        if tempo_total > 0:
            for key, valor in totais.items():
                totais_por_hora[key] = round(valor / tempo_total, 2)
            resumo_dados = agrupar_por_categoria(totais_por_hora)

        session['resumo_dados'] = json.dumps(resumo_dados)
        flash("Resumo calculado com sucesso!", "success")

# 🔽 Adicione isso aqui
    search = request.args.get("search", "").strip()
    pessoa_filtro = request.args.get("pessoa_filtro", "")

    pessoas = Pessoa.query.filter_by(user_id=current_user.id).order_by(Pessoa.nome.asc()).all()

    resumos_query = ResumoSalvo.query.filter_by(user_id=current_user.id)

    if pessoa_filtro == "eu":
        resumos_query = resumos_query.filter(ResumoSalvo.pessoa_id.is_(None))
    elif pessoa_filtro:
        resumos_query = resumos_query.filter(ResumoSalvo.pessoa_id == int(pessoa_filtro))

    if search:
        resumos_query = resumos_query.filter(
            database.or_(
                ResumoSalvo.nome_treino.ilike(f"%{search}%"),
                ResumoSalvo.comentario.ilike(f"%{search}%")
            )
        )

    resumos = resumos_query.order_by(ResumoSalvo.ordem.desc(), ResumoSalvo.id.desc()).all()

    

    return render_template(
        "resumo.html",
        form=form,
        totais=totais_por_hora,
        resumo=resumo_dados,
        tempo_total=round(tempo_total, 2),
        current_date=date.today().isoformat(),
        resumos=resumos,  # <-- novo contexto
        itens_utilizados=itens_utilizados_str,
        form_salvar=form_salvar,
        pessoas=pessoas,
        pessoa_filtro=pessoa_filtro
        
    )
            

@app.route('/salvar_resumo', methods=['GET', 'POST'])
@login_required
def salvar_resumo():
    form = SalvarResumoForm()
    
    form.pessoa_id.choices = [(0, 'Eu mesmo')] + [
    (p.id, p.nome) for p in Pessoa.query.filter_by(user_id=current_user.id).order_by(Pessoa.nome.asc()).all()]

    def parse_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    if form.validate_on_submit():
        print("Formulário validado")
    else:
        print("Formulário NÃO validado")
        print(form.errors)

    resumo_json = session.get('resumo_dados')
    if not resumo_json:
        flash("Nenhum resumo disponível para salvar. Por favor, calcule um resumo antes.", "danger")
        return redirect(url_for('resumo_view'))

    if form.validate_on_submit():
        tempo_natacao = parse_float(request.form.get("tempo_natacao_horas")) + parse_float(request.form.get("tempo_natacao_minutos")) / 60
        tempo_bike = parse_float(request.form.get("tempo_bike_horas")) + parse_float(request.form.get("tempo_bike_minutos")) / 60
        tempo_corrida = parse_float(request.form.get("tempo_corrida_horas")) + parse_float(request.form.get("tempo_corrida_minutos")) / 60
        tempo_total = tempo_natacao + tempo_bike + tempo_corrida

        # 🔽 Captura os suplementos utilizados no momento atual
        itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
        suplementos_utilizados = ", ".join(
            [f"{item.quantidade}x {item.suplemento.nome}" for item in itens if item.suplemento]
        )

        novo_resumo = ResumoSalvo(
            user_id=current_user.id,
            pessoa_id=form.pessoa_id.data if form.pessoa_id.data != 0 else None,
            token_publico=secrets.token_urlsafe(16),  # Gera um token seguro e curto
            nome_treino=form.nome_treino.data,
            data=form.data.data,
            comentario=form.comentario.data,
            resumo_dados=json.loads(request.form["resumo_dados"]),
            suplementos_utilizados=suplementos_utilizados,  # ✅ aqui
            tempo_natacao=tempo_natacao,
            tempo_bike=tempo_bike,
            tempo_corrida=tempo_corrida,
            tempo_total=tempo_total
        )

        # Define a maior ordem atual + 1
        maior_ordem = database.session.query(database.func.max(ResumoSalvo.ordem)).filter_by(user_id=current_user.id).scalar() or 0
        novo_resumo.ordem = maior_ordem + 1
            
        database.session.add(novo_resumo)
        database.session.commit()
        flash("Resumo salvo com sucesso!", "success")
        return redirect(url_for('resumo_view'))

    return render_template("salvar_resumo.html", form=form, dados=json.loads(resumo_json))


@app.route('/deletar_resumo/<int:id>', methods=['POST'])
@login_required
def deletar_resumo(id):
    resumo = ResumoSalvo.query.get_or_404(id)
    if resumo.user_id != current_user.id:
        flash("Você não tem permissão para excluir esse resumo.", "danger")
        return redirect(url_for('resumo_view'))

    database.session.delete(resumo)
    database.session.commit()
    flash("Resumo excluído com sucesso!", "success")
    return redirect(url_for('resumo_view'))


@app.route('/buscar_resumos')
@login_required
def buscar_resumos():
    termo = request.args.get("termo", "").strip().lower()

    pessoa_filtro = request.args.get("pessoa_filtro")
    query = ResumoSalvo.query.filter_by(user_id=current_user.id)

    if pessoa_filtro == "eu":
        query = query.filter(ResumoSalvo.pessoa_id.is_(None))
    elif pessoa_filtro:
        query = query.filter(ResumoSalvo.pessoa_id == int(pessoa_filtro))

    if termo:
        query = query.filter(
            database.or_(
                ResumoSalvo.nome_treino.ilike(f"%{termo}%"),
                ResumoSalvo.comentario.ilike(f"%{termo}%")
            )
        )

    resultados = query.order_by(ResumoSalvo.data.desc()).all()

    return jsonify([
        {
            "id": r.id,
            "nome_treino": r.nome_treino,
            "comentario": r.comentario,
            "data": r.data.strftime("%d/%m/%Y"),
            "tempo_total": round(r.tempo_total, 2),
            "tempo_natacao": round(r.tempo_natacao, 2),
            "tempo_bike": round(r.tempo_bike, 2),
            "tempo_corrida": round(r.tempo_corrida, 2),
            "resumo_dados": r.resumo_dados  # ⬅️ aqui está a chave
        }
        for r in resultados
    ])



@app.route('/resumo/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_resumo(id):
    resumo = ResumoSalvo.query.get_or_404(id)
    if resumo.user_id != current_user.id:
        flash("Você não tem permissão para editar esse resumo.", "danger")
        return redirect(url_for('resumo_view'))

    form = SalvarResumoForm(obj=resumo)

    if form.validate_on_submit():
        resumo.nome_treino = form.nome_treino.data
        resumo.data = form.data.data
        resumo.comentario = form.comentario.data

        # opcionalmente você pode reprocessar tempos ou suplementos aqui
        database.session.commit()
        flash("Resumo atualizado com sucesso!", "success")
        return redirect(url_for('resumo_view'))

    return render_template("editar_resumo.html", form=form, resumo=resumo)



# 🔼 mover_cima (ordem maior → menor)
@app.route('/resumo/mover_cima/<int:id>')
@login_required
def mover_cima(id):
    atual = ResumoSalvo.query.get_or_404(id)
    anterior = ResumoSalvo.query.filter(
        ResumoSalvo.user_id == current_user.id,
        ResumoSalvo.ordem > atual.ordem
    ).order_by(ResumoSalvo.ordem.asc()).first()

    if anterior:
        atual.ordem, anterior.ordem = anterior.ordem, atual.ordem
        database.session.commit()

    return redirect(url_for('resumo_view'))


# 🔽 mover_baixo (ordem menor → maior)
@app.route('/resumo/mover_baixo/<int:id>')
@login_required
def mover_baixo(id):
    atual = ResumoSalvo.query.get_or_404(id)
    proximo = ResumoSalvo.query.filter(
        ResumoSalvo.user_id == current_user.id,
        ResumoSalvo.ordem < atual.ordem
    ).order_by(ResumoSalvo.ordem.desc()).first()
    if proximo:
        atual.ordem, proximo.ordem = proximo.ordem, atual.ordem
        database.session.commit()
    return redirect(url_for('resumo_view'))




@app.route('/salvar_resumo_livre', methods=['POST'])
@login_required
def salvar_resumo_livre():
    form = SalvarResumoForm()

    itens = PlanejamentoItem.query.filter_by(user_id=current_user.id).all()
    suplementos_utilizados = ", ".join(
        [f"{item.quantidade}x {item.suplemento.nome}" for item in itens if item.suplemento]
    )

    resumo_dados = agrupar_por_categoria(calcular_totais_planejamento(itens))

    novo_resumo = ResumoSalvo(
        user_id=current_user.id,
        token_publico=secrets.token_urlsafe(16),  # 🔥 AQUI resolve seu problema
        nome_treino=form.nome_treino.data,
        data=form.data.data,
        comentario=form.comentario.data,
        resumo_dados=resumo_dados,
        suplementos_utilizados=suplementos_utilizados,
        tempo_natacao=0,
        tempo_bike=0,
        tempo_corrida=0,
        tempo_total=0,
        ordem=(
            database.session.query(database.func.max(ResumoSalvo.ordem))
            .filter_by(user_id=current_user.id)
            .scalar() or 0
        ) + 1
    )

    database.session.add(novo_resumo)
    database.session.commit()

    flash("Resumo livre salvo com sucesso!", "success")
    return redirect(url_for('resumo_view'))



# --- PRINT: helpers de impressão --
def formatar_tempo_decimal(h):
    if h is None:
        return "-"
    horas = int(h)
    minutos = int(round((h - horas) * 60))
    return f"{horas}h{minutos:02d}"

UNIDADES_PRINT = {
    categoria: {
        meta["label"]: meta["unidade"]
        for _, meta in campos.items()
    }
    for categoria, campos in RESUMO_SCHEMA.items()
}

# --- PRINT: um resumo ---
@app.route("/resumo/print/<int:id>")
@login_required
def print_resumo(id):
    resumo = ResumoSalvo.query.get_or_404(id)
    if resumo.user_id != current_user.id:
        return redirect(url_for('resumo_view'))
    return render_template(
        "resumo_print.html",
        resumo=resumo,
        unidades=UNIDADES_PRINT,
        formatar_tempo_decimal=formatar_tempo_decimal
    )

# (opcional) PRINT: vários de uma vez (respeita ?search=)
@app.route("/resumos/print")
@login_required
def print_resumos():
    termo = request.args.get("search", "").strip()
    q = ResumoSalvo.query.filter_by(user_id=current_user.id)
    if termo:
        q = q.filter(
            database.or_(ResumoSalvo.nome_treino.ilike(f"%{termo}%"),
                         ResumoSalvo.comentario.ilike(f"%{termo}%"))
        )
    resumos = q.order_by(ResumoSalvo.data.desc()).all()
    return render_template(
        "resumos_print_many.html",
        resumos=resumos,
        unidades=UNIDADES_PRINT,
        formatar_tempo_decimal=formatar_tempo_decimal
    )
    
    
#NOVAS ROTAS DE REFATORAÇÃO 

@app.route('/ferramentas/calculadora', methods=['GET', 'POST'])
def ferramentas_calculadora():
    tipo = request.args.get('tipo', 'ritmo')  # padrão

    resultado = None
    error = None
    tabela_pace = None
    zonas_vo2 = None
    previsoes_prova = None
    form_data = request.form.to_dict() if request.method == 'POST' else {}

    if request.method == 'POST':
        try:
            if tipo == 'tempo':
                from conversor.services.calculos_performance import calculate_estimated_time

                distance = float(request.form.get('distance'))
                pace = request.form.get('pace')

                tempo_calculado = calculate_estimated_time(distance, pace)

                resultado = {
                    "Tempo estimado": tempo_calculado
                }

            elif tipo == 'distancia':
                from conversor.services.calculos_performance import calculate_estimated_distance
                from conversor.services.formatadores import tempo_para_segundos

                hour = request.form.get('hour')
                minute = request.form.get('minute')
                second = request.form.get('second')
                pace = request.form.get('pace')

                tempo = tempo_para_segundos(hour, minute, second)

                distancia = calculate_estimated_distance(tempo, pace)

                resultado = {
                    "Distância estimada": f"{distancia} km"
                }
                
                
            elif tipo == 'ritmo':
                from conversor.services.calculos_performance import (
                    convert_pace,
                    calc_average_speed_bike,
                    calc_swim_pace
                )
                from conversor.services.formatadores import tempo_para_segundos

                hour = request.form.get('hour')
                minute = request.form.get('minute')
                second = request.form.get('second')
                distance = float(request.form.get('distance'))
                activity = request.form.get('activity', 'corrida')

                tempo = tempo_para_segundos(hour, minute, second)

                if activity == 'corrida':
                    pace_km, pace_mile = convert_pace(tempo, distance)
                    resultado = {
                        "Pace por km": pace_km,
                        "Pace por milha": pace_mile
                    }

                elif activity == 'ciclismo':
                    avg_speed = calc_average_speed_bike(tempo, distance)
                    resultado = {
                        "Velocidade média": f"{avg_speed} km/h"
                    }

                elif activity == 'natacao':
                    pace_100m = calc_swim_pace(tempo, distance)
                    resultado = {
                        "Pace por 100m": f"{pace_100m} /100m"
                    }
                
            
            elif tipo == 'pace_velocidade':
                from conversor.services.calculos_performance import convert_pace_to_speed, convert_speed_to_pace

                pace = request.form.get('pace')
                speed = request.form.get('speed')

                if pace:
                    velocidade = convert_pace_to_speed(pace)
                    resultado = {
                        "Velocidade": f"{velocidade} km/h"
                    }

                elif speed:
                    pace_convertido = convert_speed_to_pace(float(speed))
                    resultado = {
                        "Pace": f"{pace_convertido} /km"
                    }

                else:
                    error = "Informe o pace ou a velocidade."
                    
                    
            elif tipo == 'km_milhas':
                from conversor.services.calculos_performance import convert_km_to_miles, convert_miles_to_km

                km = request.form.get('km')
                miles = request.form.get('miles')

                if km:
                    milhas = convert_km_to_miles(float(km))
                    resultado = {
                        "Milhas": f"{milhas} mi"
                    }

                elif miles:
                    quilometros = convert_miles_to_km(float(miles))
                    resultado = {
                        "Quilômetros": f"{quilometros} km"
                    }

                else:
                    error = "Informe km ou milhas."  
                    
                    
            elif tipo == 'pace_milha':
                from conversor.services.calculos_performance import pace_km_para_milha, pace_milha_para_km

                pace_km = request.form.get('pace_km')
                pace_mile = request.form.get('pace_mile')

                if pace_km:
                    resultado = {
                        "Pace milha": pace_km_para_milha(pace_km)
                    }

                elif pace_mile:
                    resultado = {
                        "Pace km": pace_milha_para_km(pace_mile)
                    }

                else:
                    error = "Informe um dos campos."
                    
                    
            elif tipo == 'tabela_pace':
                from conversor.services.calculos_performance import gerar_tabela_pace

                pace_inicio = request.form.get('pace_inicio')
                pace_fim = request.form.get('pace_fim')
                intervalo = request.form.get('intervalo')

                tabela_pace = gerar_tabela_pace(pace_inicio, pace_fim, intervalo)
                resultado = None
                
            elif tipo == 'vo2max':
                from conversor.services.calculos_performance import calculate_vo2max
                from conversor.services.formatadores import tempo_para_segundos

                hour = request.form.get('hour')
                minute = request.form.get('minute')
                second = request.form.get('second')

                tempo = tempo_para_segundos(hour, minute, second)

                dados_vo2 = calculate_vo2max(tempo)

                resultado = {
                    "Pace médio 10K": dados_vo2["pace"],
                    "VO2Max estimado": dados_vo2["vo2max"]
                }

                zonas_vo2 = dados_vo2["zonas"]
                
                
            elif tipo == 'vo2max_3k':
                from conversor.services.calculos_performance import calculate_vo2max_3k
                from conversor.services.formatadores import tempo_para_segundos

                hour = request.form.get('hour')
                minute = request.form.get('minute')
                second = request.form.get('second')

                tempo = tempo_para_segundos(hour, minute, second)

                dados = calculate_vo2max_3k(tempo)

                resultado = {
                    "Pace médio 3K": dados["pace"],
                    "VO2Max estimado": dados["vo2max"]
                }

                zonas_vo2 = dados["zonas"]
                
            
            elif tipo == 'previsao_prova':
                from conversor.services.calculos_performance import race_predictions_from_3k
                from conversor.services.formatadores import tempo_para_segundos

                hour = request.form.get('hour')
                minute = request.form.get('minute')
                second = request.form.get('second')

                tempo = tempo_para_segundos(hour, minute, second)

                previsoes_prova = race_predictions_from_3k(tempo, 3)
                resultado = None
                    
                    

        except Exception as e:
            error = "Erro no cálculo"
        

    

    return render_template(
        'ferramentas/calculadora.html',
        tipo=tipo,
        resultado=resultado,
        tabela_pace=tabela_pace,
        error=error,
        form_data=form_data,
        zonas_vo2=zonas_vo2,
        previsoes_prova=previsoes_prova
    )




@app.route('/pessoas', methods=['GET', 'POST'])
@login_required
def pessoas():
    form = PessoaForm()

    if form.validate_on_submit():
        pessoa = Pessoa(
            user_id=current_user.id,
            nome=form.nome.data,
            email=form.email.data,
            peso=form.peso.data,
            objetivo=form.objetivo.data,
            observacoes=form.observacoes.data
        )

        database.session.add(pessoa)
        database.session.commit()

        flash('Pessoa cadastrada com sucesso!', 'success')
        return redirect(url_for('pessoas'))

    pessoas = Pessoa.query.filter_by(user_id=current_user.id).order_by(Pessoa.nome.asc()).all()

    return render_template('pessoas.html', form=form, pessoas=pessoas)

    
    
@app.route('/resumo/publico/<token>')
def resumo_publico(token):
    resumo = ResumoSalvo.query.filter_by(token_publico=token).first_or_404()

    return render_template(
        'plano_publico.html',
        resumo=resumo
    )
    
    
    #testando rotas de importação de CSV (ainda não tem interface, só backend