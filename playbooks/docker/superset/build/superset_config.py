import os
RDS_USERNAME = os.getenv('RDS_USERNAME')
RDS_PASSWORD = os.getenv('RDS_PASSWORD')
RDS_PORT = os.getenv('RDS_PORT')
RDS_HOSTNAME = os.getenv('RDS_HOSTNAME')
RDS_DB_NAME = os.getenv('RDS_DB_NAME')
SQLALCHEMY_DATABASE_URI = f'postgresql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}'
MAPBOX_API_KEY = os.getenv('MAPBOX_API_KEY', None)

GUEST_ROLE_NAME = "Gamma"
FEATURE_FLAGS = {
      "DYNAMIC_PLUGINS": True,
      "HORIZONTAL_FILTER_BAR": os.getenv("HORIZONTAL_FILTER_BAR", "true").lower() == "true",
      "ALLOW_ADHOC_SUBQUERY": True,
      "ALERTS_ATTACH_REPORTS": True,
      "DASHBOARD_CROSS_FILTERS": True,
      "DASHBOARD_RBAC": True,
      "EMBEDDABLE_CHARTS": True,
      "EMBEDDED_SUPERSET": True,
      "ENABLE_JAVASCRIPT_CONTROLS": True,
      "ENABLE_TEMPLATE_PROCESSING": True,
      "LISTVIEWS_DEFAULT_CARD_VIEW": False,
      "SQL_VALIDATORS_BY_ENGINE": True,
      "THUMBNAILS": False,
      "ALLOW_FULL_CSV_EXPORT": True,
    }
TALISMAN_ENABLED = False
SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_SECURE = True
ENABLE_PROXY_FIX = False
GUEST_TOKEN_JWT_SECRET = os.getenv('GUEST_TOKEN_JWT_SECRET')
GUEST_TOKEN_JWT_EXP_SECONDS = 3600  # 1 hour
ENABLE_CORS=False
HTTP_HEADERS = {
  'X-Frame-Options': 'ALLOWALL'
}

# Not ideal, but a quick fix to let the ITM download all participants data.
SQL_MAX_ROW=1000000
SQLLAB_TIMEOUT=120 # default 60
SUPERSET_WEBSERVER_TIMEOUT=120 # default 60

# Increase the max dashboard size to 10 MB, the default of 65535 bytes is too low.
# https://github.com/apache/superset/issues/15169#issuecomment-1011902952
SUPERSET_DASHBOARD_POSITION_DATA_LIMIT = 10000000 # 10 MB