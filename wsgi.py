import os
from sauce import create_app

app = create_app(config=os.environ.get('SAUCE_CONFIG', 'config.dev'))
