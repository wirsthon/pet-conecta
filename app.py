import os

from flask import Flask, flash, redirect, request, url_for

from extensions import db, login_manager


def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-only-nao-use-em-producao')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    if config:
        app.config.update(config)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from auth import auth_bp
    from views import views_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(views_bp)

    @app.errorhandler(413)
    def arquivo_grande(erro):
        flash('A imagem é grande demais. O limite é 5 MB.', 'erro')
        return redirect(request.referrer or url_for('views.index'))

    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=False)
