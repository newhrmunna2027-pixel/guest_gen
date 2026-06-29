# -*- coding: utf-8 -*-
import os
import sys

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

print("\033[1;36m[*] Initializing The Lobby Lord Engine...\033[0m")

def check_and_install_dependencies():
    packages = {"aiohttp": "aiohttp", "pycryptodome": "Crypto", "protobuf": "google.protobuf", "rich": "rich"}
    missing = False
    for pkg, mod in packages.items():
        try:
            __import__(mod.split('.')[0])
        except ImportError:
            missing = True
            break
            
    if missing:
        print("\033[1;33m[*] Installing required packages, please wait...\033[0m")
        os.system(f"{sys.executable} -m pip install aiohttp pycryptodome protobuf rich --quiet")
        print("\033[1;32m[*] Packages installed! Restarting...\033[0m")
        os.execv(sys.executable, ['python'] + sys.argv)

check_and_install_dependencies()


import hmac
import hashlib
import json
import random
import asyncio
import aiohttp
from aiohttp import web
import re
import traceback
import uuid
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

from rich.console import Console
from rich.panel import Panel

R = '\033[1;31m'
C = '\033[1;36m'
G = '\033[1;32m'
Y = '\033[1;33m'
W = '\033[1;37m'
D = '\033[0m'
K = '\033[90m'

_T = [84, 104, 101, 32, 76, 111, 98, 98, 121, 32, 76, 111, 114, 100]
_O = [79, 85, 84, 95, 79, 70, 95, 76, 65, 87]
_Q = [81, 85, 69, 69, 78, 95, 79, 70, 95, 76, 65, 87]
TITLE = "".join(chr(c) for c in _T)
AUTHOR = "".join(chr(c) for c in _O)
QUEEN = "".join(chr(c) for c in _Q)

FORMAT_MODE = "all"

# ==========================================
# === VERIFIED DEVICE PROFILES ===
# ==========================================
DEVICE_PROFILES = [
    {
        "os": "Android OS 13 / API-33",
        "os_ver_only": "Android 13",
        "cpu_short": "sm8350",
        "cpu_long": "Qualcomm Snapdragon 888 | 8 cores",
        "gpu": "Adreno (TM) 660",
        "opengl": "OpenGL ES 3.2 V@512.0",
        "width": 1440,
        "height": 3216,
        "dpi": "520",
        "ram": 12288,
        "operator": "Banglalink"
    },
    {
        "os": "Android OS 12 / API-31",
        "os_ver_only": "Android 12",
        "cpu_short": "exynos2100",
        "cpu_long": "Exynos 2100 | 8 cores",
        "gpu": "Mali-G78 MP14",
        "opengl": "OpenGL ES 3.2 v1.r26p0",
        "width": 1080,
        "height": 2400,
        "dpi": "420",
        "ram": 8192,
        "operator": "Grameenphone"
    },
    {
        "os": "Android OS 11 / API-30",
        "os_ver_only": "Android 11",
        "cpu_short": "sm7150",
        "cpu_long": "Qualcomm Snapdragon 732G | 8 cores",
        "gpu": "Adreno (TM) 618",
        "opengl": "OpenGL ES 3.2 V@502.0",
        "width": 1080,
        "height": 2400,
        "dpi": "440",
        "ram": 6144,
        "operator": "Robi"
    }
]

