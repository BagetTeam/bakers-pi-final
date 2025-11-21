from package_discovery.package_discovery import PackageDiscovery

class PackageDeliveryTest:
    def __init__(self, package_discovery: PackageDiscovery):
        self.package_discovery = package_discovery
    
    def test(self):
        self.package_discovery.explore_room()