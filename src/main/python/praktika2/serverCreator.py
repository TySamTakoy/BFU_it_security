from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime

# Создаём папку server рядом со скриптами
Path("server").mkdir(exist_ok=True)

# Генерируем ключ
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Создаём самоподписанный сертификат
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Kaliningrad region"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, "Kaliningrad"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "BFU"),
    x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
])

cert = (
    x509.CertificateBuilder()
    .subject_name(subject)
    .issuer_name(issuer)
    .public_key(key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(datetime.datetime.utcnow())
    .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    .add_extension(x509.SubjectAlternativeName([x509.DNSName("localhost")]), critical=False)
    .sign(key, hashes.SHA256())
)

# Сохраняем ключ и сертификат
with open("server/key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("server/cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("Сертификат и ключ созданы в папке 'server'")