CONFIG = {
    "TOTAL_ACCOUNTS": "all",  
    "CONCURRENT_LIMIT": 40,   
    "BADGES": {
        "new_×": [
            "ⓞUTㅤOFㅤLAW",     
            "ⓞutㅤOFㅤLaw",  
            "ⓞUTㅤOfㅤLAW", 
            "ⓞutㅤofㅤlaw", 
            "ⓞUTㅤOFㅤlaw", 
            "ⓞutㅤOFㅤLAW", 
            "ⓞutㅤOFㅤLAW", 
            "ⓞutㅤOfㅤLAW", 
            "ⓞutㅤofㅤLAW"
        ],
        "new_ori": [
            "OUT-0F-LaW",     
            "Out-0F-Law",  
            "OUT-0f-LAW", 
            "Out-0f-law"
        ],
        "Aʟᴠɪ_Sɪʀ": [
            "AʟᴠɪㅤSɪʀㅤ"
        ],
        "GHOST_MODE": [
            "ㅤㅤㅤㅤ⚡ㅤㅤㅤ⚡",
            "ㅤㅤㅤㅤ⚡ㅤㅤㅤ⚡"
        ],
        "SHAWON_DAD": [
            "SHAWONㅤDAD"
        ],
        "LAW": [
            "ᴸᵃʷㅤ",
            "ʟᴀᴡㅤ",
            "Lαωㅤ",
            "ＬＡＷㅤ"
        ],
        "fokinni": [
            "—͞SABBIR友!"
        ],
        "Zyron": [
            "_Xyron__"
        ],
        "out_of_law": [
            "OUT☆OF☆LAW",
            "out☆of☆law",
            "Out☆of☆Law"
        ],
        "KING_ADOR": [
            "IIㅤ—͞RIOㅤ"
        ],
        "HK": [
            "Hukexㅤ",
            "HUXEKㅤ",
            "hukexㅤ"
        ],
        "RUDRA": [
            "Ummmmahㅤ"
        ],
        "new1": [
            "Oᴜᴛ_ⓞꜰ_ʟᴀᴡ",
            "Oᴜᴛ-ⓞꜰ-ʟᴀᴡ",
            "Oᴜᴛㅤⓞꜰㅤʟᴀᴡ"
        ],
        "RULER": [
            "_Ruler___"
        ],
        "ador": [
            "_Ꭺᴅ፝֟፝֟oʀ___"
        ],
        "alvi": [
            "AʟᴠɪㅤSɪʀㅤ"
        ]
    },     

    "EXTRA": [
        "⓪", "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩", 
        "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳",
        "㉑", "㉒", "㉓", "㉔", "㉕", "㉖", "㉗", "㉘", "㉙", "㉚", 
        "㉛", "㉜", "㉝", "㉞", "㉟", "㊱", "㊲", "㊳", "㊴", "㊵",
        "㊶", "㊷", "㊸", "㊹", "㊺", "㊻", "㊼", "㊽", "㊾", "㊿",
        "⓿", "❶", "❷", "❸", "❹", "❺", "❻", "❼", "❽", "❾", "❿", 
        "⓫", "⓬", "⓭", "⓮", "⓯", "⓰", "⓱", "⓲", "⓳", "⓴",
        "⓵", "⓶", "⓷", "⓸", "⓹", "⓺", "⓻", "⓼", "⓽", "⓾",
        "⑴", "⑵", "⑶", "⑷", "⑸", "⑹", "⑺", "⑻", "⑼", "⑽",
        "⑾", "⑿", "⒀", "⒁", "⒂", "⒃", "⒄", "⒅", "⒆", "⒇",
        "⒈", "⒉", "⒊", "⒋", "⒌", "⒍", "⒎", "⒏", "⒐", "⒑",
        "⒒", "⒓", "⒔", "⒕", "⒖", "⒗", "⒘", "⒙", "⒚", "⛛",
        "Ⅰ", "Ⅱ", "Ⅲ", "Ⅳ", "Ⅴ", "Ⅵ", "Ⅶ", "Ⅷ", "Ⅸ", "Ⅹ", "Ⅺ", "Ⅻ",
        "ⅰ", "ⅱ", "ⅲ", "ⅳ", "ⅴ", "ⅵ", "ⅶ", "ⅷ", "ⅸ", "ⅹ", "ⅺ", "ⅻ",
        "Ⅼ", "Ⅽ", "Ⅾ", "Ⅿ", "ⅼ", "ⅽ", "ⅾ", "ⅿ", 
        "ⓐ", "ⓑ", "ⓒ", "ⓓ", "ⓔ", "ⓕ", "ⓖ", "ⓗ", "ⓘ", "ⓙ",
        "ⓚ", "ⓛ", "ⓜ", "ⓝ", "ⓞ", "ⓟ", "ⓠ", "ⓡ", "ⓢ", "ⓣ",
        "ⓤ", "ⓥ", "ⓦ", "ⓧ", "ⓨ", "ⓩ",
        "Ⓐ", "Ⓑ", "Ⓒ", "Ⓓ", "Ⓔ", "Ⓕ", "Ⓖ", "Ⓗ", "Ⓘ", "Ⓙ",
        "Ⓚ", "Ⓛ", "Ⓜ", "Ⓝ", "Ⓞ", "Ⓟ", "Ⓠ", "Ⓡ", "Ⓢ", "Ⓣ",
        "Ⓤ", "Ⓥ", "Ⓦ", "Ⓧ", "Ⓨ", "Ⓩ",
        "⒜", "⒝", "⒞", "⒟", "⒠", "⒡", "⒢", "⒣", "⒤", "⒥", 
        "⒦", "⒧", "⒨", "⒩", "⒪", "⒫", "⒬", "⒭", "⒮", "⒯", 
        "⒰", "⒱", "⒲", "⒳", "⒴", "⒵",
        "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹",
        "₀", "₁", "₂", "₃", "₄", "₅", "₆", "₇", "₈", "₉",
        "½", "⅓", "⅔", "¼", "¾", "⅕", "⅖", "⅗", "⅘", "⅙", 
        "⅚", "⅛", "⅜", "⅝", "⅞",
        "™", "©", "®", "℅", "℡", "№",
        "㎎", "㎏", "㎜", "㎝", "㎞", "㎡", "㏄", "㏎", "㏑", "㏒",
        "☂", "☠", "☢", "☣", "☯", "✿", "❀", "⚡", "⚠", "♔", "♕",
        "♠", "♣", "♥", "♦", "★", "☆", "⌖", "⚔", "⚕", "∞", "×",
        "ㅤ", "⠀", "ﾠ", " ", " ",
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",  
        "a", "b", "c", "d", "e", "f", "g", "h", "i", "j","k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v","w", "x", "y", "z",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J","K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V","W", "X", "Y", "Z"
    ]
}

