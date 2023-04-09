import usaddress
addr = usaddress.tag('Maison Jar, 566 Leonard Street, Brooklyn, NY 11222')
print(addr)
print(addr[0]['Recipient'] + ', ' + addr[0]['AddressNumber'] + ' ' + addr[0]['StreetName'] + ' ' + addr[0]['StreetNamePostType'] + ', ' + addr[0]['PlaceName'] + ', ' + addr[0]['StateName'] + ' ' + addr[0]['ZipCode'])
print('Maison Jar, 566 Leonard Street, Brooklyn, NY 11222')

def parse_address(row):
    ap = AddressParser()
    address = ap.parse_address('123 West Mifflin Street, Madison, WI, 53703')
    print("Address is: {0} {1} {2} {3}".format(address.house_number, address.street_prefix, address.street, address.street_suffix))
    return row