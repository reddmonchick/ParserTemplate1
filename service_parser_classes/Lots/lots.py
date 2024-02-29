from service_parser_classes.Lots.lot_items import LotItems


class Lots:
    def __init__(self, soup):
        self.soup = soup

    def get_data(self) -> list[dict]:
        lots = []
        # в цикле
        lot = {
            'region': self._get_region(),
            'deliveryPlace': None,
            'lotItems': LotItems(self.soup).get_data()
        }
        # lots.appen(lot)

        return lots

    def _get_region(self):
        region = self.soup.find('div', class_='region')
        if region:
            return region.get_text()