AVAILABLE_BIOS = [
    {
        "name": "Default Law",
        "content": "[B][C][0000FF] ╭─╮\n— ꚠ —  [FFFF99]┆ @ OUT_OF_LAW\n[0000FF] ╰─╯"
    },
    {
        "name": "Shawon",
        "content": "[B][C][0000FF] ╭─╮\n— ꚠ —  [FFFF99]┆   @showon5592\n[0000FF] ╰─╯"
    },
    {
        "name": "King Ador",
        "content": "[B][C][FF0000]SPAM KING ADOR→\n[00FF00]ALL BOT[00BFFF] AVAILABLE লাগলে [00FFFF]INBOX MY\n[FFFF00] TIKTOK : [FF00FF]→@rio_sir2"
    },
    {
        "name": "alvi",
        "content": "[B][C][FFFF00]Fᴜᴄᴋ Yᴏᴜʀ Aᴛᴛɪᴛᴜᴅᴇ\n\n[C0C0C0]Tɪᴋ Tᴏᴋ  Aʟᴠɪ Sɪʀ"
    },
    {
        "name": "Red Skull VIP",
        "content": "[b][c][ff0000] ☠ DANGEROUS ☠\n[000000] ⚡ NO MERCY ⚡"
    },
    {
        "name": "Sabbir",
        "content": "[B][C][0000FF] ╭─╮\n— ꚠ —  [FFFF99]┆ @ mdsabbirvai659\n[0000FF] ╰─╯"
    },
    {
        "name": "White Angel",
        "content": "[b][c][ffffff] 🕊️ INNOCENT 🕊️\n[00ffff] ⭐ PEACE MAKER ⭐"
    },
    {
        "name": "Alex",
        "content": "[B][C][C0C0C0]নাম টাই যথেষ্ট,,\n[FF99FF]বাকিটা তোর ভাবিরে জিগা,,\n[FF00FF]Alex কেডা..."
    },
    {
        "name": "garena",
        "content": "[B][C]\n[C0C0C0]Garena গুষ্টি চুদি"
    },
    {
        "name": "AX_ROMJAN",
        "content": "[B][C][0000FF] ╭─╮\nYOUTUBE  [FFFF99]┆ AX_ROMJAN_YT\n[0000FF] ╰─╯"
    },
    {
        "name": "none",
        "content": "[B][C][0000FF].................. "
    },
    {
        "name": "Venom",
        "content": "[B][C]FREE F[ff8800]I[ffffff]RE [FFFF00] GUILD BOT→[FF1493] GLORY BOT [FF00FF]PERSONAL SPAM SERVER[00FF00]→LIKE [FF4500]→LONG BIO[00FFFF] লাগলে INBOX→[00BFFF]LOW [FF1493]PRICE : [FFFF00]TIKTOK : [00FFFF]@venombd2.0 → [00FF00]W'P : → [ffffff]01986995772"
    },
    {
        "name": "Default Law 2",
        "content": "[B][C][0000FF] ╭─────────────╮\n[FFFF99] 10 YEARS OLD\n[0000FF] ╰─────────────╯"
    },
    {
        "name": "Sensat!on ",
        "content": "[B][C][0000FF] your destination says you're a sensation player"
    }
]

