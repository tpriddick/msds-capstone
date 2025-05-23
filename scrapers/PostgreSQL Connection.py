# PostgreSQL Connection
from sqlalchemy import URL, create_engine

con = create_engine(
    URL.create('postgresql',
    database = 'railway',
    host = 'roundhouse.proxy.rlwy.net',
    port = 44826,
    username = 'postgres',
    password = 'WjValpnjgoYyLCVqoPrZhiSbVwdbgbUh')
)
