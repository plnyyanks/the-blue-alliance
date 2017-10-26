import unittest2

from google.appengine.ext import ndb
from google.appengine.ext import testbed

from helpers.district_manipulator import DistrictManipulator
from helpers.event_helper import EventHelper
from models.district import District


class TestEventGetShortName(unittest2.TestCase):
    def setUp(self):
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub(root_path=".")
        ndb.get_context().clear_cache(
        )  # Prevent data from leaking between tests

        # Create districts
        districts = []
        for code in [
                'mar', 'isr', 'nc', 'ne', 'pnw', 'pch', 'chs', 'in', 'ont',
                'fim'
        ]:
            year = 2017
            districts.append(
                District(
                    id=District.renderKeyName(year, code),
                    year=year,
                    abbreviation=code,
                ))
        DistrictManipulator.createOrUpdate(districts)

    def tearDown(self):
        self.testbed.deactivate()

    def test_event_get_short_name(self):
        # Edge cases.
        self.assertEquals(
            EventHelper.getShortName("  { Random 2.718 stuff! }  "),
            "{ Random 2.718 stuff! }")
        self.assertEquals(
            EventHelper.getShortName("IN District -Bee's Knee's LX  "),
            "Bee's Knee's LX")
        self.assertEquals(
            EventHelper.getShortName(
                "MAR District - Brussels Int'l Event sponsored by Sprouts"),
            "Brussels Int'l")
        self.assertEquals(
            EventHelper.getShortName(
                "FIM District - Brussels Int'l Eventapalooza sponsored by TBA"
            ), "Brussels Int'l")
        self.assertEquals(
            EventHelper.getShortName(
                "NE District - ReallyBigEvent Scaling Up Every Year"),
            "ReallyBig")
        self.assertEquals(
            EventHelper.getShortName("PNW District -  Event!  "), "Event!")

        self.assertEquals(
            EventHelper.getShortName(
                "FRC Detroit FIRST Robotics District Competition"), "Detroit")
        self.assertEquals(
            EventHelper.getShortName(
                "FIRST Robotics Detroit FRC State Championship"), "Detroit")
        self.assertEquals(
            EventHelper.getShortName("Maui FIRST Robotics Regional and Luau"),
            "Maui")
        self.assertEquals(
            EventHelper.getShortName(
                "California State Surf and Turf sponsored by TBA"),
            "California")
        self.assertEquals(
            EventHelper.getShortName("CarTalk Plaza Tournament"),
            "CarTalk Plaza")
        self.assertEquals(
            EventHelper.getShortName("IRI FRC Be-all and End-all"), "IRI")
        self.assertEquals(EventHelper.getShortName("   Ada    Field  "), "Ada")
        self.assertEquals(
            EventHelper.getShortName(
                " FIRST Robotics Einstein Field Equations "), "Einstein")
        self.assertEquals(
            EventHelper.getShortName(
                "FRC Martin Luther King Jr. Region Championship"),
            "Martin Luther King Jr.")
        self.assertEquals(
            EventHelper.getShortName(
                "PNW   Ada Lovelace    Tournament of Software  "),
            "Ada Lovelace")
        self.assertEquals(
            EventHelper.getShortName(
                "\tPNW   Ada Lovelace    Tournament of Software  "),
            "Ada Lovelace")
        self.assertEquals(
            EventHelper.getShortName(
                " MAR FIRST Robotics   Rosa Parks    FRC Tournament of Roses  "
            ), "Rosa Parks")
        self.assertEquals(
            EventHelper.getShortName("Washington D.C. FIRST Robotics Region"),
            "Washington D.C.")
        self.assertEquals(
            EventHelper.getShortName("Washington D.C. FIRST Robotics Region."),
            "Washington D.C.")
        self.assertEquals(
            EventHelper.getShortName(
                "Washington D.C. FIRST Robotics Regiontonian"),
            "Washington D.C. FIRST Robotics Regiontonian"
        )  # Does not match "Region\b"

        # Tests from various years
        self.assertEqual(
            EventHelper.getShortName("FIRST Robotics Competition"),
            "FIRST Robotics Competition")
        self.assertEqual(
            EventHelper.getShortName("National Championship"),
            "National Championship")
        self.assertEqual(
            EventHelper.getShortName("New England Tournament"), "New England")
        self.assertEqual(
            EventHelper.getShortName("FIRST National Championship"),
            "FIRST National Championship")
        self.assertEqual(
            EventHelper.getShortName("Motorola Midwest Regional"),
            "Motorola Midwest")
        self.assertEqual(
            EventHelper.getShortName("DEKA New England Regional"),
            "DEKA New England")
        self.assertEqual(
            EventHelper.getShortName(
                "Johnson & Johnson Mid-Atlantic Regional"),
            "Johnson & Johnson Mid-Atlantic")
        self.assertEqual(
            EventHelper.getShortName("Great Lakes Regional"), "Great Lakes")
        self.assertEqual(
            EventHelper.getShortName("New England Regional"), "New England")
        self.assertEqual(
            EventHelper.getShortName("Southwest Regional"), "Southwest")
        self.assertEqual(
            EventHelper.getShortName("NASA Ames Regional"), "NASA Ames")
        self.assertEqual(
            EventHelper.getShortName("Kennedy Space Center Regional"),
            "Kennedy Space Center")
        self.assertEqual(
            EventHelper.getShortName("UTC New England Regional"),
            "UTC New England")
        self.assertEqual(
            EventHelper.getShortName("Philadelphia Alliance Regional"),
            "Philadelphia Alliance")
        self.assertEqual(
            EventHelper.getShortName(
                "Kennedy Space Center Southeast Regional"),
            "Kennedy Space Center Southeast")
        self.assertEqual(
            EventHelper.getShortName("Long Island Regional"), "Long Island")
        self.assertEqual(
            EventHelper.getShortName("Lone Star Regional"), "Lone Star")
        self.assertEqual(
            EventHelper.getShortName("NASA Langley/VCU Regional"),
            "NASA Langley/VCU")
        self.assertEqual(
            EventHelper.getShortName("Archimedes Field"), "Archimedes")
        self.assertEqual(
            EventHelper.getShortName("Southern California Regional"),
            "Southern California")
        self.assertEqual(
            EventHelper.getShortName("Silicon Valley Regional"),
            "Silicon Valley")
        self.assertEqual(
            EventHelper.getShortName("UTC/New England Regional"),
            "UTC/New England")
        self.assertEqual(EventHelper.getShortName("Curie Field"), "Curie")
        self.assertEqual(
            EventHelper.getShortName("NASA KSC Southeast Regional"),
            "NASA KSC Southeast")
        self.assertEqual(EventHelper.getShortName("Galileo Field"), "Galileo")
        self.assertEqual(
            EventHelper.getShortName("West Michigan Regional"),
            "West Michigan")
        self.assertEqual(EventHelper.getShortName("Newton Field"), "Newton")
        self.assertEqual(
            EventHelper.getShortName("J&J Mid-Atlantic Regional"),
            "J&J Mid-Atlantic")
        self.assertEqual(
            EventHelper.getShortName("New York City Regional"),
            "New York City")
        self.assertEqual(
            EventHelper.getShortName("NASA Langley Regional"), "NASA Langley")
        self.assertEqual(
            EventHelper.getShortName("SBPLI Long Island Regional"),
            "SBPLI Long Island")
        self.assertEqual(
            EventHelper.getShortName("Western Michigan Regional"),
            "Western Michigan")
        self.assertEqual(
            EventHelper.getShortName("St. Louis Regional"), "St. Louis")
        self.assertEqual(
            EventHelper.getShortName("J&J Mid Atlantic Regional"),
            "J&J Mid Atlantic")
        self.assertEqual(
            EventHelper.getShortName("Buckeye Regional"), "Buckeye")
        self.assertEqual(
            EventHelper.getShortName("Canadian Regional"), "Canadian")
        self.assertEqual(
            EventHelper.getShortName("NASA Langley / VCU Regional"),
            "NASA Langley / VCU")
        self.assertEqual(
            EventHelper.getShortName("Pacific Northwest Regional"),
            "Pacific Northwest")
        self.assertEqual(
            EventHelper.getShortName("Arizona Regional"), "Arizona")
        self.assertEqual(
            EventHelper.getShortName("Einstein Field"), "Einstein")
        self.assertEqual(
            EventHelper.getShortName("Central Florida Regional"),
            "Central Florida")
        self.assertEqual(
            EventHelper.getShortName("Peachtree Regional"), "Peachtree")
        self.assertEqual(
            EventHelper.getShortName("Midwest Regional"), "Midwest")
        self.assertEqual(
            EventHelper.getShortName("Chesapeake Regional"), "Chesapeake")
        self.assertEqual(
            EventHelper.getShortName("BAE SYSTEMS Granite State Regional"),
            "BAE SYSTEMS Granite State")
        self.assertEqual(
            EventHelper.getShortName("Philadelphia Regional"), "Philadelphia")
        self.assertEqual(
            EventHelper.getShortName("Pittsburgh Regional"), "Pittsburgh")
        self.assertEqual(
            EventHelper.getShortName("Sacramento Regional"), "Sacramento")
        self.assertEqual(
            EventHelper.getShortName("NASA / VCU Regional"), "NASA / VCU")
        self.assertEqual(
            EventHelper.getShortName("Colorado Regional"), "Colorado")
        self.assertEqual(
            EventHelper.getShortName("Detroit Regional"), "Detroit")
        self.assertEqual(
            EventHelper.getShortName("Florida Regional"), "Florida")
        self.assertEqual(
            EventHelper.getShortName("New Jersey Regional"), "New Jersey")
        self.assertEqual(
            EventHelper.getShortName("Greater Toronto Regional"),
            "Greater Toronto")
        self.assertEqual(
            EventHelper.getShortName("Palmetto Regional"), "Palmetto")
        self.assertEqual(
            EventHelper.getShortName("Boilermaker Regional"), "Boilermaker")
        self.assertEqual(
            EventHelper.getShortName(
                "GM/Technion University Israel Pilot Regional"),
            "GM/Technion University Israel Pilot")
        self.assertEqual(
            EventHelper.getShortName("Las Vegas Regional"), "Las Vegas")
        self.assertEqual(
            EventHelper.getShortName("Finger Lakes Regional"), "Finger Lakes")
        self.assertEqual(
            EventHelper.getShortName("Waterloo Regional"), "Waterloo")
        self.assertEqual(
            EventHelper.getShortName("GM/Technion Israel Regional"),
            "GM/Technion Israel")
        self.assertEqual(EventHelper.getShortName("Boston Regional"), "Boston")
        self.assertEqual(
            EventHelper.getShortName("Davis Sacramento Regional"),
            "Davis Sacramento")
        self.assertEqual(
            EventHelper.getShortName("Wisconsin Regional"), "Wisconsin")
        self.assertEqual(
            EventHelper.getShortName("Brazil Pilot"), "Brazil Pilot")
        self.assertEqual(
            EventHelper.getShortName("Los Angeles Regional"), "Los Angeles")
        self.assertEqual(
            EventHelper.getShortName("UTC Connecticut Regional"),
            "UTC Connecticut")
        self.assertEqual(
            EventHelper.getShortName("Greater Kansas City Regional"),
            "Greater Kansas City")
        self.assertEqual(EventHelper.getShortName("Bayou Regional"), "Bayou")
        self.assertEqual(
            EventHelper.getShortName("San Diego Regional"), "San Diego")
        self.assertEqual(EventHelper.getShortName("Brazil Regional"), "Brazil")
        self.assertEqual(
            EventHelper.getShortName("Connecticut Regional"), "Connecticut")
        self.assertEqual(EventHelper.getShortName("Hawaii Regional"), "Hawaii")
        self.assertEqual(EventHelper.getShortName("Israel Regional"), "Israel")
        self.assertEqual(
            EventHelper.getShortName("Minnesota Regional"), "Minnesota")
        self.assertEqual(
            EventHelper.getShortName("BAE Systems Granite State Regional"),
            "BAE Systems Granite State")
        self.assertEqual(
            EventHelper.getShortName("Oklahoma City Regional"),
            "Oklahoma City")
        self.assertEqual(EventHelper.getShortName("Oregon Regional"), "Oregon")
        self.assertEqual(
            EventHelper.getShortName("UC Davis Sacramento Regional"),
            "UC Davis Sacramento")
        self.assertEqual(
            EventHelper.getShortName("Microsoft Seattle Regional"),
            "Microsoft Seattle")
        self.assertEqual(
            EventHelper.getShortName(
                "Dallas Regional, Sponsored by JCPenney and the JCPenney Afterschool Fund"
            ), "Dallas")
        self.assertEqual(
            EventHelper.getShortName("Washington DC  Regional"),
            "Washington DC")
        self.assertEqual(
            EventHelper.getShortName(
                "Detroit FIRST Robotics District Competition"), "Detroit")
        self.assertEqual(
            EventHelper.getShortName(
                "Cass Tech FIRST Robotics District Competition"), "Cass Tech")
        self.assertEqual(
            EventHelper.getShortName(
                "Kettering University FIRST Robotics District Competition"),
            "Kettering University")
        self.assertEqual(
            EventHelper.getShortName(
                "Michigan FIRST Robotics Competition State Championship"),
            "Michigan")
        self.assertEqual(
            EventHelper.getShortName(
                "Lansing FIRST Robotics District Competition"), "Lansing")
        self.assertEqual(
            EventHelper.getShortName(
                "Traverse City FIRST Robotics District Competition"),
            "Traverse City")
        self.assertEqual(
            EventHelper.getShortName(
                "West Michigan FIRST Robotics District Competition"),
            "West Michigan")
        self.assertEqual(
            EventHelper.getShortName("Minnesota 10000 Lakes Regional"),
            "Minnesota 10000 Lakes")
        self.assertEqual(
            EventHelper.getShortName("Minnesota North Star Regional"),
            "Minnesota North Star")
        self.assertEqual(
            EventHelper.getShortName("BAE Granite State Regional"),
            "BAE Granite State")
        self.assertEqual(
            EventHelper.getShortName(
                "Troy FIRST Robotics District Competition"), "Troy")
        self.assertEqual(
            EventHelper.getShortName("NASA VCU Regional"), "NASA VCU")
        self.assertEqual(
            EventHelper.getShortName(
                "Northeast Utilities FIRST Connecticut Regional"),
            "Northeast Utilities FIRST Connecticut")
        self.assertEqual(
            EventHelper.getShortName(
                "Dallas Regional sponsored by JCPenney and the JCPenney Afterschool Fund"
            ), "Dallas")
        self.assertEqual(
            EventHelper.getShortName(
                "Hawaii Regional sponsored by BAE Systems"), "Hawaii")
        self.assertEqual(
            EventHelper.getShortName("North Carolina Regional"),
            "North Carolina")
        self.assertEqual(
            EventHelper.getShortName("Oklahoma Regional"), "Oklahoma")
        self.assertEqual(
            EventHelper.getShortName("Autodesk Oregon Regional"),
            "Autodesk Oregon")
        self.assertEqual(
            EventHelper.getShortName(
                "Silicon Valley Regional sponsored by Google and BAE Systems"),
            "Silicon Valley")
        self.assertEqual(
            EventHelper.getShortName(
                "Utah Regional sponsored by NASA & Platt"), "Utah")
        self.assertEqual(
            EventHelper.getShortName("Virginia Regional"), "Virginia")
        self.assertEqual(
            EventHelper.getShortName(
                "Ann Arbor FIRST Robotics District Competition"), "Ann Arbor")
        self.assertEqual(EventHelper.getShortName("WPI Regional"), "WPI")
        self.assertEqual(
            EventHelper.getShortName("Dallas Regional sponsored by jcpenney"),
            "Dallas")
        self.assertEqual(
            EventHelper.getShortName("Lake Superior Regional"),
            "Lake Superior")
        self.assertEqual(
            EventHelper.getShortName(
                "Michigan FIRST Robotics District Competition State Championship"
            ), "Michigan")
        self.assertEqual(
            EventHelper.getShortName("BAE Systems/Granite State Regional"),
            "BAE Systems/Granite State")
        self.assertEqual(
            EventHelper.getShortName(
                "Waterford FIRST Robotics District Competition"), "Waterford")
        self.assertEqual(
            EventHelper.getShortName("Greater Toronto East Regional"),
            "Greater Toronto East")
        self.assertEqual(
            EventHelper.getShortName("Greater Toronto West Regional"),
            "Greater Toronto West")
        self.assertEqual(EventHelper.getShortName("Alamo Regional"), "Alamo")
        self.assertEqual(
            EventHelper.getShortName(
                "Niles FIRST Robotics District Competition"), "Niles")
        self.assertEqual(
            EventHelper.getShortName("Smoky Mountain Regional"),
            "Smoky Mountain")
        self.assertEqual(
            EventHelper.getShortName(
                "Utah Regional co-sponsored by NASA and Platt"), "Utah")
        self.assertEqual(
            EventHelper.getShortName("Seattle Olympic Regional"),
            "Seattle Olympic")
        self.assertEqual(
            EventHelper.getShortName("Seattle Cascade Regional"),
            "Seattle Cascade")
        self.assertEqual(
            EventHelper.getShortName(
                "Livonia FIRST Robotics District Competition"), "Livonia")
        self.assertEqual(
            EventHelper.getShortName("Central Valley Regional"),
            "Central Valley")
        self.assertEqual(
            EventHelper.getShortName(
                "Dallas East Regional sponsored by jcpenney"), "Dallas East")
        self.assertEqual(
            EventHelper.getShortName(
                "Dallas West Regional sponsored by jcpenney"), "Dallas West")
        self.assertEqual(
            EventHelper.getShortName("Orlando Regional"), "Orlando")
        self.assertEqual(
            EventHelper.getShortName("Michigan FRC State Championship"),
            "Michigan")
        self.assertEqual(
            EventHelper.getShortName(
                "Gull Lake FIRST Robotics District Competition"), "Gull Lake")
        self.assertEqual(
            EventHelper.getShortName(
                "Rutgers University FIRST Robotics District Competition"),
            "Rutgers University")
        self.assertEqual(
            EventHelper.getShortName(
                "Mount Olive FIRST Robotics District Competition"),
            "Mount Olive")
        self.assertEqual(
            EventHelper.getShortName(
                "Lenape FIRST Robotics District Competition"), "Lenape")
        self.assertEqual(
            EventHelper.getShortName("Queen City Regional"), "Queen City")
        self.assertEqual(
            EventHelper.getShortName(
                "Mid-Atlantic Robotics FRC Region Championship"),
            "Mid-Atlantic Robotics")
        self.assertEqual(
            EventHelper.getShortName(
                "Hatboro-Horsham FIRST Robotics District Competition"),
            "Hatboro-Horsham")
        self.assertEqual(
            EventHelper.getShortName(
                "Chestnut Hill FIRST Robotics District Competition"),
            "Chestnut Hill")
        self.assertEqual(
            EventHelper.getShortName(
                "Festival de Robotique FRC a Montreal Regional"),
            "Festival de Robotique")
        self.assertEqual(
            EventHelper.getShortName("South Florida Regional"),
            "South Florida")
        self.assertEqual(
            EventHelper.getShortName("Smoky Mountains Regional"),
            "Smoky Mountains")
        self.assertEqual(
            EventHelper.getShortName("Spokane Regional"), "Spokane")
        self.assertEqual(
            EventHelper.getShortName(
                "Northville FIRST Robotics District Competition"),
            "Northville")
        self.assertEqual(
            EventHelper.getShortName("Western Canadian FRC Regional"),
            "Western Canadian")
        self.assertEqual(
            EventHelper.getShortName("Razorback Regional"), "Razorback")
        self.assertEqual(
            EventHelper.getShortName("Phoenix Regional"), "Phoenix")
        self.assertEqual(
            EventHelper.getShortName(
                "Los Angeles Regional sponsored by The Roddenberry Foundation"
            ), "Los Angeles")
        self.assertEqual(
            EventHelper.getShortName("Inland Empire Regional"),
            "Inland Empire")
        self.assertEqual(
            EventHelper.getShortName("Connecticut Regional sponsored by UTC"),
            "Connecticut")
        self.assertEqual(
            EventHelper.getShortName("Crossroads Regional"), "Crossroads")
        self.assertEqual(
            EventHelper.getShortName("Pine Tree Regional"), "Pine Tree")
        self.assertEqual(
            EventHelper.getShortName(
                "Bedford FIRST Robotics District Competition"), "Bedford")
        self.assertEqual(
            EventHelper.getShortName(
                "Grand Blanc FIRST Robotics District Competition"),
            "Grand Blanc")
        self.assertEqual(
            EventHelper.getShortName(
                "St Joseph FIRST Robotics District Competition"), "St Joseph")
        self.assertEqual(
            EventHelper.getShortName("Northern Lights Regional"),
            "Northern Lights")
        self.assertEqual(
            EventHelper.getShortName(
                "Bridgewater-Raritan FIRST Robotics District Competition"),
            "Bridgewater-Raritan")
        self.assertEqual(
            EventHelper.getShortName(
                "TCNJ FIRST Robotics District Competition"), "TCNJ")
        self.assertEqual(
            EventHelper.getShortName(
                "Lenape Seneca FIRST Robotics District Competition"),
            "Lenape Seneca")
        self.assertEqual(
            EventHelper.getShortName(
                "Springside - Chestnut Hill FIRST Robotics District Competition"
            ), "Springside - Chestnut Hill")
        self.assertEqual(
            EventHelper.getShortName(
                "Festival de Robotique FRC de Montreal Regional"),
            "Festival de Robotique")
        self.assertEqual(EventHelper.getShortName("Dallas Regional"), "Dallas")
        self.assertEqual(
            EventHelper.getShortName("Hub City Regional"), "Hub City")
        self.assertEqual(
            EventHelper.getShortName(
                "Alamo Regional sponsored by Rackspace Hosting"), "Alamo")
        self.assertEqual(
            EventHelper.getShortName(
                "Utah Regional co-sponsored by the Larry H. Miller Group & Platt"
            ), "Utah")
        self.assertEqual(
            EventHelper.getShortName("Seattle Regional"), "Seattle")
        self.assertEqual(
            EventHelper.getShortName("Central Washington Regional"),
            "Central Washington")
        self.assertEqual(
            EventHelper.getShortName("Western Canada Regional"),
            "Western Canada")
        self.assertEqual(
            EventHelper.getShortName("Arkansas Regional"), "Arkansas")
        self.assertEqual(
            EventHelper.getShortName("Groton District Event"), "Groton")
        self.assertEqual(
            EventHelper.getShortName("Hartford District Event"), "Hartford")
        self.assertEqual(
            EventHelper.getShortName("Southington District Event"),
            "Southington")
        self.assertEqual(
            EventHelper.getShortName("Greater DC Regional"), "Greater DC")
        self.assertEqual(
            EventHelper.getShortName("Central Illinois Regional"),
            "Central Illinois")
        self.assertEqual(
            EventHelper.getShortName("Northeastern University District Event"),
            "Northeastern University")
        self.assertEqual(EventHelper.getShortName("WPI District Event"), "WPI")
        self.assertEqual(
            EventHelper.getShortName("Pine Tree District Event"), "Pine Tree")
        self.assertEqual(
            EventHelper.getShortName(
                "Center Line FIRST Robotics District Competition"),
            "Center Line")
        self.assertEqual(
            EventHelper.getShortName(
                "Escanaba FIRST Robotics District Competition"), "Escanaba")
        self.assertEqual(
            EventHelper.getShortName(
                "Howell FIRST Robotics District Competition"), "Howell")
        self.assertEqual(
            EventHelper.getShortName(
                "St. Joseph FIRST Robotics District Competition"),
            "St. Joseph")
        self.assertEqual(
            EventHelper.getShortName(
                "Southfield FIRST Robotics District Competition"),
            "Southfield")
        self.assertEqual(
            EventHelper.getShortName("Mexico City Regional"), "Mexico City")
        self.assertEqual(
            EventHelper.getShortName("New England FRC Region Championship"),
            "New England")
        self.assertEqual(EventHelper.getShortName("UNH District Event"), "UNH")
        self.assertEqual(
            EventHelper.getShortName("Granite State District Event"),
            "Granite State")
        self.assertEqual(
            EventHelper.getShortName(
                "MAR FIRST Robotics Bridgewater-Raritan District Competition"),
            "Bridgewater-Raritan")
        self.assertEqual(
            EventHelper.getShortName(
                "MAR FIRST Robotics Clifton District Competition"), "Clifton")
        self.assertEqual(
            EventHelper.getShortName(
                "MAR FIRST Robotics Mt. Olive District Competition"),
            "Mt. Olive")
        self.assertEqual(
            EventHelper.getShortName(
                "MAR FIRST Robotics Lenape-Seneca District Competition"),
            "Lenape-Seneca")
        self.assertEqual(
            EventHelper.getShortName("New York Tech Valley Regional"),
            "New York Tech Valley")
        self.assertEqual(
            EventHelper.getShortName("North Bay Regional"), "North Bay")
        self.assertEqual(
            EventHelper.getShortName("Windsor Essex Great Lakes Regional"),
            "Windsor Essex Great Lakes")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Oregon City District Event"),
            "Oregon City")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Oregon State University District Event"),
            "Oregon State University")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Wilsonville District Event"),
            "Wilsonville")
        self.assertEqual(
            EventHelper.getShortName(
                "MAR FIRST Robotics Hatboro-Horsham District Competition"),
            "Hatboro-Horsham")
        self.assertEqual(
            EventHelper.getShortName(
                "MAR FIRST Robotics Springside Chestnut Hill District Competition"
            ), "Springside Chestnut Hill")
        self.assertEqual(
            EventHelper.getShortName("Greater Pittsburgh Regional"),
            "Greater Pittsburgh")
        self.assertEqual(
            EventHelper.getShortName("Autodesk PNW FRC Championship"),
            "Autodesk PNW")
        self.assertEqual(
            EventHelper.getShortName("Rhode Island District Event"),
            "Rhode Island")
        self.assertEqual(EventHelper.getShortName("Utah Regional"), "Utah")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Auburn District Event"), "Auburn")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Auburn Mountainview District Event"),
            "Auburn Mountainview")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Eastern Washington University District Event"
            ), "Eastern Washington University")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Central Washington University District Event"
            ), "Central Washington University")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Mt. Vernon District Event"), "Mt. Vernon")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Shorewood District Event"), "Shorewood")
        self.assertEqual(
            EventHelper.getShortName(
                "PNW FIRST Robotics Glacier Peak District Event"),
            "Glacier Peak")
        # 2015 edge cases
        self.assertEqual(
            EventHelper.getShortName("FIM District - Howell Event"), "Howell")
        self.assertEqual(
            EventHelper.getShortName("NE District - Granite State Event"),
            "Granite State")
        self.assertEqual(
            EventHelper.getShortName("PNW District - Oregon City Event"),
            "Oregon City")
        self.assertEqual(
            EventHelper.getShortName("IN District -Indianapolis"),
            "Indianapolis")
        self.assertEqual(
            EventHelper.getShortName("MAR District - Mt. Olive Event"),
            "Mt. Olive")
        self.assertEqual(
            EventHelper.getShortName(
                "Israel Regional - see Site Info for additional information"),
            "Israel")
        self.assertEqual(
            EventHelper.getShortName(
                "IN District - Kokomo City of Firsts Event sponsored by AndyMark"
            ), "Kokomo City of Firsts")
        # 2017 edge cases
        self.assertEqual(
            EventHelper.getShortName(
                "ONT District - McMaster University Event"),
            "McMaster University")
        self.assertEqual(
            EventHelper.getShortName("FIRST Ontario Provincial Championship"),
            "Ontario")
        self.assertEqual(
            EventHelper.getShortName(
                "FIM District - Kettering University Event #1"),
            "Kettering University #1")
        self.assertEqual(
            EventHelper.getShortName("ISR District Event #1"), "ISR #1")
        # 2018 edge cases
        self.assertEqual(
            EventHelper.getShortName("PNW District Clackamas Academy Event"),
            "Clackamas Academy")
