import logging
import asyncio
import aiohttp
import requests
import base64
import json
import yaml
from datetime import datetime, timedelta

from __init__ import __version__
from config import config
from lib.esi import ESIApi
from lib.utils import EVEUtils
from lib.token import EVEToken

log = logging.getLogger("library.notifications")

class NotifFormatter:
    def __init__(self, notification):
        self.notification = notification
        self.esiclient = ESIApi()

    async def _selfclean(self, vars):
        for attr in vars: self.__dict__.pop(attr,None)

    async def get_formatted(self):
        template = await self._get_template(self.notification["type"])
        values = await self._parse_values(self.notification["text"])
        log.info("NotifText: {}".format(template))
        log.info("NotifValues: {}".format(values))
        return template.format(**values)

    async def _get_template(self, type):
        types = {
            'AllWarDeclaredMsg': self.text_war_declared,
            'DeclareWar': self.text_declare_war,
            'AllWarInvalidatedMsg': self.text_war_invalidated,
            'AllyJoinedWarAggressorMsg': self.text_aggressor_ally_joined_war,
            'CorpWarDeclaredMsg': self.text_war_declared,
            'EntosisCaptureStarted': self.text_entosis_capture_started,
            'SovCommandNodeEventStarted':
                self.text_sov_structure_command_nodes_decloaked,
            'SovStructureDestroyed': self.text_sov_structure_destroyed,
            'SovStructureReinforced': self.text_sov_structure_reinforced,
            'StructureUnderAttack': self.text_citadel_attacked,
            'OwnershipTransferred': self.text_structure_transferred,
            'StructureOnline': self.text_citadel_onlined,
            'StructureDestroyed': self.text_citadel_destroyed,
            'StructureFuelAlert': self.text_citadel_low_fuel,
            'StructureAnchoring': self.text_citadel_anchored,
            'StructureUnanchoring': self.text_citadel_unanchoring,
            'StructureServicesOffline': self.text_citadel_out_of_fuel,
            'StructureLostShields': self.text_citadel_lost_shields,
            'StructureLostArmor': self.text_citadel_lost_armor,
            'TowerAlertMsg': self.text_pos_attack,
            'TowerResourceAlertMsg': self.text_pos_fuel_alert,
            'StationServiceEnabled': self.text_entosis_enabled_structure,
            'StationServiceDisabled': self.text_entosis_disabled_structure,
            'OrbitalReinforced': self.text_customs_office_reinforced,
            'OrbitalAttacked': self.text_customs_office_attacked,
            'SovAllClaimAquiredMsg': self.text_sov_claim_acquired,
            'SovStationEnteredFreeport': self.text_sov_structure_freeported,
            'AllAnchoringMsg': self.text_structure_anchoring_alert,
            'InfrastructureHubBillAboutToExpire':
                self.text_ihub_bill_about_to_expire,
            'SovAllClaimLostMsg': self.text_sov_claim_lost,
            'SovStructureSelfDestructRequested': self.text_sov_structure_started_self_destructing,
            'SovStructureSelfDestructFinished': self.text_sov_structure_self_destructed,
            'StationConquerMsg': self.text_station_conquered,
            'MoonminingExtractionStarted': self.text_moon_extraction_started,
            'MoonminingExtractionCancelled': self.text_moon_extraction_cancelled,
            'MoonminingExtractionFinished': self.text_moon_extraction_finished,
            'MoonminingLaserFired': self.text_moon_extraction_turned_into_belt,
            'MoonminingAutomaticFracture': self.text_moon_extraction_autofractured,
            'CorpAllBillMsg': self.text_corporation_bill,
            'BillPaidCorpAllMsg': self.text_corporation_bill_paid,
            'CharAppAcceptMsg': self.text_character_application_accepted,
            'CorpAppNewMsg': self.text_new_character_application_to_corp,
            'CharAppWithdrawMsg': self.text_character_application_withdrawn,
            'CharLeftCorpMsg': self.text_character_left_corporation,
            'CorpNewCEOMsg': self.text_new_corporation_ceo,
            'CorpVoteMsg': self.text_corporation_vote_initiated,
            'CorpVoteCEORevokedMsg': self.text_corporation_vote_for_ceo_revoked,
            'CorpTaxChangeMsg': self.text_corporation_tax_changed,
            'CorpDividendMsg': self.text_corporation_dividend_paid_out,
            'BountyClaimMsg': self.text_bounty_claimed,
            'KillReportVictim': self.text_kill_report_victim,
            'KillReportFinalBlow': self.text_kill_report_final_blow,
        }
        if type in types:
            return types[type]()
        else:
            return "Not text for this notification.\n Dump data: {}"

    async def _parse_values(self, data):
        try:
            data_types = {
                'againstID': self.get_corp_or_alliance,
                'aggressorID': self.get_character,
                'declaredByID': self.get_corp_or_alliance,
                'charID': self.get_character,
                'defenderID': self.get_corp_or_alliance,
                'entityID': self.get_corp_or_alliance,
                'allyID': self.get_corp_or_alliance,
                'corpID': self.get_corp_or_alliance,
                'startTime': EVEUtils.epoch_to_date,
                'solarSystemID': self.get_system,
                'structureTypeID': self.get_item,
                'cancelledBy': self.get_character,
                'startedBy': self.get_character,
                'moonID': self.get_moon,
                'planetID': self.get_planet,
                'victimShipTypeID': self.get_item,
                'structureID': self.get_structure,
                'oldOwnerID': self.get_character,
                'newOwnerID': self.get_character,
                'shieldValue': EVEUtils.conv_to_percentage,
                'shieldLevel': EVEUtils.conv_to_percentage,
                'armorValue': EVEUtils.conv_to_percentage,
                'hullValue': EVEUtils.conv_to_percentage,
                'solarSystemLinkData': self.get_system_from_link,
                'fromCorporationLinkData': self.get_corporation_from_link,
                'toCorporationLinkData': self.get_corporation_from_link,
                'characterLinkData': self.get_character_from_link,
                'structureShowInfoData': self.get_structure_type_from_link,
                'dueDate': EVEUtils.epoch_to_date,
                'reinforceExitTime': EVEUtils.epoch_to_date,
                'decloakTime': EVEUtils.epoch_to_date,
                'freeportexittime': EVEUtils.epoch_to_date,
                'destructTime': EVEUtils.epoch_to_date,
                'readyTime': EVEUtils.epoch_to_date,
                'autoTime': EVEUtils.epoch_to_date,
                'currentDate': EVEUtils.epoch_to_date,
            }
            time_types = {
                'timeLeft': EVEUtils.duration_to_date,
            }
            data = yaml.load(data)
            for key , value in data.items():
                if key in data_types:
                    data[key] = await data_types[key](value)
                if key in time_types:
                    data[key] = await data_types[key](
                        self.notification["timestamp"], value)
            return data
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_character(self, id):
        try:
            name = await self.esiclient.char_get_name(id)
            if name is None:
                return id
            else: 
                return name
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_corp_or_alliance(self, id):
        try:
            name = await self.esiclient.corp_get_name(id)
            if name is None:
                name = await self.esiclient.alliance_get_name(id)
            if name is None:
                return id
            else: 
                return name
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_item(self, id):
        try:
            data = await self.esiclient.type_get_details(id)
            if data["name"] is None:
                return id
            else: 
                return data["name"]
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_moon(self, id):
        try:
            data = await self.esiclient.moon_get_details(id)
            if data["name"] is None:
                return id
            else: 
                return data["name"]
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_planet(self, id):
        try:
            data = await self.esiclient.planet_get_details(id)
            if data["name"] is None:
                return id
            else: 
                return data["name"]
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_structure(self, id):
        try:
            token_api = EVEToken()
            token = await token_api.get_token(
                "notifications_token",
                "esi-characters.read_notifications.v1")["access_token"]
            data = await self.esiclient.structure_get_details(id, token)
            if data["name"] is None:
                return id
            else:
                return data["name"]
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_system(self, id):
        try:
            data = await self.esiclient.system_get_details(id)
            if data["name"] is None:
                return id
            else: 
                return data["name"]
        except Exception:
            log.exception("An exception has occurred in {}: ".format(__name__))

    async def get_corporation_from_link(self, show_info):
        return await self.get_corp_or_alliance(show_info[-1])

    async def get_structure_type_from_link(self, show_info):
        return await self.get_item(show_info[1])

    async def get_system_from_link(self, show_info):
        return await self.get_system(show_info[-1])

    async def get_character_from_link(self, show_info):
        return await self.get_character(show_info[-1])

    def text_war_declared(self):
        return 'War has been declared to **{againstID}** by **{declaredByID}**'

    def text_declare_war(self):
        return '**{charID}** from **{entityID}** has declared war to **{defenderID}**'

    def text_war_invalidated(self):
        return 'War has been invalidated to **{againstID}** by **{declaredByID}**'

    def text_aggressor_ally_joined_war(self):
        return 'Ally **{allyID}** joined the war to help **{defenderID}** starting **{startTime}**'

    def text_sov_claim_lost(self):
        return 'SOV lost in **{solarSystemID}** by **{corpID}**'

    def text_sov_claim_acquired(self):
        return 'SOV acquired in **{solarSystemID}** by **{corpID}**'

    def text_pos_anchoring_alert(self):
        return 'New POS anchored in **"{moonID}"** by **{corpID}**'

    def text_pos_attack(self):
        return '**{moonID}** POS **"{typeID}"** (**{shieldValue}** shield, **{armorValue}** armor, **{hullValue}** hull) under attack by **{aggressorID}**'

    def text_pos_fuel_alert(self):
        return '{moonID} POS **"{typeID}"** is low on fuel: **{wants}**'

    def text_station_conquered(self):
        return "Station conquered from **{oldOwnerID}** by **{newOwnerID}** in **{solarSystemID}**"

    def text_customs_office_attacked(self):
        return '**"{planetID}"** POCO (**{shieldLevel}** shields) has been attacked by **{aggressorID}**'

    def text_customs_office_reinforced(self):
        return '**"{planetID}"** POCO has been reinforced by **{aggressorID}** (comes out of reinforce on **"{reinforceExitTime}"**)'

    def text_structure_transferred(self):
        return '**"{structureName}"** structure in **{solarSystemLinkData}** has been transferred from **{fromCorporationLinkData}** to **{toCorporationLinkData}** by **{characterLinkData}**'

    def text_entosis_capture_started(self):
        return 'Capturing of **"{structureTypeID}"** in **{solarSystemID}** has started'

    def text_entosis_enabled_structure(self):
        return 'Structure **"{structureTypeID}"** in **{solarSystemID}** has been enabled'

    def text_entosis_disabled_structure(self):
        return 'Structure **"{structureTypeID}"** in **{solarSystemID}** has been disabled'

    def text_sov_structure_reinforced(self):
        return 'SOV structure **"{campaignEventType}"** in **{solarSystemID}** has been reinforced, nodes will decloak **"{decloakTime}"**'

    def text_sov_structure_command_nodes_decloaked(self):
        return 'Command nodes for **"{campaignEventType}"** SOV structure in **{solarSystemID}** have decloaked'

    def text_sov_structure_destroyed(self):
        return 'SOV structure **"{structureTypeID}"** in **{solarSystemID}** has been destroyed'

    def text_sov_structure_freeported(self):
        return 'SOV structure **"{structureTypeID}"** in **{solarSystemID}** has been freeported, exits freeport on **"{freeportexittime}"**'

    def text_citadel_low_fuel(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) low fuel alert in **{solarsystemID}**'

    def text_citadel_anchored(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) anchored in **{solarsystemID}** by **{ownerCorpLinkData}**'

    def text_citadel_unanchoring(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) unanchoring in **{solarsystemID}** by **{ownerCorpLinkData}**'

    def text_citadel_attacked(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) attacked (**{shieldPercentage}** shield, **{armorPercentage}** armor, **{hullPercentage}** hull) in **{solarsystemID}** by **{charID}**'

    def text_citadel_onlined(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) onlined in **{solarsystemID}**'

    def text_citadel_lost_shields(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) lost shields in **{solarsystemID}** (comes out of reinforce on **"{0:eve_duration_to_date(notification_timestamp, timeLeft)}"**)'

    def text_citadel_lost_armor(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) lost armor in **{solarsystemID}** (comes out of reinforce on **"{0:eve_duration_to_date(notification_timestamp, timeLeft)}"**)'

    def text_citadel_destroyed(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) destroyed in **{solarsystemID}** owned by **{ownerCorpLinkData}**'

    def text_citadel_out_of_fuel(self):
        return 'Citadel (**{structureShowInfoData}**, **"{structureID}"**) ran out of fuel in **{solarsystemID}** with services **"{listOfServiceModuleIDs}"**'

    def text_structure_anchoring_alert(self):
        return 'New structure (**{typeID}**) anchored in **"{moonID}"** by **{corpID}**'

    def text_ihub_bill_about_to_expire(self):
        return 'IHUB bill to **{corpID}** for system **{solarSystemID}** will expire **{dueDate}**'

    def text_sov_structure_self_destructed(self):
        return 'SOV structure **"{structureTypeID}"** has self destructed in **{solarSystemID}**'

    def text_sov_structure_started_self_destructing(self):
        return 'Self-destruction of **"{structureTypeID}"** SOV structure in **{solarSystemID}** has been requested by **{charID}**. Structure will self-destruct on **"{destructTime}"**'

    def text_moon_extraction_started(self):
        return 'Moon extraction started by **{startedBy}** in **{solarSystemID}** (**{moonID}**, **"{structureName}"**) and will be ready on **{readyTime}** (or will auto-explode into a belt on **{autoTime}**)'

    def text_moon_extraction_cancelled(self):
        return 'Moon extraction cancelled by **{cancelledBy}** in **{solarSystemID}** (**{moonID}**, **"{structureName}"**)'

    def text_moon_extraction_finished(self):
        return 'Moon extraction has finished and is ready in **{solarSystemID}** (**{moonID}**, **"{structureName}"**) to be exploded into a belt (or will auto-explode into one on **{autoTime}**)'

    def text_moon_extraction_turned_into_belt(self):
        return 'Moon laser has been fired by **{firedBy}** in **{solarSystemID}** (**{moonID}**, **"{structureName}"**) and the belt is ready to be mined'

    def text_moon_extraction_autofractured(self):
        return 'Moon extraction in **{solarSystemID}** (**{moonID}**, **"{structureName}"**) has autofractured into a belt and is ready to be mined'

    def text_corporation_bill(self):
        return 'Corporation bill issued to **{debtorID}** by **{creditorID}** for the amount of **{amount}** at **{currentDate}**. Bill is due **{dueDate}**'

    def text_corporation_bill_paid(self):
        return 'Corporation bill for **{amount}** was paid. Bill was due **{dueDate}**'

    def text_new_character_application_to_corp(self):
        return 'Character **{charID}** has applied to corporation **{corpID}**. Application text:\n\n**{applicationText}**'

    def text_character_application_withdrawn(self):
        return 'Character **{charID}** application to corporation **{corpID}** has been withdrawn'

    def text_character_application_accepted(self):
        return 'Character **{charID}** accepted to corporation **{corpID}**'

    def text_character_left_corporation(self):
        return 'Character **{charID}** left corporation **{corpID}**'

    def text_new_corporation_ceo(self):
        return '**{newCeoID}** has replaced **{oldCeoID}** as the new CEO of **{corpID}**'

    def text_corporation_vote_initiated(self):
        return 'New corporation vote for **"{subject}"**:\n\n**{body}**'

    def text_corporation_vote_for_ceo_revoked(self):
        return 'Corporation **"{corpID}"** vote for new CEO has been revoked by **{charID}**'

    def text_corporation_tax_changed(self):
        return 'Tax changed from **{oldTaxRate}** to **{newTaxRate}** for **{corpID}**'

    def text_corporation_dividend_paid_out(self):
        return 'Corporation **{corpID}** has paid out **{payout}** ISK in dividends'

    def text_bounty_claimed(self):
        return 'A bounty of **{amount}** has been claimed for killing **{charID}**'

    def text_kill_report_victim(self):
        return 'Died in a(n) **{victimShipTypeID}**: **{0:get_killmail(killMailID, killMailHash)}**'

    def text_kill_report_final_blow(self):
        return 'Got final blow on **{victimShipTypeID}**: **{0:get_killmail(killMailID, killMailHash)}**'
