import os
from django.conf import settings

CACHE_ROOT = getattr(settings, 'STATIC_PRECOMPILE_CACHE_ROOT', None) or\
              getattr(settings, 'STATIC_ROOT', None) or\
              os.path.join(
                getattr(settings,'PROJECT_ROOT', getattr(settings, 'BASE_DIR')),
                '.static_precompile_cache'
              )

SASS_EXTENSION = getattr(settings, 'STATIC_PRECOMPILE_SASS_EXTENSION', 'sass')

HANDLEBARS_EXTENSION = getattr(settings, 'STATIC_PRECOMPILE_HANDLEBARS_EXTENSION', 'hbs')

USE_COMPASS = getattr(settings, 'STATIC_PRECOMPILE_USE_COMPASS', True)
