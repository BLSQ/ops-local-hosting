import subprocess
import uuid
import yaml
import re
import bcrypt

def generate_random_password():
  return uuid.uuid4().hex


def generate_portainer_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12))
    hashed_password = hashed_password.decode('utf-8').replace('$2b$', '$2y$')
    return re.sub(r'\$', r'$$', hashed_password)

def get_input_with_default(prompt, default):
    value = input(f"{prompt} ({default}): ").strip()
    return value or default

# Ansible connection details
is_localhost = input("Will you run Ansible directly on the server [Y/n]?: ").strip().lower() == "y"
server_ip = "localhost" if is_localhost else input("Enter the server public IP (SSH connection): ").strip()
ansible_user = input("Enter the username of the server: ").strip()

# BLSQ products list
available_products = ["dhis2", "iaso", "hesabu", "dataviz", "superset"]
print("Available products:")
for i, product in enumerate(available_products, 1):
    print(f"{i}. {product}")

# Select products to install 
selected_products_indices = input("Enter the number of the products you want to install (separate by commas for multiple): ").strip()
selected_products_indices = [int(i) - 1 for i in selected_products_indices.split(",")]
selected_products = [available_products[i] for i in selected_products_indices]

blsq_products_regexp = f".*(?:{'|'.join(selected_products)}).*"

# Traefik and ACME
traefik_pwd = generate_random_password()
acme_email = input("Enter your email for ACME: ").strip()
domain_name = input("Enter your domain name: ").strip()
has_proxy = input("Is TLS/HTTPS already handled by an external reverse proxy [Y/n]?: ").strip().lower() == "y"
tls_enabled = not has_proxy
portainer_password = generate_portainer_password(traefik_pwd)


# Set default subdomain names based on the main domain
default_dhis2_domain = f"dhis2.{domain_name}"
default_iaso_domain = f"iaso.{domain_name}"
default_enketo_domain = f"enketo.{domain_name}"
default_hesabu_domain = f"hesabu.{domain_name}"
default_dataviz_backend_domain = f"dataviz-backend.{domain_name}"
default_dataviz_frontend_domain = f"dataviz.{domain_name}"
default_minio_domain = f"minio.{domain_name}"
default_superset_domain = f"superset.{domain_name}"

# Additional variables for selected products
additional_vars = {}

# Minio
if any(product in selected_products for product in ["iaso", "dataviz", "hesabu"]):
    additional_vars["MINIO_ROOT_USER"] = "miniouser"
    additional_vars["MINIO_ROOT_PASSWORD"] = generate_random_password()
    minio_domain_name = get_input_with_default("Enter Minio domain name", default_minio_domain)

    additional_vars.update({
        "MINIO_DOMAIN_NAME": minio_domain_name,
    })

# Iaso
if "iaso" in selected_products:
    iaso_domain_name = get_input_with_default("Enter Iaso domain name", default_iaso_domain) 

    additional_vars.update({
        "ENKETO_API_KEY": generate_random_password(),
        "IASO_VERSION": "be4d3bec7706a188a716c039f79dcdee342870fd",
        "IASO_DB_HOST": "db",
        "IASO_DB_NAME": "iaso",
        "IASO_DB_USER": "iaso",
        "IASO_DB_PASSWORD": generate_random_password(),
        "IASO_SECRET_KEY": generate_random_password(),
        "IASO_DOMAIN_NAME": iaso_domain_name,

    })

# Hesabu
if "hesabu" in selected_products:
    hesabu_domain_name = get_input_with_default("Enter Hesabu domain name", default_hesabu_domain)

    additional_vars.update({
        "HESABU_VERSION": "1.0.323.g6b14240d",
        "HESABU_POSTGRES_VERSION": "16",
        "HESABU_POSTGRES_USER": "hesabu",
        "HESABU_POSTGRES_DB": "orbf2",
        "HESABU_POSTGRES_PASSWORD": generate_random_password(),
        "HESABU_REDIS_VERSION": "6.2.5",
        "HESABU_REDIS_PASSWORD": generate_random_password(),
        "HESABU_ADMIN_PASSWORD": generate_random_password(),
        "HESABU_MONITORING_TOKEN": generate_random_password(),
        "HESABU_SECRET_KEY_BASE": generate_random_password(),
        "HESABU_DOMAIN_NAME": hesabu_domain_name,
    })

