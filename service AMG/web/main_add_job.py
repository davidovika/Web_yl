from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user

from data import db_session
from data.add_job import AddJobForm
from data.login_form import LoginForm
from data.users import User
from data.jobs import Jobs
from data.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
SERVICE = {
    'technical_maintenance':{
        'name': 'техническое обслуживание',
        'description': 'Техническое обслуживание автомобиля — процесс, необходимый для поддержания автомобиля в рабочем состоянии. Для того, чтобы эксплуатация автомобиля была комфортной, безопасной, длительной и экономичной, важно, чтобы техническое обслуживание было регулярным.',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'technical_maintenance.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'mercedes_benz_auto_start':{
        'name': 'автозапуск mercedes-benz',
        'description': 'Работает автозапуск достаточно просто — автомобиль заводится и глушится при помощи команды — трех нажатий кнопки закрытия.\nПосле дистанционного запуска двигателя автомобиль остается в режиме охраны, двери будут закрыты и для попадания в салон необходимо на ключе нажать кнопку открытия. Но даже оказавшись в салоне, при попытке тронуться, без ключа в замке зажигания, автомобиль сразу заглохнет. Поэтому владельцу ключ нужен всегда',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'mercedes_benz_auto_start.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'painting_and_body_repair':{
        'name': 'малярно-кузовной ремонт',
        'description': 'Внешний вид автомобиля имеет немаловажное значение для его владельца. \n Мы понимаем, что работы по кузовному ремонту должны выполняться с максимальным качеством и в кратчайшие сроки. \n В «ТехЦентр АМГ», Вы можете осуществить полный комплекс услуг по ремонту PREMIUM автомобилей, окраске, тонировке, удалению вмятин без окраски, шумоизоляции, вклейки стекл, химчистки салона, полировки кузова и фар, а также сварочным работам.',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'painting_and_body_repair.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'chip_tuning':{
        'name': 'чип-тюнинг',
        'description': 'Совершенно новый уровень мощности, плавности хода и экономичности двигателя вашего Mercedes-Benz – без технического вмешательства в работу его узлов.\nПолучите 100% безопасности и максимум эффективности двигателя для вашего стиля вождения!',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'chip_tuning.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'disabling_adblue_and_bluetec':{
        'name': 'отключение ADBLUE и BLUETEC',
        'description': 'Современные дизельные автомобили Мерседес для соответствия последним Европейским нормативам по экологии (Euro 5 и Euro 6) оборудованы системами AdBlue BlueTec SCR.\nМинус системы AdBlue в том, что при ее неисправности блокируется дальнейшая возможность эксплуатации автомобиля!',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'disabling_adblue_and_bluetec.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'mercedes_benz_coding':{
        'name': 'кодирование mercedes benz',
        'description': 'Кодирование Мерседес используется для активации различных скрытых программных функций, для дооснащения и прописывания установленного оборудования, я так же в диагностических и ремонтных целях.',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'mercedes_benz_coding.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'computer_diagnostics':{
        'name': 'компьютерная диагностика',
        'description': 'Компьютерная диагностика включает в себя:\n*Диагностика электронных систем ДВС\n*Диагностика электронных систем АКПП и РКПП\n* Диагностика инжектора\n* Диагностика ABS, SRS, ESP\n* Диагностика считывания кодов ошибок с ЭБУ',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'computer_diagnostics.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'engine_repair':{
        'name': 'ремонт двигателей',
        'description': 'Ремонт двигателя длится, по меньшей мере, несколько дней. В зависимости от степени повреждения узла, работы могут занять срок до месяца и даже более. После окончания работ водителю следует быть осторожнее. Примерно 1000 километров нужно избегать «гоночного» режима вождения. В этот период все детали обкатываются, мастера следят за расходом топлива и масла.',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'engine_repair.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'repair_of_automatic_transmission_and_manual_transmission':{
        'name': 'ремонт двигателей',
        'description': '',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'repair_of_automatic_transmission_and_manual_transmission.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'collapse_convergence':{
        'name': 'развал-схождения',
        'description': 'Положение колеса автомобиля должно быть идеальным, небольшой уклон в 1-2 градуса по одной из осей может привести к серьезным последствиям. В первую очередь, это влияет на управляемость автомобиля, может стать причиной ДТП. Покрышки при неправильном сход-развале изнашиваются быстрее, а это серьезные финансовые затраты. Еще один минус данного дефекта – повышенная нагрузка на сопряженные детали подвески, что увеличивает расход топлива и износ ходовой части.',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'collapse_convergence.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'autoelectrics':{
        'name': 'автоэлектрика',
        'description': 'Установка автосигнализации\nУстановка ксенона и биксенона\nУстановка патронников\nЗамена электрических элементов автомобиля\nРемонт проводки в эл. узлах автомобиля',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'autoelectrics.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'tire_service':{
        'name': 'шиномонтаж',
        'description': '',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'tire_service.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'refueling_or_repairing_an_air_conditioner':{
        'name': 'заправка/ремонт кондиционера',
        'description': 'Заправка и ремонт кондиционеров в автомобилях — это услуги по поддержанию работоспособности системы кондиционирования, которая обеспечивает комфортный микроклимат в салоне. Они включают восстановление уровня хладагента, устранение неисправностей и профилактику поломок. ',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'refueling_or_repairing_an_air_conditioner.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'locksmith_work':{
        'name': 'слесарные работы',
        'description': 'Слесарные работы — это комплекс мероприятий по техническому обслуживанию, диагностике, ремонту и замене деталей и узлов автомобиля. Их выполняют автослесари в автосервисах с применением специального оборудования и инструментов. Цель — поддерживать автомобиль в исправном состоянии, обеспечивать безопасность движения и продлевать срок службы узлов и агрегатов.',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'locksmith_work.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    },
    'car_glass_replacement':{
        'name': 'замена автостекл',
        'description': 'Компания «ТехЦентр АМГ» предлагает своим клиентам высококачественный сервис по подбору и замене автостекла. Квалифицированные и опытные специалисты произведут замену лобового стекла, заднего стекла и любого другого вида автостекла на высоком профессиональном уровне. Мы сосредотачиваем максимум усилий на оттачивании навыков и умений, гарантируем сжатые сроки выполнения каждой заявки. Работаем исключительно на результат и находим индивидуальный подход к каждому клиенту.',
        'price': 'Чтобы узнать стоимость на техническое обслуживание автомобиля, вы можете оставить заявку на сайте',
        'image': 'car_glass_replacement.jpg',
        'benefits': 'На все работы предоставляется гарантия.'
    }
}


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Wrong login or password", form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    users = db_sess.query(User).all()
    names = {name.id: (name.surname, name.name) for name in users}
    return render_template("index.html", jobs=jobs, names=names, title='Work log', services=SERVICE)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Register', form=form,
                                   message="Passwords don't match")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form,
                                   message="This user already exists")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/addjob', methods=['GET', 'POST'])
def addjob():
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs(
            job=add_form.job.data,
            team_leader=add_form.team_leader.data,
            work_size=add_form.work_size.data,
            collaborators=add_form.collaborators.data,
            is_finished=add_form.is_finished.data
        )
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Adding a job', form=add_form)

@app.route('/service/<service_key>')
def service_detail(service_key):

    service = SERVICE.get(service_key)

    if not service:
        return "Услуга не найдена", 404

    return render_template('service_detail.html', service=service, service_key=service_key)


def main():
    db_session.global_init("db/mars_explorer.sqlite")

    app.run()


if __name__ == '__main__':
    main()
