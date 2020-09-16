import os

GLOBAL_TOPIC = os.getenv('GLOBAL_TOPIC', 'dev_walkathon_global')
DEBUG = os.getenv('DEBUG', 'True')
SECRET_KEY = os.getenv('DEBUG', 'ee!r^oi3s8iezw(^yill5er^u=@5fecshgizc-xzr=+-7t$)+-')

DATABASE_NAME = os.getenv('DATABASE_NAME', 'SKU_Avon')
DATABASE_USER = os.getenv('DATABASE_USER', 'SKU_Avon')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'M0t0r0la12345')
DATABASE_HOST = os.getenv('DATABASE_HOST', 'dedi860.jnb3.host-h.net')
DATABASE_PORT = os.getenv('DATABASE_PORT', '3306')

# DATABASE_NAME = os.getenv('DATABASE_NAME', 'avonJ001')
# DATABASE_USER = os.getenv('DATABASE_USER', 'avonJ001')
# DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD', 'M0t0r0la12345')
# DATABASE_HOST = os.getenv('DATABASE_HOST', 'dedi860.jnb3.host-h.net')
# DATABASE_PORT = os.getenv('DATABASE_PORT', '3306')