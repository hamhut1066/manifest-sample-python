import json

from jwcrypto import jwk, jws
from jwcrypto.common import json_encode
# A script to build a manifest file ready for upload to the registry
# See bottom of file for what we are trying to generate

# Our payload minus the signatures key
payload = {
  "schemaVersion": 1,
  "name": "moredhel/test",
  "tag": "testing",
  "architecture": "amd64",
  "fsLayers": [
    {
      "blobSum": "sha256:6d987f6f42797d81a318c40d442369ba3dc124883a0964d40b0c8f4f7561d913"
    }
  ],
  "history": [
    {
      "v1Compatibility": "{\"architecture\":\"amd64\",\"comment\":\"Imported from -\",\"config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":null,\"Cmd\":null,\"Image\":\"\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"container_config\":{\"Hostname\":\"\",\"Domainname\":\"\",\"User\":\"\",\"AttachStdin\":false,\"AttachStdout\":false,\"AttachStderr\":false,\"Tty\":false,\"OpenStdin\":false,\"StdinOnce\":false,\"Env\":null,\"Cmd\":null,\"Image\":\"\",\"Volumes\":null,\"WorkingDir\":\"\",\"Entrypoint\":null,\"OnBuild\":null,\"Labels\":null},\"created\":\"2018-01-18T10:24:34.112276782Z\",\"docker_version\":\"17.12.0-ce\",\"id\":\"78682976813c03845c5155a3d0ea9510f3addf67410bc47f211e45f866b2352e\",\"os\":\"linux\"}"
    }
  ],
}

# Generate the Json web Key
key = jwk.JWK.generate(kty='EC')
print(key.export())

# Create the Web Token, payload is being dumped to json
jwstoken = jws.JWS(json.dumps(payload))

# Add signing key
jwstoken.add_signature(key, None,
                           json_encode({"alg": "ES256"}),
                           json_encode({"kid": key.thumbprint()}))
sig = jwstoken.serialize()
print(sig)

# This is what we are trying to replicate...
"""
  "signatures": [
    {
      "header": {
        "jwk": {
          "crv": "P-256",
          "kid": "RWEW:AUWQ:HF5Z:4AOL:DXDC:CCMK:5V2I:GRTV:7CED:ATZS:6KKK:IVDG",
          "kty": "EC",
          "x": "LuL5N1Y1eRA23PqREItorn8IHEGZNi9Rz8ADRE65Ovk",
          "y": "i23NudaR2sV3Z4aZD-S3SFYTLwqF8Ln0dr48tikXUJ4"
        },
        "alg": "ES256"
      },
      "signature": "n0tcl5tPttSnvzrc6rZHTDrUuG8xefyKhcngdvsfxvM8ixMYUI7REe0qXD-2YoHJXCy5XDC3s3j0-8Hi-hqrnw",
      "protected": "eyJmb3JtYXRMZW5ndGgiOjExODIsImZvcm1hdFRhaWwiOiJDbjAiLCJ0aW1lIjoiMjAxOC0wMS0xOFQxMDoyNTo0NVoifQ"
    }
  ]
"""
