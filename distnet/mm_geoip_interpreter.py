"""
    MaxMindDB reader and searcher class.
    TODO:  use geolite2 or implement
"""
import ipaddress
import pkg_resources

db_path = str(pkg_resources.resource_filename(__name__, 'resources/GeoIP/'))




class GeoIP_Controller_ReadDataError(Exception):
    def __init__(self, message):
        super(Exception, self).__init__(message)



class GeoIP_Controller():
    def __init__(self):

        self.__blocks_data = None
        self.__locations_data = None

        self.__blocks_list = None
        self.__locations_list = None

        self.__locations_dict = dict()
        self.__blocks_dict = dict()

        try:
            with open(db_path + str('GeoLite2-Country-Blocks-IPv4.csv')) as cbd:
                self.__blocks_data = cbd.read()

            with open(db_path + str('GeoLite2-Country-Locations-en.csv')) as cld:
                self.__location_data = cld.read()

        except Exception:
            raise GeoIP_Controller_ReadDataError("")


        try:
            self.__blocks_list = self.__blocks_data.split('\n')
            self.__locations_list = self.__location_data.split('\n')
        except Exception:
            raise GeoIP_Controller_ReadDataError("")

        for item in self.__locations_list[1:]:
            if item == "":
                continue
            country_id = item.split(',')[0]
            self.__locations_dict[country_id] = item.split(',')[4]


        for item in self.__blocks_list[1:]:
            if item == "":
                continue
            lsplit = item.split(',')
            cdir_ip_string = lsplit[0]
            cdir_ip_firstbits = cdir_ip_string.split('.')[0]


            if cdir_ip_firstbits not in self.__blocks_dict.keys():
                self.__blocks_dict[cdir_ip_firstbits] = list()
                self.__blocks_dict[cdir_ip_firstbits].append(item)
            else:
                self.__blocks_dict[cdir_ip_firstbits].append(item)


    def search_CIDR_location(self, normal_ip):

        firstbits=normal_ip.split('.')[0]

        for line in self.__blocks_dict[firstbits]:
            lsplit = line.split(',')
            cidr_ip_string = lsplit[0]
            country_geoname_id = lsplit[2]

            if cidr_ip_string.split('.')[1] != normal_ip.split('.')[1]:
                continue

            hosts_list = list(ipaddress.ip_network(cidr_ip_string).hosts())
            for item in hosts_list:
                if item.exploded == normal_ip:
                    if country_geoname_id != '':
                        return self.__locations_dict[country_geoname_id]
                    else:
                        return None

        return None
