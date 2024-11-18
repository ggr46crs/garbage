from pathlib import Path

basedir = Path(__file__).parent.parent

# BaseConfigクラスを作成
class BaseConfig:
    SECRET_KEY = "{SECRET_KEY}"

# BaseConfigクラスを継承しLocalConfigクラスを作成
class LocalConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{password}@{host}/{name}'.format(**{
        'user': 'postgres',
        'password': 'ohara2024',
        'host': 'localhost:5432',
        'name': 'garbage'
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# config辞書にマッピング
config = {
    "local": LocalConfig,
}