HEX_KEY = "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"
KEY = bytes.fromhex(HEX_KEY)
LANG = "en"

REGISTER_URL = "https://100067.connect.garena.com/api/v2/oauth/guest:register"
TOKEN_URL = "https://100067.connect.garena.com/api/v2/oauth/guest/token:grant"
MAJOR_REGISTER_URL = "https://loginbp.ggpolarbear.com/MajorRegister"
MAJOR_LOGIN_URL = "https://loginbp.ggpolarbear.com/MajorLogin"
UPDATE_BIO_URL = "https://clientbp.ggpolarbear.com/UpdateSocialBasicInfo"

_sym_db = _symbol_database.Default()
_globals = globals()

# ==================== INLINE PROTOBUF DEFINITIONS ====================

DESC_DATA = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ndata.proto\"\xbb\x01\n\x04\x44\x61ta\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x1e\n\x07\x66ield_5\x18\x05 \x01(\x0b\x32\r.EmptyMessage\x12\x1e\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\r.EmptyMessage\x12\x0f\n\x07\x66ield_8\x18\x08 \x01(\t\x12\x0f\n\x07\x66ield_9\x18\t \x01(\x05\x12\x1f\n\x08\x66ield_11\x18\x0b \x01(\x0b\x32\r.EmptyMessage\x12\x1f\n\x08\x66ield_12\x18\x0c \x01(\x0b\x32\r.EmptyMessage\"\x0e\n\x0c\x45mptyMessageb\x06proto3'
)
_builder.BuildMessageAndEnumDescriptors(DESC_DATA, _globals)
_builder.BuildTopDescriptorsAndMessages(DESC_DATA, 'data_pb2', _globals)

DESC_MAJOR_LOGIN_REQ = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3'
)
_builder.BuildMessageAndEnumDescriptors(DESC_MAJOR_LOGIN_REQ, _globals)
_builder.BuildTopDescriptorsAndMessages(DESC_MAJOR_LOGIN_REQ, 'MajorLoginReq_pb2', _globals)

DESC_MAJOR_LOGIN_RES = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x13MajorLoginRes.proto\"|\n\rMajorLoginRes\x12\x13\n\x0b\x61\x63\x63ount_uid\x18\x01 \x01(\x04\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0b\n\x03key\x18\x16 \x01(\x0c\x12\n\n\x02iv\x18\x17 \x01(\x0c\x62\x06proto3'
)
_builder.BuildMessageAndEnumDescriptors(DESC_MAJOR_LOGIN_RES, _globals)
_builder.BuildTopDescriptorsAndMessages(DESC_MAJOR_LOGIN_RES, 'MajorLoginRes_pb2', _globals)

DESC_GET_LOGIN_DATA_RES = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x15GetLoginDataRes.proto\"\xa4\x01\n\x0cGetLoginData\x12\x12\n\nAccountUID\x18\x01 \x01(\x04\x12\x0e\n\x06Region\x18\x03 \x01(\t\x12\x13\n\x0b\x41\x63\x63ountName\x18\x04 \x01(\t\x12\x16\n\x0eOnline_IP_Port\x18\x0e \x01(\t\x12\x0f\n\x07\x43lan_ID\x18\x14 \x01(\x03\x12\x16\n\x0e\x41\x63\x63ountIP_Port\x18  \x01(\t\x12\x1a\n\x12\x43lan_Compiled_Data\x18\x37 \x01(\tb\x06proto3'
)
_builder.BuildMessageAndEnumDescriptors(DESC_GET_LOGIN_DATA_RES, _globals)
_builder.BuildTopDescriptorsAndMessages(DESC_GET_LOGIN_DATA_RES, 'GetLoginDataRes_pb2', _globals)

Data = _sym_db.GetSymbol('Data')
EmptyMessage = _sym_db.GetSymbol('EmptyMessage')
MajorLogin = _sym_db.GetSymbol('MajorLogin')
MajorLoginRes = _sym_db.GetSymbol('MajorLoginRes')
GetLoginData = _sym_db.GetSymbol('GetLoginData')

