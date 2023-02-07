import nipyapi
import ssl
from nipyapi import canvas,config
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/home/irshad/data-loader-genie/docker/nifi-ssl/admin-cert.pem', '/home/irshad/data-loader-genie/docker/nifi-ssl/admin-private-key.pem',password='SuperSecret')

# nipyapi.config.nifi_config.host = 'https://localhost:8443/nifi-api'
nipyapi.config.nifi_config.host = 'https://ingestion-devops.dev.prevalent.ai:8443/nifi-api'
# https://ingestion-devops.dev.prevalent.ai:8443/nifi
# root_process_group = canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')

nipyapi.config.nifi_config.verify_ssl = False
nipyapi.utils.set_endpoint('https://ingestion-devops.dev.prevalent.ai:8443/nifi-api')

context_nifi = nipyapi.security.set_service_ssl_context(service='nifi',
                                         client_cert_file='/home/irshad/data-loader-genie/docker/nifi-ssl/tls.pem',
                                         client_key_file='/home/irshad/data-loader-genie/docker/nifi-ssl/tls-key.pem',
                                         # client_key_password='SuperSecret',
                                                        check_hostname=False)

nifi_user_identity = nipyapi.security.get_service_user('CN=Random User')

rpg_id = nipyapi.canvas.get_root_pg_id()

access_policies = [
        ('write', 'process-groups', rpg_id),
        ('read', 'process-groups', rpg_id)
    ]
try:
    for pol in access_policies:
        ap = nipyapi.security.create_access_policy(
            action=pol[0],
            resource=pol[1],
            r_id=pol[2],
            service='nifi'
        )
        nipyapi.security.add_user_to_access_policy(
            nifi_user_identity,
            policy=ap,
            service='nifi'
        )
except:
    pass

root_process_group = canvas.get_process_group(nipyapi.canvas.get_root_pg_id(), 'id')

genie_process_group = nipyapi.canvas.get_process_group("Test", identifier_type='name',
                                                               greedy=True)
print(genie_process_group)