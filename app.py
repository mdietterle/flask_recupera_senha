from flask import Flask, request, render_template, redirect, url_for, flash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
import os

app = Flask(__name__)
app.secret_key = 'secret_key'  # Chave de segurança para cookies de sessão

# Configuração de e-mail (substitua com as suas credenciais)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'martim.dietterle@gmail.com'
app.config['MAIL_PASSWORD'] = 'bhxk upst mafb qkvi'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

# Serializer para gerar tokens seguros
s = URLSafeTimedSerializer(app.secret_key)

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para solicitar a recuperação de senha
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']

        # Aqui você verificaria no banco de dados se o email está registrado
        # Se o e-mail for válido, envie o e-mail de redefinição
        token = s.dumps(email, salt='password-recovery')

        msg = Message('Redefinição de Senha', sender='seu_email@gmail.com', recipients=[email])
        link = url_for('reset_password', token=token, _external=True)
        msg.body = f'Clique no link para redefinir sua senha: {link}'
        mail.send(msg)

        flash('Um link de recuperação foi enviado para seu e-mail.', 'success')
        return redirect(url_for('index'))

    return render_template('forgot_password.html')

# Rota para redefinir a senha
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='password-recovery', max_age=3600)  # Token válido por 1 hora
    except SignatureExpired:
        return '<h1>O link de redefinição expirou.</h1>'
    except BadSignature:
        return '<h1>Token inválido.</h1>'

    if request.method == 'POST':
        new_password = request.form['password']
        # Aqui você atualizaria a senha no banco de dados
        flash('Sua senha foi redefinida com sucesso.', 'success')
        return redirect(url_for('index'))

    return render_template('reset_password.html')

if __name__ == '__main__':
    app.run(debug=True)