# =====================================================================

console = Console()

exec(bytes.fromhex('6465662067656e65726174655f637573746f6d5f70617373776f726428293a0a2020202062617365203d20224f55545f4f465f4c41575f220a202020207375666669785f6c656e203d206d617828302c203634202d206c656e286261736529290a20202020737566666978203d2027272e6a6f696e2872616e646f6d2e63686f696365282730313233343536373839414243444546272920666f72205f20696e2072616e6765287375666669785f6c656e29290a2020202072657475726e2062617365202b20737566666978').decode('utf-8'))

def generate_dynamic_name(base_name):
    req_len = max(0, 12 - len(base_name))
    if req_len == 0:
        return base_name[:12]
    extras = "".join(random.choices(CONFIG["EXTRA"], k=req_len))
    return base_name + extras

def E_AEs(pc):
    Z = bytes.fromhex(pc)
    key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(Z, AES.block_size))

async def EnC_Vr(N):
    if N < 0: return b''
    H = []
    while True:
        BesTo = N & 0x7F
        N >>= 7
        if N: BesTo |= 0x80
        H.append(BesTo)
        if not N: break
    return bytes(H)

async def CrEaTe_VarianT(field_number, value):
    return await EnC_Vr((field_number << 3) | 0) + await EnC_Vr(value)

async def CrEaTe_LenGTh(field_number, value):
    encoded_value = value.encode() if isinstance(value, str) else value
    return await EnC_Vr((field_number << 3) | 2) + await EnC_Vr(len(encoded_value)) + encoded_value

async def CrEaTe_ProTo(fields):
    packet = bytearray()
    for field, value in fields.items():
        if isinstance(value, dict):
            nested_packet = await CrEaTe_ProTo(value)
            packet.extend(await CrEaTe_LenGTh(field, nested_packet))
        elif isinstance(value, int):
            packet.extend(await CrEaTe_VarianT(field, value))
        elif isinstance(value, str) or isinstance(value, bytes):
            packet.extend(await CrEaTe_LenGTh(field, value))
    return packet

async def DecodE_HeX(num):
    h = hex(num)[2:]
    return "0" + h if len(h) == 1 else h

async def EnC_PacKeT(hex_str, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(bytes.fromhex(hex_str), AES.block_size)).hex()

