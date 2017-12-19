# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from collections import namedtuple

PublicKey = namedtuple("PublicKey", ["m", "e"])


class RSA:
    # To get modulus and exponent:
    # grep -v -- - public.key | tr -d \\n | base64 -d | openssl asn1parse -inform DER -i

    # TODO Add CDNs keys
    server_public_keys = {
        0xc3b42b026ce86b21 - (1 << 64): PublicKey(  # Main
            # -----BEGIN RSA PUBLIC KEY-----
            # MIIBCgKCAQEAwVACPi9w23mF3tBkdZz+zwrzKOaaQdr01vAbU4E1pvkfj4sqDsm6
            # lyDONS789sVoD/xCS9Y0hkkC3gtL1tSfTlgCMOOul9lcixlEKzwKENj1Yz/s7daS
            # an9tqw3bfUV/nqgbhGX81v/+7RFAEd+RwFnK7a+XYl9sluzHRyVVaTTveB2GazTw
            # Efzk2DWgkBluml8OREmvfraX3bkHZJTKX4EQSjBbbdJ2ZXIsRrYOXfaA+xayEGB+
            # 8hdlLmAjbCVfaigxX0CDqWeR1yFL9kwd9P0NsZRPsmoqVwMbMu7mStFai6aIhc3n
            # Slv8kg9qv1m6XHVQY3PnEw+QQtqSIXklHwIDAQAB
            # -----END RSA PUBLIC KEY-----
            int(
                "C150023E2F70DB7985DED064759CFECF0AF328E69A41DAF4D6F01B538135A6F9"
                "1F8F8B2A0EC9BA9720CE352EFCF6C5680FFC424BD634864902DE0B4BD6D49F4E"
                "580230E3AE97D95C8B19442B3C0A10D8F5633FECEDD6926A7F6DAB0DDB7D457F"
                "9EA81B8465FCD6FFFEED114011DF91C059CAEDAF97625F6C96ECC74725556934"
                "EF781D866B34F011FCE4D835A090196E9A5F0E4449AF7EB697DDB9076494CA5F"
                "81104A305B6DD27665722C46B60E5DF680FB16B210607EF217652E60236C255F"
                "6A28315F4083A96791D7214BF64C1DF4FD0DB1944FB26A2A57031B32EEE64AD1"
                "5A8BA68885CDE74A5BFC920F6ABF59BA5C75506373E7130F9042DA922179251F",
                16
            ),  # Modulus
            int("010001", 16)  # Exponent
        ),
        0x15931aac70e0d30f7 - (1 << 64): PublicKey(  # CDN DC121 (Test)
            # -----BEGIN RSA PUBLIC KEY-----
            # MIIBCgKCAQEA+Lf3PvgE1yxbJUCMaEAkV0QySTVpnaDjiednB5RbtNWjCeqSVakY
            # HbqqGMIIv5WCGdFdrqOfMNcNSstPtSU6R9UmRw6tquOIykpSuUOje9H+4XVIKquj
            # yL2ISdK+4ZOMl4hCMkqauw4bP1Sbr03vZRQbU6qEA04V4j879BAyBVhr3WG9+Zi+
            # t5XfGSTgSExPYEl8rZNHYNV5RB+BuroVH2HLTOpT/mJVfikYpgjfWF5ldezV4Wo9
            # LSH0cZGSFIaeJl8d0A8Eiy5B9gtBO8mL+XfQRKOOmr7a4BM4Ro2de5rr2i2od7hY
            # Xd3DO9FRSl4y1zA8Am48Rfd95WHF3N/OmQIDAQAB
            # -----END RSA PUBLIC KEY-----
            int(
                "F8B7F73EF804D72C5B25408C6840245744324935699DA0E389E76707945BB4D5"
                "A309EA9255A9181DBAAA18C208BF958219D15DAEA39F30D70D4ACB4FB5253A47"
                "D526470EADAAE388CA4A52B943A37BD1FEE175482AABA3C8BD8849D2BEE1938C"
                "978842324A9ABB0E1B3F549BAF4DEF65141B53AA84034E15E23F3BF410320558"
                "6BDD61BDF998BEB795DF1924E0484C4F60497CAD934760D579441F81BABA151F"
                "61CB4CEA53FE62557E2918A608DF585E6575ECD5E16A3D2D21F471919214869E"
                "265F1DD00F048B2E41F60B413BC98BF977D044A38E9ABEDAE01338468D9D7B9A"
                "EBDA2DA877B8585DDDC33BD1514A5E32D7303C026E3C45F77DE561C5DCDFCE99",
                16
            ),  # Modulus
            int("010001", 16)  # Exponent
        )
    }

    @classmethod
    def encrypt(cls, data: bytes, fingerprint: int) -> bytes:
        return int.to_bytes(
            pow(
                int.from_bytes(data, "big"),
                cls.server_public_keys[fingerprint].e,
                cls.server_public_keys[fingerprint].m
            ),
            256,
            "big"
        )