# Dataviz
if "dataviz" in selected_products:
    dataviz_backend_domain_name = get_input_with_default("Enter Dataviz backend domain name", default_dataviz_backend_domain)
    dataviz_frontend_domain_name = get_input_with_default("Enter Dataviz frontend domain name", default_dataviz_frontend_domain)
   
    additional_vars.update({
        "DATAVIZ_BACKEND_VERSION": "00f61a7.0.0",
        "DATAVIZ_FRONT_VERSION": "vORBF.1033.gf7f076a",
        "DATAVIZ_REDIS_VERSION": "6.2.5",
        "DATAVIZ_REDIS_PASSWORD": generate_random_password(),
        "DATAVIZ_POSTGRES_VERSION": "16",
        "DATAVIZ_POSTGRES_DB": "dataviz",
        "DATAVIZ_POSTGRES_USER": "dataviz",
        "DATAVIZ_POSTGRES_PASSWORD": generate_random_password(),
        "DATAVIZ_ADMIN_PASSWORD": generate_random_password(),
        "DATAVIZ_MONITORING_TOKEN": generate_random_password(),
        "DATAVIZ_SECRET_KEY_BASE": generate_random_password(),
        "DATAVIZ_BACKEND_DOMAIN_NAME": dataviz_backend_domain_name,
        "DATAVIZ_FRONT_DOMAIN_NAME": dataviz_frontend_domain_name
    })

# Superset
if "superset" in selected_products:
    superset_domain_name = get_input_with_default("Enter Superset domain name", default_superset_domain)
    additional_vars.update({
        "SUPERSET_POSTGRES_VERSION": "16",
        "SUPERSET_POSTGRES_HOST": "db",
        "SUPERSET_POSTGRES_DB": "superset",
        "SUPERSET_POSTGRES_USER": "superset",
        "SUPERSET_POSTGRES_PASSWORD": generate_random_password(),
        "SUPERSET_ADMIN_PASSWORD": generate_random_password(),
        "SUPERSET_SECRET_KEY": generate_random_password(),
        "SUPERSET_GUEST_TOKEN_JWT_SECRET": str(uuid.uuid4())
    })

#
if "dhis2" in selected_products:
    additional_vars["DHIS2_DATABASE_USER"] = "dhis2"
    additional_vars["DHIS2_DATABASE_NAME"] = "dhis2"
    dhis2_db_host = input("Enter DHIS2 database host (private IP): ").strip()
    dhis2_postgres_version = input("Enter DHIS2 Postgres version: ").strip()
    dhis2_domain_name = get_input_with_default("Enter DHIS2 domain name", default_dhis2_domain)
    dhis2_version = input("Enter DHIS2 version: ").strip()

    additional_vars.update({
        "DHIS2_DATABASE_PASSWORD": generate_random_password(),
        "DHIS2_DATABASE_HOST": dhis2_db_host,
        "DHIS2_POSTGRES_VERSION": dhis2_postgres_version,
        "DHIS2_DOMAIN_NAME": dhis2_domain_name,
        "DHIS2_VERSION": dhis2_version
    })


# Inventory file
inventory = {
    "all": {
        "children": {
            "iaso": {
                "hosts": {
                    server_ip: {
                        "ansible_user": ansible_user,
                        **({"ansible_connection": "local"} if is_localhost else {}), 
                        "config_system_locale": "en_US.UTF-8" , 
                        "PORTAINER_PASSWORD": portainer_password,                     
                        "TRAEFIK_PWD": traefik_pwd,
                        "TRAEFIK_USER": "admin",
                        "TRAEFIK_VERSION": "v3.6.2",
                        "ACME_EMAIL": acme_email,
                        "DOMAIN_NAME": domain_name,
                        **additional_vars,
                        "blsq_products_regexp": blsq_products_regexp,
                        "TLS_ENABLED": tls_enabled
                    }
                }
            },
            "ungrouped": {}
        }
    }
}

with open("../inventory.yml", "w") as f:
    yaml.dump(inventory, f, default_flow_style=False, sort_keys=False)

print("\nInventory generated: inventory.yml\n")
print(yaml.dump(inventory, default_flow_style=False, sort_keys=False))