async def xAuThSTarTuP(target_uid, token, timestamp, key, iv):
    uid_hex = hex(target_uid)[2:]
    encrypted_timestamp = await DecodE_HeX(timestamp)
    encrypted_packet = await EnC_PacKeT(token.encode().hex(), key, iv)
    encrypted_packet_length = hex(len(encrypted_packet) // 2)[2:]
    headers = '0000000'
    if len(uid_hex) == 8: headers = '00000000'
    elif len(uid_hex) == 10: headers = '000000'
    elif len(uid_hex) == 7: headers = '000000000'
    return f"0115{headers}{uid_hex}{encrypted_timestamp}00000{encrypted_packet_length}{encrypted_packet}"

# ==================== NETWORK REQUESTS WITH PROXY SUPPORT ====================

async def guest_register(session, dev, proxy=None):
    password = generate_custom_password()
    payload = {"app_id": 100067, "client_type": 2, "password": password, "source": 2}
    body_json = json.dumps(payload, separators=(',', ':'))
    signature = hmac.new(KEY, body_json.encode(), hashlib.sha256).hexdigest()
    headers = {
        "Authorization": f"Signature {signature}",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "Host": "100067.connect.garena.com"
    }
    async with session.post(REGISTER_URL, headers=headers, data=body_json, proxy=proxy) as resp:
        if resp.status != 200: raise Exception("Garena guest registration failed.")
        data = await resp.json()
        if data.get("code") != 0: raise Exception("Garena response indicated error.")
        return data['data']['uid'], password

async def guest_token(session, uid, password, dev, proxy=None):
    payload = {
        "client_id": 100067,
        "client_secret": HEX_KEY,
        "client_type": 2,
        "password": password,
        "response_type": "token",
        "uid": uid
    }
    body_json = json.dumps(payload, separators=(',', ':'))
    signature = hmac.new(KEY, body_json.encode(), hashlib.sha256).hexdigest()
    headers = {
        "Authorization": f"Signature {signature}",
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "Connection": "Keep-Alive",
        "Host": "100067.connect.garena.com"
    }
    async with session.post(TOKEN_URL, headers=headers, data=body_json, proxy=proxy) as resp:
        if resp.status != 200: raise Exception("Garena oauth token request failed.")
        data = await resp.json()
        if data.get("code") != 0: raise Exception("Garena token response error.")
        return data['data']['access_token'], data['data']['open_id']

async def major_register(session, access_token, open_id, name, dev, proxy=None):
    keystream = [0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37,
                 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30, 0x31, 0x37, 0x30, 0x30, 0x30, 0x30, 0x30, 0x32, 0x30]
    encoded_open_id = ""
    for i, ch in enumerate(open_id):
        encoded_open_id += chr(ord(ch) ^ keystream[i % len(keystream)])
    field14 = encoded_open_id.encode('latin1')
    payload_fields = {
        1: name, 2: access_token, 3: open_id, 5: 102000007,
        6: 4, 7: 1, 13: 1, 14: field14, 15: LANG, 16: 1, 17: 1
    }
    proto_bytes = await CrEaTe_ProTo(payload_fields)
    encrypted_payload = E_AEs(bytes(proto_bytes).hex())
    headers = {
        "Accept-Encoding": "gzip", "Authorization": "Bearer", "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded", "Expect": "100-continue",
        "Host": "loginbp.ggpolarbear.com", "ReleaseVersion": "OB54",  
        "X-GA": "v1 1", "X-Unity-Version": "2018.4."
    }
    async with session.post(MAJOR_REGISTER_URL, headers=headers, data=encrypted_payload, proxy=proxy) as resp:
        if resp.status != 200: raise Exception("Polarbear major registration failed.")
        return True

async def EncRypTMajoRLoGin(open_id, access_token, dev):
    major_login = MajorLogin()
    major_login.event_time = str(datetime.now())[:-7]
    major_login.game_name = "free fire"
    major_login.platform_id = 2
    major_login.client_version = "1.126.1"  
    major_login.system_software = f"{dev['os']} ({dev['os_ver_only']})"
    major_login.system_hardware = "Handheld"
    major_login.telecom_operator = dev["operator"]
    major_login.network_type = "WIFI"
    major_login.screen_width = dev["width"]
    major_login.screen_height = dev["height"]
    major_login.screen_dpi = dev["dpi"]
    major_login.processor_details = dev["cpu_long"]
    major_login.memory = dev["ram"]
    major_login.gpu_renderer = dev["gpu"]
    major_login.gpu_version = dev["opengl"]
    major_login.unique_device_id = f"Google|{random.randint(10000000, 99999999)}-a7d5-4cb6-8d7e-3b0e448a0c57"
    major_login.client_ip = "223.191.51.89"  # BD IP range
    major_login.language = "en"
    major_login.open_id = open_id
    major_login.open_id_type = "4"
    major_login.device_type = "Handheld"
    major_login.memory_available.version = 55
    major_login.memory_available.hidden_value = 81
    major_login.access_token = access_token
    major_login.platform_sdk_id = 2
    major_login.network_operator_a = dev["operator"]
    major_login.network_type_a = "WIFI"
    major_login.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major_login.external_storage_total = 36235
    major_login.external_storage_available = 31335
    major_login.internal_storage_total = 2519
    major_login.internal_storage_available = 703
    major_login.game_disk_storage_available = 25010
    major_login.game_disk_storage_total = 26628
    major_login.external_sdcard_avail_storage = 32992
    major_login.external_sdcard_total_storage = 36235
    major_login.login_by = 3
    major_login.library_path = "/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/lib/arm64"
    major_login.reg_avatar = 1
    major_login.library_token = "5b892aaabd688e571f688053118a162b|/data/app/com.dts.freefireth-YPKM8jHEwAJlhpmhDhv5MQ==/base.apk"
    major_login.channel_type = 3
    major_login.cpu_type = 2
    major_login.cpu_architecture = "64"
    major_login.client_version_code = "2019120776"  
    major_login.graphics_api = "OpenGLES2"
    major_login.supported_astc_bitset = 16383
    major_login.login_open_id_type = 4
    major_login.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major_login.loading_time = 13564
    major_login.release_channel = "android"
    major_login.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major_login.android_engine_init_flag = 110009
    major_login.if_push = 2
    major_login.is_vpn = 1
    major_login.origin_platform_type = "4"
    major_login.primary_platform_type = "4"
    serialized = major_login.SerializeToString()
    key = b'Yg&tc%DEuh6%Zc^8'
    iv = b'6oyZDr22E3ychjM%'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(serialized, AES.block_size))

