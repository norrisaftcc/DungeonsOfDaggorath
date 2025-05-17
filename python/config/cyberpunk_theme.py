"""Cyberpunk theme configuration and mapping."""

from typing import Dict, Any
from ..domain import CreatureType, ItemTemplate, ItemType

class CyberpunkTheme:
    """Maps classic Daggorath elements to cyberpunk equivalents."""
    
    # Visual theme
    COLORS = {
        'background': '#000000',
        'text': '#00FF00',
        'highlight': '#00FFFF',
        'danger': '#FF0000',
        'warning': '#FFFF00',
        'ice': '#0080FF'
    }
    
    # Entity name mappings
    CREATURE_MAPPING = {
        'SPIDER': 'Security_Probe',
        'VIPER': 'Data_Snake',
        'SCORPION': 'Crypto_Scorpion', 
        'KNIGHT': 'WhiteICE',
        'BLOB': 'Memory_Leak',
        'WRAITH': 'Ghost_Protocol',
        'WIZARD': 'SysAdmin_Root'
    }
    
    ITEM_MAPPING = {
        'TORCH': 'Scanner.exe',
        'SWORD': 'IceBreaker.exe',
        'SHIELD': 'Firewall.sys',
        'DAGGER': 'Script_Kiddie.bat',
        'MACE': 'LogicBomb.app',
        'RING': 'AccessToken.key',
        'SCROLL': 'Exploit.txt',
        'FLASK': 'Defrag.bat',
        'ELIXIR': 'SystemRestore.iso'
    }
    
    # Action translations
    ACTION_MAPPING = {
        'MOVE': 'NAVIGATE',
        'TURN': 'ROTATE',
        'ATTACK': 'EXECUTE',
        'GET': 'DOWNLOAD',
        'DROP': 'DELETE',
        'USE': 'RUN',
        'PULL': 'LOAD',
        'STOW': 'ARCHIVE',
        'EXAMINE': 'SCAN'
    }
    
    # Status translations  
    STATUS_MAPPING = {
        'Health': 'System Integrity',
        'Heart Rate': 'Connection Ping',
        'Fainting': 'Connection Lost',
        'Dead': 'Blue Screen',
        'Vision': 'Scan Radius',
        'Weight': 'Memory Usage'
    }
    
    # UI text replacements
    UI_TEXT = {
        'DUNGEONS OF DAGGORATH': 'CYBERSPACE INFILTRATOR',
        'PREPARE YE': 'JACK IN',
        'DARE YE': 'HACK THE',
        'LEVEL': 'SECURITY LAYER',
        'TORCH': 'SCANNER',
        'LIT': 'ACTIVE',
        'DIED': 'DISCONNECTED'
    }
    
    @staticmethod
    def create_ice_types() -> Dict[str, CreatureType]:
        """Create cyberpunk ICE (enemy) types."""
        return {
            'PROBE': CreatureType(
                name="Security_Probe",
                base_health=10,
                damage=5, 
                defense=2,
                speed=3,
                description="Basic scanning daemon",
                sound="digital_beep.wav"
            ),
            'WHITE_ICE': CreatureType(
                name="WhiteICE_2.0",
                base_health=20,
                damage=10,
                defense=8,
                speed=4,
                description="Defensive barrier program",
                sound="static_burst.wav"
            ),
            'BLACK_ICE': CreatureType(
                name="BlackICE_Lethal",
                base_health=40,
                damage=20,
                defense=10,
                speed=6,
                description="Military-grade attack program",
                sound="electronic_scream.wav"
            ),
            'GHOST': CreatureType(
                name="Ghost_Protocol",
                base_health=30,
                damage=18,
                defense=3,
                speed=10,
                description="Stealth hunter AI",
                sound="phase_shift.wav"  
            ),
            'ADMIN': CreatureType(
                name="SysAdmin_Root",
                base_health=100,
                damage=30,
                defense=20,
                speed=5,
                description="The corporate AI overlord",
                sound="system_critical.wav"
            )
        }
    
    @staticmethod
    def create_program_types() -> Dict[str, ItemTemplate]:
        """Create cyberpunk program (item) types."""
        return {
            # Weapons (Attack Programs)
            'ICEBREAKER': ItemTemplate(
                name="IceBreaker.exe",
                item_type=ItemType.WEAPON,
                value=50,
                weight=5,
                description="Basic intrusion program",
                properties={"damage": 10, "code": "SW"}
            ),
            'LOGIC_BOMB': ItemTemplate(
                name="LogicBomb.app",
                item_type=ItemType.WEAPON,
                value=100,
                weight=8,
                description="Explosive code injection",
                properties={"damage": 15, "code": "SW"}
            ),
            'VIRUS_SPIKE': ItemTemplate(
                name="VirusSpike.bin",
                item_type=ItemType.WEAPON,
                value=200,
                weight=12,
                description="Malicious payload delivery",
                properties={"damage": 25, "code": "SW"}
            ),
            
            # Defense (Security Programs)
            'FIREWALL': ItemTemplate(
                name="Firewall.sys",
                item_type=ItemType.ARMOR,
                value=40,
                weight=3,
                description="Standard protection suite",
                properties={"defense": 5, "code": "SH"}
            ),
            'PROXY_SHIELD': ItemTemplate(
                name="ProxyShield.dll",
                item_type=ItemType.ARMOR,
                value=80,
                weight=5,
                description="Redirects attacks through proxies",
                properties={"defense": 8, "code": "SH"}
            ),
            
            # Utilities (Consumables)
            'SCANNER': ItemTemplate(
                name="Scanner.exe",
                item_type=ItemType.TORCH,
                value=5,
                weight=1,
                description="Reveals network topology",
                properties={"duration": 500, "code": "TO"}
            ),
            'DEFRAG': ItemTemplate(
                name="Defrag.bat",
                item_type=ItemType.CONSUMABLE,
                value=15,
                weight=1,
                description="Repairs system integrity",
                properties={"heal": 50, "code": "FL"}
            ),
            'BANDWIDTH': ItemTemplate(
                name="Bandwidth.cfg",
                item_type=ItemType.CONSUMABLE,
                value=25,
                weight=1,
                description="Boosts connection speed",
                properties={"speed": 10, "duration": 100, "code": "FL"}
            ),
            
            # Quest Items
            'ACCESS_KEY': ItemTemplate(
                name="RootAccess.key",
                item_type=ItemType.QUEST,
                value=1000,
                weight=0,
                description="Grants admin privileges",
                properties={"code": "RG", "opens": "mainframe"}
            ),
            'DATA_CORE': ItemTemplate(
                name="DataCore.zip",
                item_type=ItemType.TREASURE,
                value=1000,
                weight=5,
                description="Valuable corporate secrets",
                properties={"code": "RG", "score": 1000}
            )
        }
    
    @staticmethod
    def get_level_themes() -> Dict[int, Dict[str, Any]]:
        """Get visual themes for each security layer."""
        return {
            0: {
                'name': 'DMZ_Gateway',
                'color': '#00FF00',  # Green
                'wall': '#',
                'floor': '.',
                'style': 'terminal_classic'
            },
            1: {
                'name': 'Corporate_Firewall',
                'color': '#FFA500',  # Amber
                'wall': '█',
                'floor': '░',
                'style': 'security_warning'
            },
            2: {
                'name': 'Data_Vault',
                'color': '#FF0000',  # Red
                'wall': '▓',
                'floor': '▒',
                'style': 'danger_zone'
            },
            3: {
                'name': 'Core_Mainframe',
                'color': '#0080FF',  # Blue
                'wall': '╬',
                'floor': '═',
                'style': 'ice_fortress'
            }
        }
    
    @classmethod
    def apply_theme(cls, game_config: Dict[str, Any]) -> Dict[str, Any]:
        """Apply cyberpunk theme to game configuration."""
        # Deep copy config
        import copy
        cyber_config = copy.deepcopy(game_config)
        
        # Apply theme name
        cyber_config['theme'] = 'cyberpunk'
        cyber_config['name'] = 'Cyberspace Infiltrator'
        
        # Convert all text references
        cyber_config['ui_strings'] = cls.UI_TEXT
        cyber_config['action_names'] = cls.ACTION_MAPPING
        cyber_config['status_names'] = cls.STATUS_MAPPING
        
        # Apply visual style
        cyber_config['display'] = {
            'color_scheme': 'matrix_green',
            'font': 'terminal_mono',
            'effects': {
                'scanlines': True,
                'crt_curve': True,
                'glitch_on_damage': True
            }
        }
        
        return cyber_config