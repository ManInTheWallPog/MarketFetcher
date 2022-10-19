from turtle import pos
from ratelimit import limits, sleep_and_retry
import requests
import sys

WFM_API = "https://api.warframe.market/v1"
@sleep_and_retry
@limits(calls=1, period=1)
def get_name():
   Name = str(input("Introduce your Name: "))
   return Name

def get_request(url):
    """Executes a wfm query"""
    request = requests.get(WFM_API + url, stream=True)
    if request.status_code == 200:
        return request.json()["payload"]
    return None

def get_auctions():
    """Returns the current auctions of the user."""
    result = get_request("/profile/" +get_name() +"/auctions")
    return result["auctions"]

def save_rivens():
    with open('Rivens.txt', 'w') as out:
        for auction in get_auctions():
           weaponName = auction["item"]["weapon_url_name"].capitalize().replace("_", " ")
           rivenName = auction["item"]["name"].capitalize().replace("_", " ")
           rivenPrice = str(auction["starting_price"])
           attributes = ""
           poscount = 0

           for attr in auction["item"]["attributes"]:    
               posi = attr["positive"]
               if posi == True:
                    poscount = poscount +1
               elif posi == False and poscount == 2:
                   attributes = attributes + ",,"  
               new_attr = clean_values(attr["url_name"])
               attributes = attributes + "," + new_attr +"," +str(attr["value"])            

           print(weaponName + "," + rivenName + ",[" + weaponName + " " + rivenName + "],"  + rivenPrice + attributes , file=out)


def clean_values(attr):
    if attr == "base_damage_/_melee_damage":
        return "Damage"
    elif attr == "multishot":
        return "MS"
    elif attr == "fire_rate_/_attack_speed":
        return "FR"
    elif attr == "damage_vs_corpus":
        return "DTC"
    elif attr == "damage_vs_grineer":
        return "DTG"
    elif attr == "damage_vs_infested":
        return "DTI"
    elif attr == "impact_damage":
        return "Impact"
    elif attr == "puncture_damage":
        return "Puncture"
    elif attr == "slash_damage":
        return "Slash"
    elif attr == "cold_damage":
        return "Cold"
    elif attr == "toxin_damage":
        return "Tox"
    elif attr == "heat_damage":
        return "Heat"
    elif attr == "electric_damage":
        return "Elec"
    elif attr == "combo_duration":
        return "Combo"
    elif attr == "critical_chance":
        return "Critchance"
    elif attr == "critical_damage":
        return "Critdmg"
    elif attr == "critical_chance_on_slide_attack":
        return "Slide"
    elif attr == "finisher_damage":
        return "Finisher"
    elif attr == "projectile_speed":
        return "FlightSpeed"
    elif attr == "ammo_maximum":
        return "Ammo"
    elif attr == "magazine_capacity":
        return "Mag"
    elif attr == "punch_through":
        return "PT"
    elif attr == "reload_speed":
        return "Reload"
    elif attr == "range":
        return "Range"
    elif attr == "status_chance":
        return "SC"
    elif attr == "status_duration":
        return "SD"
    elif attr == "recoil":
        return "Rec"
    elif attr == "zoom":
        return "Zoom"
    elif attr == "channeling_damage":
        return "IC"
    elif attr == "channeling_efficiency":
        return "Heavy"
    elif attr == "chance_to_gain_combo_count":
        return "Combochance"
    return (attr)