async def major_login_async(session, access_token, open_id, dev, proxy=None):
    encrypted_payload = await EncRypTMajoRLoGin(open_id, access_token, dev)
    headers = {
        "Accept-Encoding": "gzip", "Authorization": "Bearer", "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded", "Expect": "100-continue",
        "Host": "loginbp.ggpolarbear.com", "ReleaseVersion": "OB54",  
        "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"
    }
    async with session.post(MAJOR_LOGIN_URL, headers=headers, data=encrypted_payload, proxy=proxy) as resp:
        if resp.status != 200: raise Exception("Polarbear MajorLogin request failed.")
        content = await resp.read()
        res = MajorLoginRes()
        res.ParseFromString(content)
        return res

async def get_login_data(session, base_url, payload, jwt_token, dev, proxy=None):
    url = f"{base_url}/GetLoginData"
    headers = {
        "Accept-Encoding": "gzip", "Authorization": f"Bearer {jwt_token}",
        "Connection": "Keep-Alive", "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue", "Host": base_url.replace("https://", ""),
        "ReleaseVersion": "OB54",  
        "X-GA": "v1 1", "X-Unity-Version": "2018.4.11f1"
    }
    async with session.post(url, headers=headers, data=payload, proxy=proxy) as resp:
        if resp.status != 200: raise Exception("Polarbear GetLoginData request failed.")
        content = await resp.read()
        data = GetLoginData()
        data.ParseFromString(content)
        return data

