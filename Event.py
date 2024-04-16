from EventOrigin import EventOrigin
import json

class DeviceEvent:
    def __init__(self, _id, dev_id, hostname, os, ip_address, agent_version, agent_local_time, mac_address, event_origin):
        self._id = _id
        self.device_id = dev_id
        self.hostname = hostname
        self.os = os
        self.ip_address = ip_address
        self.agent_version = agent_version
        self.agent_local_time = agent_local_time
        self.mac_address = mac_address
        self.event_origin = event_origin

    def serialize(self):
        '''
        basic serialization, but these can be more complex - use avro instead if needed
        '''
        _data =  {"id" : self._id, 
                "device_id" : self.device_id,
                "hostname" : self.hostname,
                "os" : self.os,
                "ip_addr " : self.ip_address,
                "agent_version" : self.agent_version, 
                "agent_local_time" : self.agent_local_time,
                "mac_address" : self.mac_address,
                "event_source " : self.event_origin 
                }
        return json.dumps(_data)

    @staticmethod
    def createEvent(jsn_event):
        if "os" in jsn_event.keys() :
            _event_id, _dev_id, _hostname, _os, _ip_address, _agent_version, _time, _mac_addr, _event_origin= DeviceEvent.qualys_parser(jsn_event)
        elif "os_version" in jsn_event.keys():
            _event_id, _dev_id, _hostname, _os, _ip_address, _agent_version, _time, _mac_addr, _event_origin= DeviceEvent.crowdstrike_parser(jsn_event)
        else:
            raise Exception("The event origin type processor is not implemented")
        return DeviceEvent(_event_id, _dev_id, _hostname, _os, _ip_address, _agent_version, _time, _mac_addr, _event_origin)
        
    @staticmethod
    def crowdstrike_parser(event):
        try:
            _dev_id = event['device_id']
            _event_id = event['_id']
            _os = event["os_version"]
            _hostname = event["hostname"]
            _ip_address = event["connection_ip"]
            _time = event["agent_local_time"]
            _agent_version = event["agent_version"]
            _mac_addr = event["mac_address"]
            _event_origin = EventOrigin.CROWDSTRIKE
        except Exception as e:
            raise Exception(e)
        return _event_id, _dev_id, _hostname, _os, _ip_address, _agent_version, _time, _mac_addr, _event_origin

    @staticmethod       
    def qualys_parser(event):
        try:
            _dev_id = event['id']
            event_id = event['_id']
            _os = event["os"]
            _hostname = event["dnsHostName"]
            _ip_address = event["address"]
            _time = event["agentInfo"]["lastCheckedIn"]
            _agent_version = event["agentInfo"]["agentVersion"]
            interfaces = event["networkInterface"]
            #just pick the first mac address for proof of concept
            _mac = ""
            for l in interfaces["list"]:
                if "HostAssetInterface" in l :
                    t =l["HostAssetInterface"]
                    if "macAddress" in t:
                        _mac = t["macAddress"]
                        break
            else:
                print("does not have mac address ")
                #raise Exception("does not have mac address")

            _mac_addr = _mac
            _event_origin = EventOrigin.QUALYS
        except Exception as e:
            raise Exception(e)
        return event_id, _dev_id, _hostname, _os, _ip_address, _agent_version, _time, _mac_addr, _event_origin