async def update_bio_async(session, jwt_token, bio_text, dev, proxy=None):
    key = bytes([89,103,38,116,99,37,68,69,117,104,54,37,90,99,94,56])
    iv = bytes([54,111,121,90,68,114,50,50,69,51,121,99,104,106,77,37])
    proto = Data()
    proto.field_2 = 17
    proto.field_5.CopyFrom(EmptyMessage())
    proto.field_6.CopyFrom(EmptyMessage())
    proto.field_8 = bio_text
    proto.field_9 = 1
    proto.field_11.CopyFrom(EmptyMessage())
    proto.field_12.CopyFrom(EmptyMessage())
    raw = proto.SerializeToString()
    padded = pad(raw, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(padded)
    headers = {
        "Expect": "100-continue", "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1", "X-GA": "v1 1", "ReleaseVersion": "OB54",  
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive", "Accept-Encoding": "gzip"
    }
    try:
        async with session.post(UPDATE_BIO_URL, headers=headers, data=encrypted, timeout=10, proxy=proxy) as resp:
            return resp.status == 200
    except:
        return False

async def equip_emote_async(session, jwt_token, dev, proxy=None):
    url = "https://clientbp.ggpolarbear.com/ChooseEmote"
    emote_data = bytes.fromhex("CAF683222A25C7BEFEB51F59544DB313")
    headers = {
        "Expect": "100-continue", 
        "Authorization": f"Bearer {jwt_token}",
        "X-Unity-Version": "2018.4.11f1", 
        "X-GA": "v1 1", 
        "ReleaseVersion": "OB54",  
        "Content-Type": "application/x-www-form-urlencoded",
        "Connection": "Keep-Alive", 
        "Accept-Encoding": "gzip"
    }
    try:
        async with session.post(url, headers=headers, data=emote_data, timeout=10, proxy=proxy) as resp:
            return resp.status == 200
    except:
        return False

async def tcp_connection(ip, port, auth_token_hex):
    try:
        reader, writer = await asyncio.open_connection(ip, int(port), ssl=False)
        auth_bytes = bytes.fromhex(auth_token_hex)
        writer.write(auth_bytes)
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        return True
    except:
        return False

# ==================== CORE GENERATION FUNCTION ====================

async def create_single_account(session, selected_format, base_name, selected_bio, proxy=None):
    device = random.choice(DEVICE_PROFILES)
    
    uid, password = await guest_register(session, device, proxy=proxy)
    access_token, open_id = await guest_token(session, uid, password, device, proxy=proxy)
    full_name = generate_dynamic_name(base_name)
    await major_register(session, access_token, open_id, full_name, device, proxy=proxy)
    major_res = await major_login_async(session, access_token, open_id, device, proxy=proxy)
    jwt_token = major_res.token
    account_id = major_res.account_uid
    payload = await EncRypTMajoRLoGin(open_id, access_token, device)
    login_data = await get_login_data(session, major_res.url, payload, jwt_token, device, proxy=proxy)
    
    await asyncio.gather(
        update_bio_async(session, jwt_token, selected_bio, device, proxy=proxy),
        equip_emote_async(session, jwt_token, device, proxy=proxy)
    )
    
    auth_token_hex = await xAuThSTarTuP(int(account_id), jwt_token, int(major_res.timestamp), major_res.key, major_res.iv)
    online_ip, online_port = login_data.Online_IP_Port.split(":")
    chat_ip, chat_port = login_data.AccountIP_Port.split(":")
    
    await asyncio.gather(
        tcp_connection(online_ip, online_port, auth_token_hex),
        tcp_connection(chat_ip, chat_port, auth_token_hex)
    )
    
    # Formatted Data return based on selection
    account_data = {}
    if selected_format == "bot":
        account_data = {"uid": str(uid), "password": password}
    elif selected_format == "vv":
        account_data = {str(uid): password}
    else:  # api
        account_data = f"uid={uid}&password={password}"

    return {
        "status": "success",
        "account_id": str(account_id),
        "name": full_name,
        "region": login_data.Region,
        "data": account_data
    }

# ==================== WEB API HANDLERS ====================

async def handle_create_account(request):
    try:
        # Query parameters reading
        params = request.query
        selected_format = params.get("format", "api").lower()
        if selected_format not in ["bot", "vv", "api"]:
            selected_format = "api"
            
        badge_choice = params.get("badge", "new_×")
        if badge_choice in CONFIG["BADGES"]:
            active_badge_list = CONFIG["BADGES"][badge_choice]
        else:
            active_badge_list = [badge_choice]
            
        base_name = random.choice(active_badge_list)
        
        # Bio selection
        bio_choice = params.get("bio", "1")
        selected_bio = AVAILABLE_BIOS[0]['content']
        if bio_choice.isdigit():
            idx = int(bio_choice) - 1
            if 0 <= idx < len(AVAILABLE_BIOS):
                selected_bio = AVAILABLE_BIOS[idx]['content']
        else:
            for b in AVAILABLE_BIOS:
                if b['name'].lower() == bio_choice.lower():
                    selected_bio = b['content']
                    break

        # Bangladesh Proxy Settings
        # Environment Variable এ BD_PROXY সেট করা থাকলে সেটি প্রাধিকার পাবে।
        # কুয়েরি প্যারামিটারেও '?proxy=http://...' আকারে পাঠানো যাবে।
        proxy = os.environ.get("BD_PROXY") or params.get("proxy")
        if not proxy:
            # প্রক্সি ডিফাইন করা না থাকলে সতর্কবার্তা দেওয়া হবে কিন্তু এক্সিকিউশন সচল থাকবে
            print("\033[1;33m[!] Warning: No BD Proxy provided. Account region might default to VPS host region.\033[0m")
        else:
            print(f"\033[1;32m[*] Routing request through BD Proxy: {proxy}\033[0m")

        connector = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=connector) as session:
            result = await create_single_account(session, selected_format, base_name, selected_bio, proxy=proxy)
            return web.json_response(result)
            
    except Exception as e:
        traceback.print_exc()
        return web.json_response({
            "status": "error",
            "message": str(e)
        }, status=500)

async def handle_health_check(request):
    return web.json_response({"status": "running", "engine": TITLE})

# ==================== MAIN WEB SERVER START ====================

def main():
    app = web.Application()
    # মূল হেলথ চেক রাউট
    app.router.add_get('/', handle_health_check)
    
    # স্ল্যাশসহ বা স্ল্যাশ ছাড়া উভয় রাউটই হ্যান্ডেল করার জন্য
    app.router.add_get('/create', handle_create_account)
    app.router.add_get('/create/', handle_create_account)
    app.router.add_post('/create', handle_create_account)
    app.router.add_post('/create/', handle_create_account)

    port = int(os.environ.get("PORT", 10000))
    print(f"\033[1;32m[*] Starting Server on port {port}...\033[0m")
    web.run_app(app, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
